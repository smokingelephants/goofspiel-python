import math
from typing import Callable, List, Tuple

import attr


# TODO: Bid and Card should kinda match...
Bid = int
# TODO: Consider making this a strong type
Card = int

BreedFunction = Callable[
    ["BotPlayer", "BotPlayer", "GameConfig", float, float], "BotPlayer"
]
MutationFunction = Callable[["BotPlayer", "GameConfig"], "BotPlayer"]


class Score(object):
    """Represented as a mixed number."""

    def __init__(self, whole: int, num: int = 0, den: int = 1):
        self.whole = whole
        self.num = num
        self.den = den
        self.reduce()

    def as_str(self) -> str:
        frac = ""
        if self.num:
            frac = f" {self.num}/{self.den}"
        points = "points"
        if 1 == self.value():
            points = "point"
        return f"{self.whole}{frac} {points}"

    def value(self) -> float:
        """Used for sorting and stuff"""
        return self.whole + (self.num / self.den)

    def reduce(self) -> None:
        if self.num < 0:
            self.num *= -1
            self.whole *= -1
        if self.den < 0:
            self.den *= -1
            self.whole *= -1

        while self.num >= self.den:
            self.num -= self.den
            self.whole += 1 if self.whole >= 0 else -1

        self.num //= math.gcd(self.num, self.den)
        self.den //= math.gcd(self.num, self.den)

        self._validate()

    def inc(self, other: "Score") -> "Score":
        self.whole += other.whole
        self.num = self.num * other.den + other.num * self.den
        self.den = self.den * other.den
        self.reduce()
        return self

    def _validate(self) -> None:
        assert isinstance(self.whole, int)
        assert isinstance(self.num, int)
        assert isinstance(self.den, int)
        assert self.num >= 0
        assert self.den > 0


Scorer = Callable[[Card, List[Tuple["Player", Bid]]], List[Tuple["Player", Score]]]


# TOOD: Move to another file
class GoofErrors(Exception):
    """Any error that's specific to this program's code."""

    pass
