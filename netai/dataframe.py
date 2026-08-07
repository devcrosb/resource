from collections.abc import Mapping
from typing import Any

import pandas as pd


def UnpackPD(
	data: Mapping[Any, Any],
	columns: list[str],
) -> pd.DataFrame:
	"""
	Convert a nested dictionary into a pandas DataFrame.

	Dictionary keys become values in the grouping columns. The dictionary is
	unpacked only to the depth specified by `columns`.

	The value assigned to the final column is preserved exactly as-is. If it
	contains additional dictionaries, lists, or other child elements, they are
	not flattened or modified.

	Example:
		data = {
			"group_a": {
				"item_1": {"status": "active", "values": [1, 2, 3]},
				"item_2": {"status": "inactive", "values": [4, 5]},
			},
			"group_b": {
				"item_3": {"status": "active", "values": [6]},
			},
		}

		columns = ["group", "item", "value"]

		Result:
			  group    item                                      value
		0   group_a  item_1  {"status": "active", "values": [1, 2, 3]}
		1   group_a  item_2     {"status": "inactive", "values": [4, 5]}
		2   group_b  item_3          {"status": "active", "values": [6]}

	Args:
		data:
			Nested dictionary whose keys represent grouping values.
		columns:
			Output column names. All columns except the final column represent
			dictionary-key levels. The final column contains the untouched
			value found at that depth.

	Returns:
		A pandas DataFrame with the specified columns.

	Raises:
		ValueError:
			If no columns are supplied, or if a non-dictionary value is
			encountered before the requested unpacking depth is reached.
		TypeError:
			If `data` is not a mapping.
	"""
	if not isinstance(data, Mapping):
		raise TypeError("data must be a dictionary or other mapping")

	if not columns:
		raise ValueError("columns must contain at least one column name")

	if len(set(columns)) != len(columns):
		raise ValueError("column names must be unique")

	rows: list[dict[str, Any]] = []
	grouping_depth = len(columns) - 1

	def unpack(
		value: Any,
		depth: int,
		row_values: list[Any],
	) -> None:
		# The requested depth has been reached. Preserve the remaining value.
		if depth == grouping_depth:
			rows.append(dict(zip(columns, [*row_values, value])))
			return

		if not isinstance(value, Mapping):
			path = " -> ".join(map(str, row_values)) or "<root>"
			raise ValueError(
				f"Expected a dictionary at depth {depth} beneath {path}, "
				f"but found {type(value).__name__}"
			)

		for key, child_value in value.items():
			unpack(
				value=child_value,
				depth=depth + 1,
				row_values=[*row_values, key],
			)

	unpack(data, depth=0, row_values=[])

	return pd.DataFrame(rows, columns=columns)


def UnpackDF(data,columns):

	rows: list[dict[str, Any]] = []
	grouping_depth = len(columns) - 1

	def unpack(
		value: Any,
		depth: int,
		row_values: list[Any],
	) -> None:
		# The requested depth has been reached. Preserve the remaining value.
		if depth == grouping_depth:
			rows.append(dict(zip(columns, [*row_values, value])))
			return

		if not isinstance(value, Mapping):
			path = " -> ".join(map(str, row_values)) or "<root>"
			raise ValueError(
				f"Expected a dictionary at depth {depth} beneath {path}, "
				f"but found {type(value).__name__}"
			)

		for key, child_value in value.items():
			unpack(
				value=child_value,
				depth=depth + 1,
				row_values=[*row_values, key],
			)

	unpack(data, depth=0, row_values=[])

	return Rows_to_DF(rows,columns)

def Rows_to_DF(rows,cols):

	data = []
	for row in rows:
		rec = SetRec(row,cols)
		if isRecord(rec):
			data.append(rec)

	return data

def SetRec(row,cols):

	rec = {}

	for n in range(0,len(cols)):
		key = cols[n]
		try: val = row[n]
		except: val = None

		rec[key] = val

	return rec

def isRecord(rec):

	if not (rec and isinstance(rec,dict)):
		return False

	for key,val in rec.items():
		if Value(val):
			return True

def Value(value):

	val = str(value).lower().strip()

	if len(val) == 0:
		return 

	if val in {"none","null","nill","0","{}","[]","()"}:
		return 

	if isSemantic(val):
		return value


def isSemantic(value):

	for val in str(value):
		if val.isalnum():
			return True

	return False

