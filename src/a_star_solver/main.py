from typing import Generator, Iterable, NamedTuple, Protocol
import enum

class Game[State](Protocol):
    @staticmethod
    def get_heuristic(state: State) -> int:
        ...

    @staticmethod
    def get_successors(state: State) -> Iterable[State]:
        ...

    @staticmethod
    def is_goal(state: State) -> bool:
        ...




def solve[State](game: Game[State], initial_state: State) -> list[State] | None:
    # Solve using A* search
    import heapq

    # Priority queue: (f_score, counter, state)
    # Counter breaks ties for deterministic ordering
    counter = 0
    open_set = [(game.get_heuristic(initial_state), counter, initial_state)]
    counter += 1

    # Track visited states
    visited = set()

    # Track g_score (cost from start) for each state
    g_score = {hash(initial_state): 0}

    # Track parent pointers for path reconstruction
    parent: dict[int, State | None] = {hash(initial_state): None}

    while open_set:
        _, _, current = heapq.heappop(open_set)

        # Check if we've reached the goal
        if game.is_goal(current):
            # Reconstruct path
            path = []
            while current is not None:
                path.append(current)
                current = parent.get(hash(current))
            return list(reversed(path))

        state_id = hash(current)
        if state_id in visited:
            continue

        visited.add(state_id)

        # Explore successors
        for successor in game.get_successors(current):
            successor_id = hash(successor)

            if successor_id not in visited:
                tentative_g = g_score[state_id] + 1

                if successor_id not in g_score or tentative_g < g_score[successor_id]:
                    g_score[successor_id] = tentative_g
                    parent[successor_id] = current
                    f_score = tentative_g + game.get_heuristic(successor)
                    heapq.heappush(open_set, (f_score, counter, successor))
                    counter += 1

    return None


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
    import pprint
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
