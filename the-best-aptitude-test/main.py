def read_nums() -> list[float]:
    return [float(x) for x in input().split()]


def cc(x: list[float], y: list[float]) -> float:
    """Compute the Pearson correlation coefficient between two lists of numbers."""
    n = len(x)
    sum_x, sum_y = sum(x), sum(y)
    sum_x_sq, sum_y_sq = sum([i**2 for i in x]), sum([i**2 for i in y])
    sum_xy = sum([i * j for i, j in zip(x, y, strict=True)])
    numerator = n * sum_xy - sum_x * sum_y
    denominator = ((n * sum_x_sq - sum_x**2) * (n * sum_y_sq - sum_y**2)) ** 0.5
    if denominator == 0:
        return 0
    return numerator / denominator


def solve() -> None:
    input()  # Skip N: the number of students
    averages = read_nums()
    ccs = [cc(averages, read_nums()) for _ in range(5)]
    print(ccs.index(max(ccs)) + 1)


for _ in range(int(input())):
    solve()
