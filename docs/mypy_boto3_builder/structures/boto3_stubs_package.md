# Boto3StubsPackage

> Auto-generated documentation for [mypy_boto3_builder.structures.boto3_stubs_package](https://github.com/vemel/mypy_boto3_builder/blob/master/mypy_boto3_builder/structures/boto3_stubs_package.py) module.

Structure for boto3-stubs module.

- [mypy-boto3-builder](../../README.md#mypy_boto3_builder) / [Modules](../../MODULES.md#mypy-boto3-builder-modules) / [Mypy Boto3 Builder](../index.md#mypy-boto3-builder) / [Structures](index.md#structures) / Boto3StubsPackage
    - [Boto3StubsPackage](#boto3stubspackage)
        - [Boto3StubsPackage().essential_service_names](#boto3stubspackageessential_service_names)
        - [Boto3StubsPackage().get_all_names](#boto3stubspackageget_all_names)
        - [Boto3StubsPackage().get_init_required_import_records](#boto3stubspackageget_init_required_import_records)
        - [Boto3StubsPackage().get_session_required_import_records](#boto3stubspackageget_session_required_import_records)

## Boto3StubsPackage

[[find in source code]](https://github.com/vemel/mypy_boto3_builder/blob/master/mypy_boto3_builder/structures/boto3_stubs_package.py#L17)

```python
class Boto3StubsPackage(Package):
    def __init__(
        name: str = BOTO3_STUBS_NAME,
        pypi_name: str = BOTO3_STUBS_NAME,
        session_class: Optional[ClassRecord] = None,
        service_names: Iterable[ServiceName] = tuple(),
        service_packages: Iterable[ServicePackage] = tuple(),
        init_functions: Iterable[Function] = tuple(),
    ):
```

Structure for boto3-stubs module.

#### See also

- [BOTO3_STUBS_NAME](../constants.md#boto3_stubs_name)
- [Package](package.md#package)

### Boto3StubsPackage().essential_service_names

[[find in source code]](https://github.com/vemel/mypy_boto3_builder/blob/master/mypy_boto3_builder/structures/boto3_stubs_package.py#L37)

```python
@property
def essential_service_names() -> List[ServiceName]:
```

Service names marked as essential.

### Boto3StubsPackage().get_all_names

[[find in source code]](https://github.com/vemel/mypy_boto3_builder/blob/master/mypy_boto3_builder/structures/boto3_stubs_package.py#L106)

```python
def get_all_names() -> List[str]:
```

Get names for `__all__` directive.

### Boto3StubsPackage().get_init_required_import_records

[[find in source code]](https://github.com/vemel/mypy_boto3_builder/blob/master/mypy_boto3_builder/structures/boto3_stubs_package.py#L48)

```python
def get_init_required_import_records() -> List[ImportRecord]:
```

Get import records for `__init__.py[i]`.

### Boto3StubsPackage().get_session_required_import_records

[[find in source code]](https://github.com/vemel/mypy_boto3_builder/blob/master/mypy_boto3_builder/structures/boto3_stubs_package.py#L73)

```python
def get_session_required_import_records() -> List[ImportRecord]:
```

Get import reciords for `session.py[i]`.
