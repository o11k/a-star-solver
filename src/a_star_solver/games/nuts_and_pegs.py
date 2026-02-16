from typing import NamedTuple, Generator

from ..core import Game


class NutState(NamedTuple):
    peg_size: int
    pegs: tuple[tuple[int, ...], ...]

class NutGame(Game[NutState]):
    @staticmethod
    def is_goal(state: NutState) -> bool:
        # All pegs contain only one type of nut, and all pegs are of different nut-type
        for peg in state.pegs:
            if not peg:  # Empty peg
                continue

            if any(nut != peg[0] for nut in peg):
                return False

        first_nuts = [peg[0] for peg in state.pegs if peg]
        return len(first_nuts) == len(set(first_nuts))

    @staticmethod
    def get_heuristic(state: NutState) -> int:
        bad_nuts = 0

        for peg in state.pegs:
            if not peg:  # Empty peg
                continue

            for i in range(1,len(peg)):
                if peg[i] != peg[i-1]:
                    bad_nuts += 1

        first_nuts = [peg[0] for peg in state.pegs if peg]
        bad_nuts += len(first_nuts) - len(set(first_nuts))

        return bad_nuts

    @staticmethod
    def get_successors(state: NutState) -> Generator[NutState, None, None]:
        """
        This in the only way in which you can modify the state:
        1. pick a peg that's not empty
        2. pop the top nut and also all nuts directly below it that are the same as it
        3. pick another peg that is either empty, or where the top nut is the same as the ones we popped
        4. move the popped nuts to the new peg
        5. the move is valid if state.peg_size is not exceeded on the destination peg
        """
        for src_i,src_peg in enumerate(state.pegs):
            if not src_peg:
                continue

            nut_to_move = src_peg[-1]
            size = 0
            for nut in src_peg[::-1]:
                if nut != nut_to_move:
                    break
                size += 1

            for dst_i,dst_peg in enumerate(state.pegs):
                if dst_peg and dst_peg[-1] != nut_to_move:
                    continue
                if len(dst_peg) + size > state.peg_size:
                    continue

                # Create new state
                new_pegs = list(state.pegs)
                new_pegs[src_i] = src_peg[:-size]
                new_pegs[dst_i] = dst_peg + src_peg[-size:]
                yield NutState(state.peg_size, tuple(new_pegs))
