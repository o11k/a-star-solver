from typing import Generator, Iterable, NamedTuple, Protocol
import enum

from .core import solve
from .games.nuts_and_pegs import NutGame, NutState


class C(enum.IntEnum):
    RED = enum.auto()
    YELLOW = enum.auto()
    GREEN = enum.auto()
    PINK = enum.auto()
    PURPLE = enum.auto()
    ORANGE = enum.auto()
    ICE = enum.auto()
    BLUE = enum.auto()
    LIGHT_BLUE = enum.auto()

def main():
    initial_state = NutState(
        peg_size=4,
        pegs=(
            (C.YELLOW ,C.LIGHT_BLUE ,C.YELLOW    ,C.RED),
            (C.PURPLE ,C.RED        ,C.GREEN     ,C.ICE),
            (C.BLUE   ,C.LIGHT_BLUE ,C.BLUE      ,C.LIGHT_BLUE),
            (C.ORANGE ,C.PINK       ,C.GREEN     ,C.PINK),
            (C.GREEN  ,C.ORANGE     ,C.ICE       ,C.PURPLE),
            (C.PURPLE ,C.RED        ,C.GREEN     ,C.BLUE),
            (C.YELLOW ,C.PINK       ,C.BLUE      ,C.PINK),
            (C.YELLOW ,C.ICE        ,C.LIGHT_BLUE,C.RED),
            (C.ORANGE ,C.ORANGE     ,C.PURPLE    ,C.ICE),
            (),
            (),
        )
    )
    sol = solve(NutGame, initial_state)
    if sol is None:
        print("No solution")
        return 1

    for step in sol:
        for peg in step.pegs:
            if peg:
                print(*peg, sep=",")
        print()


if __name__ == "__main__":
    main()
