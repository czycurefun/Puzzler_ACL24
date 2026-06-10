from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List
from xml.etree import ElementTree as ET
from zipfile import ZipFile


NS = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def _read_shared_strings(workbook: ZipFile) -> List[str]:
    try:
        root = ET.fromstring(workbook.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    values = []
    for item in root.findall("x:si", NS):
        texts = [node.text or "" for node in item.findall(".//x:t", NS)]
        values.append("".join(texts))
    return values


def _column_name(cell_ref: str) -> str:
    return re.sub(r"\d+", "", cell_ref)


def read_xlsx_sheet(path: str, sheet_xml: str = "xl/worksheets/sheet1.xml") -> List[Dict[str, Any]]:
    """Read a simple xlsx sheet as list of dicts using only the standard library."""
    workbook_path = Path(path)
    with ZipFile(workbook_path) as workbook:
        shared_strings = _read_shared_strings(workbook)
        root = ET.fromstring(workbook.read(sheet_xml))

    rows = []
    for row in root.findall(".//x:sheetData/x:row", NS):
        values: Dict[str, Any] = {}
        for cell in row.findall("x:c", NS):
            ref = cell.attrib.get("r", "")
            column = _column_name(ref)
            value_node = cell.find("x:v", NS)
            if value_node is None:
                value = ""
            elif cell.attrib.get("t") == "s":
                value = shared_strings[int(value_node.text or "0")]
            else:
                raw = value_node.text or ""
                try:
                    value = int(raw)
                except ValueError:
                    try:
                        value = float(raw)
                    except ValueError:
                        value = raw
            values[column] = value
        rows.append(values)

    if not rows:
        return []

    header_row = rows[0]
    headers = {column: str(value).strip() for column, value in header_row.items()}
    records = []
    for row in rows[1:]:
        record = {}
        for column, header in headers.items():
            if header:
                record[header] = row.get(column, "")
        records.append(record)
    return records
