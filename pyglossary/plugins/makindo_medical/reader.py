# -*- coding: utf-8 -*-
from __future__ import annotations

import html
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	import sqlite3
	from collections.abc import Iterator

	from pyglossary.glossary_types import EntryType, ReaderGlossaryType

__all__ = ["Reader"]


class Reader:
	useByteProgress = False

	def __init__(self, glos: ReaderGlossaryType) -> None:
		self._glos = glos
		self._clear()

	def _clear(self) -> None:
		self._filename = ""
		self._con: sqlite3.Connection | None = None
		self._cur: sqlite3.Cursor | None = None

	def open(self, filename: str) -> None:
		from sqlite3 import connect

		self._filename = filename
		self._con = connect(filename)
		self._cur = self._con.cursor()
		self._glos.setDefaultDefiFormat("h")

	def __len__(self) -> int:
		if self._cur is None:
			raise ValueError("cur is None")
		self._cur.execute("select count(*) from NEW_TABLE")
		return self._cur.fetchone()[0]

	def __iter__(self) -> Iterator[EntryType]:
		if self._cur is None:
			raise ValueError("cur is None")
		self._cur.execute(
			"select _id, contents from NEW_TABLE where _id is not null",
		)
		# FIXME: iteration over self._cur stops after one entry
		# and self._cur.fetchone() returns None
		# for row in self._cur:
		for row in self._cur.fetchall():
			word = html.unescape(row[0])
			definition = row[1].decode("utf-8", errors="ignore")
			# print(f"{word!r}, {definition!r}")
			yield self._glos.newEntry(word, definition, defiFormat="h")

	def close(self) -> None:
		if self._cur:
			self._cur.close()
		if self._con:
			self._con.close()
		self._clear()
