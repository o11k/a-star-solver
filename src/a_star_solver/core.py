from typing import Iterable, Protocol


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
