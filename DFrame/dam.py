"""A small NumPy-backed table for common dataset management tasks."""
"""DAM - Data Analysis Module
This module provides a lightweight DataFrame-like container for managing tabular data using NumPy arrays."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, cast

import numpy as np


class DFrame:
    """A lightweight, DataFrame-like container built on a two-dimensional array."""

    def __init__(
        self,
        data: Any = None,
        columns: Sequence[Any] | None = None,
        index: Sequence[Any] | None = None,
    ) -> None:
        default_columns: list[Any] | None
        default_index: list[Any] | np.ndarray


        if isinstance(data, DFrame):
            array = data.data.copy()
            default_columns = list(data.columns)
            default_index = data.index


        elif isinstance(data, Mapping):
            mapping = cast(Mapping[Any, Sequence[Any]], data)
            default_columns = list(mapping.keys())
            values = list(mapping.values())
            lengths = {len(value) for value in values}
            
            if lengths and len(lengths) != 1:
                raise ValueError("All columns must have the same length")
            
            array = np.empty((next(iter(lengths), 0), len(values)), dtype=object)

            for position, value in enumerate(values):
                array[:, position] = value
            default_index = np.arange(len(array))


        else:
            default_columns = None
            array = np.asarray([] if data is None else data)

            if array.ndim == 0:
                array = array.reshape(1, 1)

            elif array.ndim == 1:
                array = array.reshape((-1, 1))

            elif array.ndim != 2:
                raise ValueError("data must be one- or two-dimensional")
            
            default_index = np.arange(len(array))

        candidate_rows = cast(list[Any], data) if isinstance(data, list) else []

        if candidate_rows and all(isinstance(row, Mapping) for row in candidate_rows):
            rows = cast(list[Mapping[Any, Any]], candidate_rows)
            default_columns = list(dict.fromkeys(key for row in rows for key in row))
            array = np.array(
                [[row.get(key, np.nan) for key in default_columns] for row in rows],
                dtype=object,
            )

        self.data: np.ndarray = np.asarray(array)

        if self.data.ndim == 1:
            self.data = self.data.reshape((-1, 1))
        self.columns: list[Any] = (
            list(columns)

            if columns is not None
            
            else list(
                default_columns
                if default_columns is not None
                else range(self.data.shape[1])
            )
        )

        self.index = list(index) if index is not None else list(default_index)

        if len(self.columns) != self.data.shape[1]:
            raise ValueError("The number of columns must match the data")
        if len(self.index) != self.data.shape[0]:
            raise ValueError("The length of index must match the data")
        if len(set(self.columns)) != len(self.columns):
            raise ValueError("Column names must be unique")

    @property
    def shape(self) -> tuple[int, int]:
        return self.data.shape

    def __len__(self) -> int:
        return self.data.shape[0]

    def __repr__(self) -> str:
        return f"DFrame({len(self)} rows x {self.shape[1]} columns)\n{self.to_string()}"

    def __getitem__(self, key: Any) -> Any:
        if (
            key in self.columns
            if not isinstance(key, (slice, np.ndarray, list, tuple))
            else False
        ):
            return self.data[:, self.columns.index(key)]
        if isinstance(key, (list, tuple)):
            column_keys = list(cast(Sequence[Any], key))
            if all(item in self.columns for item in column_keys):
                return DFrame(
                    self.data[:, [self.columns.index(item) for item in column_keys]],
                    column_keys,
                    self.index,
                )
        selected = self.data[key]
        if selected.ndim == 1:
            return selected
        return DFrame(selected, self.columns, list(np.asarray(self.index)[key]))

    def head(self, n: int = 5) -> DFrame:
        return self[: max(0, n)]

    def tail(self, n: int = 5) -> DFrame:
        return self[-max(0, n) :] if n else self[:0]

    def select(self, columns: Sequence[Any]) -> DFrame:
        return self[list(columns)]

    def filter(self, condition: Any) -> DFrame:
        mask = np.asarray(
            condition(self) if callable(condition) else condition, dtype=bool
        )
        if mask.shape != (len(self),):
            raise ValueError("filter condition must contain one value per row")
        return DFrame(self.data[mask], self.columns, list(np.asarray(self.index)[mask]))

    def assign(self, **new_columns: Any) -> DFrame:
        result = self.data.copy()
        names = list(self.columns)
        for name, values in new_columns.items():
            values = values(self) if callable(values) else values
            values = np.asarray(values)
            if values.ndim == 0:
                values = np.repeat(values, len(self))
            if len(values) != len(self):
                raise ValueError(f"Column '{name}' must have one value per row")
            if name in names:
                result[:, names.index(name)] = values
            else:
                result = np.column_stack((result, values))
                names.append(name)
        return DFrame(result, names, self.index)

    def dropna(self) -> DFrame:
        mask = ~np.any(self._missing_mask(), axis=1)
        return DFrame(self.data[mask], self.columns, list(np.asarray(self.index)[mask]))

    def fillna(self, value: Any) -> DFrame:
        result = self.data.copy()
        result[self._missing_mask()] = value
        return DFrame(result, self.columns, self.index)

    def sort_values(self, by: Any, ascending: bool = True) -> DFrame:
        keys = [by] if isinstance(by, (str, int)) else list(by)
        positions = [self.columns.index(key) for key in keys]
        missing = np.any(self._missing_mask()[:, positions], axis=1)
        valid_positions = np.flatnonzero(~missing)
        sort_values: list[np.ndarray] = []
        for position in positions:
            values = self.data[valid_positions, position]
            try:
                values = values.astype(float)
            except (TypeError, ValueError):
                pass
            sort_values.append(values)
        valid_order = np.lexsort(tuple(sort_values[::-1]))
        if not ascending:
            valid_order = valid_order[::-1]
        order = np.concatenate((valid_positions[valid_order], np.flatnonzero(missing)))
        return DFrame(
            self.data[order], self.columns, list(np.asarray(self.index)[order])
        )

    def describe(self) -> dict[str, dict[str, float]]:
        summary: dict[str, dict[str, float]] = {}
        for position, name in enumerate(self.columns):
            values = self.data[:, position]
            try:
                numeric = values.astype(float)
            except (TypeError, ValueError):
                continue
            numeric = numeric[~np.isnan(numeric)]
            if len(numeric):
                summary[str(name)] = {
                    "count": float(len(numeric)),
                    "mean": float(np.mean(numeric)),
                    "min": float(np.min(numeric)),
                    "max": float(np.max(numeric)),
                }
        return summary

    def to_numpy(self, copy: bool = True) -> np.ndarray:
        return self.data.copy() if copy else self.data

    def to_dict(self) -> dict[Any, list[Any]]:
        return {
            name: self.data[:, position].tolist()
            for position, name in enumerate(self.columns)
        }

    def to_csv(self, path: str | Path, delimiter: str = ",") -> None:
        np.savetxt(
            path,
            self.data,
            delimiter=delimiter,
            fmt="%s",
            header=delimiter.join(map(str, self.columns)),
            comments="",
        )

    def to_string(self) -> str:
        rows = ["\t".join(map(str, self.columns))]
        rows.extend("\t".join(map(str, row)) for row in self.data)
        return "\n".join(rows)

    def _missing_mask(self) -> np.ndarray:
        none_mask = np.asarray(
            np.frompyfunc(lambda value: value is None, 1, 1)(self.data),
            dtype=bool,
        )
        try:
            return none_mask | np.isnan(self.data.astype(float))
        except (TypeError, ValueError):
            return none_mask
