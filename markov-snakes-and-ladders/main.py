import random

GAMES = 5000


class Board:
    def __init__(self):
        """
        Initialize the board with the probabilities of each face of the dice and the ladders.
        """
        self.__read_next_config()

    def simulate(self) -> int:
        """
        Simulate a game of snakes and ladders.
        Returns the number of rolls it took to reach the 100th square.
        If the game takes more than 1000 rolls, return 0.
        """
        pos = 1
        for i in range(1000):
            pos = self._next_pos(pos)
            if pos == 100:
                return i + 1
        return 0

    def simulate_n_games(self, n: int) -> float:
        """
        Simulate n games of snakes and ladders.
        Returns the average number of rolls it took to reach the 100th square.
        """
        total = 0
        for _ in range(n):
            rolls = self.simulate()
            if rolls == 0:
                continue  # ignore games that take more than 1000 rolls
            total += rolls
        return total / n

    def __read_next_config(self):
        """
        Read the next configuration of the board from the input.
        """
        self.probs = list(map(float, input().split(",")))
        input()  # skip this line
        self.ladders = Board.__read_pairs() | Board.__read_pairs()

    @staticmethod
    def __read_pairs() -> dict[int, int]:
        """
        Read pairs of integers from the input and return them as a dictionary.
        """
        pairs_dict = {}
        str_pairs = input().split()
        for pair in str_pairs:
            key, value = map(int, pair.split(","))
            pairs_dict[key] = value
        return pairs_dict

    def _next_pos(self, cur_pos: int) -> int:
        """
        Get the next position on the board after rolling the dice.
        Returns the same position if the next position is greater than 100.
        - cur_pos: the current position on the board.
        """
        face = random.choices(range(1, 7), weights=self.probs)[0]
        pos = cur_pos + face
        if pos > 100:
            return cur_pos
        if pos in self.ladders:
            return self.ladders[pos]
        return pos


if __name__ == "__main__":
    T = int(input())
    for _ in range(T):
        board = Board()
        average_rolls = board.simulate_n_games(GAMES)
        print(round(average_rolls))
