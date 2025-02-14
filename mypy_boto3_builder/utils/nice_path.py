"""
Path that represents it as relative to workdir.
"""
from pathlib import Path
from typing import Iterable, Iterator


class NicePath(type(Path())):  # type: ignore
    """
    Path that represents it as relative to workdir.
    """

    def __str__(self) -> str:
        path = Path(self)
        if self.is_absolute():
            cwd = self.cwd()
            if path == cwd or path.parts <= cwd.parts:
                return str(path)

            try:
                path = Path(self).relative_to(cwd)
            except ValueError:
                return str(path)

        if len(path.parts) == 1:
            return f"./{path}"

        return str(path)

    def walk(self, exclude: Iterable[Path] = tuple()) -> Iterator[Path]:
        """
        Walk files except for `exclude`.

        Yields:
            Existing Path.
        """
        exclude_strs = {NicePath(i).as_posix() for i in exclude}
        for path in self.glob("**/*"):
            if not path.is_file():
                continue

            if path.as_posix() in exclude_strs:
                continue

            yield path
