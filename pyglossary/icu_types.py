import typing
from typing import AnyStr, Callable


class T_Locale(typing.Protocol):
	def __init__(self: "typing.Self", _id: str) -> None:
		pass

	def getName(self: "typing.Self") -> str:
		pass


class T_Collator(typing.Protocol):
	PRIMARY: int = 0
	SECONDARY: int = 1
	TERTIARY: int = 2
	QUATERNARY: int = 3
	IDENTICAL: int = 15

	@classmethod
	def createInstance(loc: "T_Locale | None" = None) -> "T_Collator":
		pass

	@property
	def getSortKey(self: "typing.Self") -> Callable[[AnyStr], bytes]:
		pass

	def setStrength(self: "typing.Self", strength: int) -> None:
		pass

	def setAttribute(self: "typing.Self", attr: int, value: int) -> None:
		pass


class T_UCollAttribute(typing.Protocol):
	ALTERNATE_HANDLING: int = 1
	CASE_FIRST: int = 2
	CASE_LEVEL: int = 3
	DECOMPOSITION_MODE: int = 4
	FRENCH_COLLATION: int = 0
	HIRAGANA_QUATERNARY_MODE: int = 6
	NORMALIZATION_MODE: int = 4
	NUMERIC_COLLATION: int = 7
	STRENGTH: int = 5


class T_UCollAttributeValue(typing.Protocol):
	DEFAULT: int = -1
	DEFAULT_STRENGTH: int = 2
	IDENTICAL: int = 15
	LOWER_FIRST: int = 24
	NON_IGNORABLE: int = 21
	OFF: int = 16
	ON: int = 17
	PRIMARY: int = 0
	QUATERNARY: int = 3
	SECONDARY: int = 1
	SHIFTED: int = 20
	TERTIARY: int = 2
	UPPER_FIRST: int = 25

