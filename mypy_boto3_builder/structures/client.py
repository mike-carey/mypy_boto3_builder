"""
Boto3 Client.
"""
from typing import Iterator, List

from botocore.client import BaseClient

from mypy_boto3_builder.enums.service_module_name import ServiceModuleName
from mypy_boto3_builder.service_name import ServiceName
from mypy_boto3_builder.structures.argument import Argument
from mypy_boto3_builder.structures.attribute import Attribute
from mypy_boto3_builder.structures.class_record import ClassRecord
from mypy_boto3_builder.structures.method import Method
from mypy_boto3_builder.type_annotations.internal_import import InternalImport
from mypy_boto3_builder.type_annotations.type import Type
from mypy_boto3_builder.type_annotations.type_class import TypeClass
from mypy_boto3_builder.type_annotations.type_subscript import TypeSubscript


class Client(ClassRecord):
    """
    Boto3 Client.
    """

    _alias_name: str = "Client"

    def __init__(self, name: str, service_name: ServiceName, boto3_client: BaseClient) -> None:
        super().__init__(name=name)
        self.service_name = service_name
        self.boto3_client = boto3_client
        self.exceptions_class = ClassRecord(name="Exceptions")
        self.bases = [TypeClass(BaseClient)]
        self.client_error_class = ClassRecord(
            name="BotocoreClientError",
            attributes=[
                Attribute("MSG_TEMPLATE", Type.str),
            ],
            bases=[TypeClass(BaseException)],
            methods=[
                Method(
                    name="__init__",
                    arguments=[
                        Argument("self", None),
                        Argument("error_response", TypeSubscript(Type.Dict, [Type.str, Type.Any])),
                        Argument("operation_name", Type.str),
                    ],
                    return_type=Type.none,
                    body_lines=[
                        "self.response: Dict[str, Any]",
                        "self.operation_name: str",
                    ],
                ),
            ],
        )

    def __hash__(self) -> int:
        """
        Calculate hash from client service name.
        """
        return hash(self.service_name)

    @property
    def boto3_doc_link(self) -> str:
        """
        List to boto3 docs page.
        """
        return self.service_name.get_boto3_doc_link("Client")

    @property
    def docstring(self) -> str:
        """
        Class docstring.
        """
        return (
            "[Show boto3 documentation]"
            f"({self.boto3_doc_link})\n"
            "[Show boto3-stubs documentation]"
            f"({self.service_name.get_doc_link('client')})"
        )

    def get_all_names(self) -> List[str]:
        """
        Get a list of names for `__all__` statement.
        """
        return [self.name]

    @property
    def own_methods(self) -> Iterator[Method]:
        """
        Get a list of auto-generated methods.
        """
        for method in self.methods:
            if method.name not in ("get_waiter", "get_paginator"):
                yield method

    def get_exceptions_property(self) -> Method:
        """
        Generate Client exceptions property.
        """
        return Method(
            name="exceptions",
            decorators=[TypeClass(property)],
            arguments=[
                Argument("self", None),
            ],
            return_type=InternalImport(
                name=self.exceptions_class.name,
                module_name=ServiceModuleName.client,
                service_name=self.service_name,
                stringify=False,
            ),
            docstring=f"{self.name} exceptions.",
        )
