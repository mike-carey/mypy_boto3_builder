# Strings

> Auto-generated documentation for [mypy_boto3_builder.utils.strings](https://github.com/vemel/mypy_boto3_builder/blob/master/mypy_boto3_builder/utils/strings.py) module.

Multiple string utils collection.

- [mypy-boto3-builder](../../README.md#mypy_boto3_builder) / [Modules](../../MODULES.md#mypy-boto3-builder-modules) / [Mypy Boto3 Builder](../index.md#mypy-boto3-builder) / [Utils](index.md#utils) / Strings
    - [get_anchor_link](#get_anchor_link)
    - [get_botocore_class_name](#get_botocore_class_name)
    - [get_class_prefix](#get_class_prefix)
    - [get_line_with_indented](#get_line_with_indented)
    - [get_min_build_version](#get_min_build_version)
    - [get_short_docstring](#get_short_docstring)
    - [is_reserved](#is_reserved)

## get_anchor_link

[[find in source code]](https://github.com/vemel/mypy_boto3_builder/blob/master/mypy_boto3_builder/utils/strings.py#L96)

```python
def get_anchor_link(text: str) -> str:
```

Convert header to markdown anchor link.

## get_botocore_class_name

[[find in source code]](https://github.com/vemel/mypy_boto3_builder/blob/master/mypy_boto3_builder/utils/strings.py#L147)

```python
def get_botocore_class_name(metadata: Dict[(str, str)]) -> str:
```

Get Botocore class name from Service metadata.

## get_class_prefix

[[find in source code]](https://github.com/vemel/mypy_boto3_builder/blob/master/mypy_boto3_builder/utils/strings.py#L23)

```python
def get_class_prefix(func_name: str) -> str:
```

Get a valid Python class prefix from `func_name`.

#### Arguments

- `func_name` - Any string.

#### Returns

String with a class prefix.

## get_line_with_indented

[[find in source code]](https://github.com/vemel/mypy_boto3_builder/blob/master/mypy_boto3_builder/utils/strings.py#L37)

```python
def get_line_with_indented(
    input_string: str,
    multi_first_line: bool = False,
) -> str:
```

Get first line of the string with all indented lines.

Fixes invalid unindent.

#### Arguments

- `input_string` - Input string.

#### Returns

A string with first line and following indented lines.

## get_min_build_version

[[find in source code]](https://github.com/vemel/mypy_boto3_builder/blob/master/mypy_boto3_builder/utils/strings.py#L157)

```python
def get_min_build_version(version: str) -> str:
```

Get min version 5 micro releases lower that `version`.

Minimum micro is 0.

## get_short_docstring

[[find in source code]](https://github.com/vemel/mypy_boto3_builder/blob/master/mypy_boto3_builder/utils/strings.py#L110)

```python
def get_short_docstring(doc: str) -> str:
```

Create a short docstring from boto3 documentation.

Trims docstring to 300 chars.
Removes double and trible backticks.
Ensures that backticks are closed.
Wraps docstring to 80 chars.

## is_reserved

[[find in source code]](https://github.com/vemel/mypy_boto3_builder/blob/master/mypy_boto3_builder/utils/strings.py#L103)

```python
def is_reserved(word: str) -> bool:
```

Check whether varialbe name conflicts with Python reserved names.
