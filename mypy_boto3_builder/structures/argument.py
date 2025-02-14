"""
Method or function argument.
"""
from typing import Optional, Set, Type, TypeVar

from mypy_boto3_builder.type_annotations.fake_annotation import FakeAnnotation
from mypy_boto3_builder.type_annotations.type_constant import TypeConstant

_R = TypeVar("_R", bound="Argument")


class Argument:
    """
    Method or function argument.

    Arguments:
        name -- Argument name.
        type_annotation -- Argument type annotation.
        value -- Default argument value.
        prefix -- Used for starargs.
    """

    def __init__(
        self,
        name: str,
        type_annotation: Optional[FakeAnnotation],
        default: Optional[TypeConstant] = None,
        prefix: str = "",
    ):
        self.name: str = name
        self.type_annotation: Optional[FakeAnnotation] = type_annotation
        self.default: Optional[TypeConstant] = default
        self.prefix: str = prefix

    def render(self) -> str:
        """
        Render argument to a string.
        """
        if not self.type_annotation:
            return f"{self.name} = {self.default}"

        return f"{self.name}: {self.type_annotation.render()} = {self.default}"

    @classmethod
    def kwflag(cls: Type[_R]) -> _R:
        """
        Create `*` keywords separator.
        """
        return cls("*", None)

    def is_kwflag(self) -> bool:
        """
        Whether argument is a `*` keywords separator.
        """
        return self.name == "*"

    def get_types(self) -> Set[FakeAnnotation]:
        """
        Extract required type annotations.
        """
        types: Set[FakeAnnotation] = set()
        if self.type_annotation is not None:
            types.update(self.type_annotation.get_types())
        if self.default is not None:
            types.update(self.default.get_types())

        return types

    @property
    def required(self) -> bool:
        """
        Whether argument does not have a default value and is required.
        """
        return self.default is None
