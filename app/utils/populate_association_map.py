from typing import Sequence

from sqlalchemy import Row


def populate_association_map(
        results: Sequence[Row[tuple[int, int]]],
        target_map: dict[int, list[int]],
        key_idx: int = 0,
        val_idx: int = 1
) -> dict[int, list[int]]:
    for row in results:
        key = row[key_idx]
        val = row[val_idx]
        if key in target_map:
            target_map[key].append(val)
    return target_map