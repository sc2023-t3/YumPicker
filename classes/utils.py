from typing import Any


class _MissingSentinel:
    def __eq__(self, other: Any) -> bool:
        return False

    def __hash__(self) -> int:
        return 0

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "..."


MISSING: Any = _MissingSentinel()
