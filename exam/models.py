"""Plain data types for the exam bank."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable

# re.ASCII keeps \b, \w and \d behaving like JavaScript regexes on Tamil/Tanglish text.
_BASE_FLAGS = re.IGNORECASE | re.ASCII


@dataclass(frozen=True)
class Criterion:
    label: str
    pattern: re.Pattern
    pts: float = 0.0          # fixed criterion: points if the pattern matches
    count: bool = False       # count criterion: `each` points per match, up to `cap`
    each: float = 0.0
    cap: int = 0
    distinct: bool = False


def c(label: str, pts: float, pattern: str, multiline: bool = False) -> Criterion:
    flags = _BASE_FLAGS | (re.MULTILINE if multiline else 0)
    return Criterion(label, re.compile(pattern, flags), pts=pts)


def k(label: str, pattern: str, each: float, cap: int, distinct: bool = False) -> Criterion:
    return Criterion(label, re.compile(pattern, _BASE_FLAGS), count=True, each=each, cap=cap, distinct=distinct)


@dataclass(frozen=True)
class Section:
    id: str
    level: int
    name: str
    sub: str
    marks: int


@dataclass(frozen=True)
class Question:
    n: int
    sec: str
    marks: int
    type: str                 # 'mcq' | 'text' | 'prompt' | 'keywords'
    q: str
    opts: list[str] = field(default_factory=list)
    ans: int | None = None
    min_words: int = 0
    quote: str = ""
    hint: str = ""
    rubric: list[Criterion] = field(default_factory=list)


@dataclass(frozen=True)
class Level:
    xp: int
    name: str


@dataclass(frozen=True)
class Badge:
    id: str
    name: str
    desc: str
    test: Callable[[dict], bool]


@dataclass(frozen=True)
class Roast:
    max: int
    tag: str
    lines: list[str]
