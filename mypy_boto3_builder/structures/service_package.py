"""
Parsed Service package.
"""
from typing import Dict, Iterable, List, Optional, Set

from mypy_boto3_builder.enums.service_module_name import ServiceModuleName
from mypy_boto3_builder.import_helpers.import_record import ImportRecord
from mypy_boto3_builder.import_helpers.import_string import ImportString
from mypy_boto3_builder.service_name import ServiceName
from mypy_boto3_builder.structures.client import Client
from mypy_boto3_builder.structures.function import Function
from mypy_boto3_builder.structures.package import Package
from mypy_boto3_builder.structures.paginator import Paginator
from mypy_boto3_builder.structures.service_resource import ServiceResource
from mypy_boto3_builder.structures.waiter import Waiter
from mypy_boto3_builder.type_annotations.fake_annotation import FakeAnnotation
from mypy_boto3_builder.type_annotations.type_literal import TypeLiteral
from mypy_boto3_builder.type_annotations.type_typed_dict import TypeTypedDict
from mypy_boto3_builder.utils.strings import is_reserved


class ServicePackage(Package):
    """
    Parsed Service package.
    """

    def __init__(
        self,
        name: str,
        pypi_name: str,
        service_name: ServiceName,
        client: Client,
        service_resource: Optional[ServiceResource] = None,
        waiters: Iterable[Waiter] = tuple(),
        paginators: Iterable[Paginator] = tuple(),
        typed_dicts: Iterable[TypeTypedDict] = tuple(),
        literals: Iterable[TypeLiteral] = tuple(),
        helper_functions: Iterable[Function] = tuple(),
    ):
        super().__init__(name=name, pypi_name=pypi_name)
        self.service_name = service_name
        self.client = client
        self.service_resource = service_resource
        self.waiters = list(waiters)
        self.paginators = list(paginators)
        self.typed_dicts = list(typed_dicts)
        self.literals = list(literals)
        self.helper_functions = list(helper_functions)

    def extract_literals(self) -> List[TypeLiteral]:
        """
        Extract literals from children.
        """
        found: Dict[str, TypeLiteral] = {}
        for type_annotation in sorted([*self.get_types(), *self.typed_dicts]):
            current: List[TypeLiteral] = []
            if isinstance(type_annotation, TypeTypedDict):
                current.extend(type_annotation.get_children_literals())
            if isinstance(type_annotation, TypeLiteral):
                current.append(type_annotation)

            for literal in current:
                if literal.name not in found:
                    found[literal.name] = literal
                    continue

                old_literal = found[literal.name]
                if not literal.is_same(old_literal):
                    raise ValueError(
                        f"Duplicate literal: {literal.name} {literal.children} != {old_literal.children}"
                    )

        return list(sorted(found.values()))

    def _get_typed_dicts(self) -> Set[TypeTypedDict]:
        result: Set[TypeTypedDict] = set()
        for type_annotation in self.get_types():
            if not isinstance(type_annotation, TypeTypedDict):
                continue
            result.add(type_annotation)

        for method in self.client.methods:
            if method.request_type_annotation:
                result.add(method.request_type_annotation)
        if self.service_resource:
            for method in self.service_resource.methods:
                if method.request_type_annotation:
                    result.add(method.request_type_annotation)
            for resource in self.service_resource.sub_resources:
                for method in resource.methods:
                    if method.request_type_annotation:
                        result.add(method.request_type_annotation)
        return result

    def extract_typed_dicts(self) -> List[TypeTypedDict]:
        """
        Extract typed dicts from children.

        Attempts to resolve circular typed dicts.
        """
        added_hashes: List[int] = []
        result: List[TypeTypedDict] = []
        discovered: List[TypeTypedDict] = []
        typed_dicts = self._get_typed_dicts()
        for type_annotation in sorted(typed_dicts):
            if hash(type_annotation) in added_hashes:
                continue

            result.append(type_annotation)
            added_hashes.append(hash(type_annotation))
            discovered.append(type_annotation)

        while discovered:
            child = discovered.pop()
            sub_typed_dicts = child.get_children_typed_dicts()
            for child_typed_dict in sorted(sub_typed_dicts):
                child_typed_dict.stringify = True

                if hash(child_typed_dict) in added_hashes:
                    continue

                result.append(child_typed_dict)
                added_hashes.append(hash(child_typed_dict))
                discovered.append(child_typed_dict)

        result.sort()
        return result

    def get_types(self) -> Set[FakeAnnotation]:
        """
        Extract type annotations from Client, ServiceResource, waiters and paginators.
        """
        types: Set[FakeAnnotation] = set()
        types.update(self.client.get_types())
        if self.service_resource:
            types.update(self.service_resource.get_types())
        for waiter in self.waiters:
            types.update(waiter.get_types())
        for paginator in self.paginators:
            types.update(paginator.get_types())

        return types

    def get_init_import_records(self) -> List[ImportRecord]:
        """
        Get import records for `__init__.py[i]`.
        """
        import_records: Set[ImportRecord] = set()
        import_records.add(
            ImportRecord(
                ImportString.parent() + ImportString(ServiceModuleName.client.name),
                self.client.name,
            )
        )
        if self.service_resource:
            import_records.add(
                ImportRecord(
                    ImportString.parent() + ImportString(ServiceModuleName.service_resource.name),
                    self.service_resource.name,
                )
            )
        for waiter in self.waiters:
            import_records.add(
                ImportRecord(
                    ImportString.parent() + ImportString(ServiceModuleName.waiter.name),
                    waiter.name,
                )
            )
        for paginator in self.paginators:
            import_records.add(
                ImportRecord(
                    ImportString.parent() + ImportString(ServiceModuleName.paginator.name),
                    paginator.name,
                )
            )

        return list(sorted(import_records))

    def get_init_all_names(self) -> List[str]:
        """
        Get `__all__` statement names for `__init__.py[i]`.
        """
        names = {self.client.name, self.client.alias_name}
        if self.service_resource:
            names.add(self.service_resource.name)
            names.add(self.service_resource.alias_name)
        for waiter in self.waiters:
            names.add(waiter.name)
        for paginator in self.paginators:
            names.add(paginator.name)

        result = list(names)
        result.sort()
        return result

    def get_client_required_import_records(self) -> List[ImportRecord]:
        """
        Get import records for `client.py[i]`.
        """
        import_records: Set[ImportRecord] = set()
        for import_record in self.client.get_required_import_records():
            import_records.add(import_record.get_external(self.service_name.module_name))
            if import_record.fallback:
                import_records.add(ImportRecord(ImportString("sys")))
        for import_record in self.client.exceptions_class.get_required_import_records():
            import_records.add(import_record.get_external(self.service_name.module_name))
            if import_record.fallback:
                import_records.add(ImportRecord(ImportString("sys")))

        return list(sorted(import_records))

    def get_service_resource_required_import_records(self) -> List[ImportRecord]:
        """
        Get import records for `service_resource.py[i]`.
        """
        if self.service_resource is None:
            return []

        import_records: Set[ImportRecord] = set()
        class_import_records = self.service_resource.get_required_import_records()
        for import_record in class_import_records:
            import_records.add(import_record.get_external(self.service_name.module_name))
            if import_record.fallback:
                import_records.add(ImportRecord(ImportString("sys")))

        return list(sorted(import_records))

    def get_paginator_required_import_records(self) -> List[ImportRecord]:
        """
        Get import records for `paginator.py[i]`.
        """
        import_records: Set[ImportRecord] = set()
        for paginator in self.paginators:
            for import_record in paginator.get_required_import_records():
                import_records.add(import_record.get_external(self.service_name.module_name))
                if import_record.fallback:
                    import_records.add(ImportRecord(ImportString("sys")))

        return list(sorted(import_records))

    def get_waiter_required_import_records(self) -> List[ImportRecord]:
        """
        Get import records for `waiter.py[i]`.
        """
        import_records: Set[ImportRecord] = set()
        for waiter in self.waiters:
            for import_record in waiter.get_required_import_records():
                import_records.add(import_record.get_external(self.service_name.module_name))
                if import_record.fallback:
                    import_records.add(ImportRecord(ImportString("sys")))

        return list(sorted(import_records))

    def get_type_defs_required_import_records(self) -> List[ImportRecord]:
        """
        Get import records for `type_defs.py[i]`.
        """
        if not self.typed_dicts:
            return []

        import_records: Set[ImportRecord] = set()
        import_records.add(ImportRecord(ImportString("sys")))
        import_records.add(
            ImportRecord(
                ImportString("typing"),
                "TypedDict",
                min_version=(3, 8),
                fallback=ImportRecord(ImportString("typing_extensions"), "TypedDict"),
            )
        )
        for typed_dict in self.typed_dicts:
            if typed_dict.replace_with_dict:
                import_records.add(
                    ImportRecord(
                        ImportString("typing"),
                        "Dict",
                    )
                )
                import_records.add(
                    ImportRecord(
                        ImportString("typing"),
                        "Any",
                    )
                )
            for type_annotation in typed_dict.get_children_types():
                import_record = type_annotation.get_import_record()
                if not import_record or import_record.is_builtins():
                    continue
                if import_record.is_type_defs():
                    continue
                import_records.add(import_record.get_external(self.service_name.module_name))

        return list(sorted(import_records))

    def get_literals_required_import_records(self) -> List[ImportRecord]:
        """
        Get import records for `literals.py[i]`.
        """
        import_records: Set[ImportRecord] = set()
        import_records.add(ImportRecord(ImportString("sys")))
        import_records.add(
            ImportRecord(
                ImportString("typing"),
                "Literal",
                min_version=(3, 8),
                fallback=ImportRecord(ImportString("typing_extensions"), "Literal"),
            )
        )
        return list(sorted(import_records))

    def validate(self) -> None:
        """
        Validate parsed module.

        Finds duplicated names.
        Finds conflicts with reserved Python words.
        """
        names = set()
        for name in (
            *(i.name for i in self.typed_dicts),
            *(i.name for i in self.literals),
            *(i.name for i in self.waiters),
            *(i.name for i in self.paginators),
            *(self.service_resource.get_all_names() if self.service_resource else []),
        ):
            if is_reserved(name):
                raise ValueError(f"{name} is a reserved keyword")
            if name in names:
                for typed_dict in self.typed_dicts:
                    if typed_dict.name == name:
                        self.logger.warning(
                            f"{typed_dict}: {[c.render() for c in typed_dict.children]}"
                        )
                raise ValueError(f"Duplicate name {name}")
            names.add(name)
