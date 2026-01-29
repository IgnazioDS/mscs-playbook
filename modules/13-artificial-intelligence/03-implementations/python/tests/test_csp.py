from src.ai.csp.csp import CSP
from src.ai.csp.ac3 import ac3
from src.ai.csp.backtracking import backtracking_search


def different(a, aval, b, bval):
    return aval != bval


def test_map_coloring_australia():
    variables = ["WA", "NT", "SA", "Q", "NSW", "V", "T"]
    domains = {v: ["red", "green", "blue"] for v in variables}
    neighbors = {
        "WA": ["NT", "SA"],
        "NT": ["WA", "SA", "Q"],
        "SA": ["WA", "NT", "Q", "NSW", "V"],
        "Q": ["NT", "SA", "NSW"],
        "NSW": ["SA", "Q", "V"],
        "V": ["SA", "NSW"],
        "T": [],
    }
    csp = CSP(variables, domains, neighbors, different)
    solution = backtracking_search(csp, use_ac3=True)
    assert solution is not None
    assert solution["WA"] != solution["NT"]
    assert solution["SA"] != solution["Q"]


def test_small_schedule_csp():
    variables = ["Task1", "Task2", "Task3"]
    domains = {"Task1": [1, 2], "Task2": [1, 2], "Task3": [2, 3]}
    neighbors = {"Task1": ["Task2"], "Task2": ["Task1", "Task3"], "Task3": ["Task2"]}

    def constraint(a, aval, b, bval):
        if a == "Task2" and b == "Task3":
            return aval < bval
        if a == "Task3" and b == "Task2":
            return bval < aval
        return aval != bval

    csp = CSP(variables, domains, neighbors, constraint)
    solution = backtracking_search(csp, use_ac3=True)
    assert solution is not None
    assert solution["Task2"] < solution["Task3"]


def test_ac3_prunes_domain():
    variables = ["X", "Y"]
    domains = {"X": [1, 2], "Y": [1]}
    neighbors = {"X": ["Y"], "Y": ["X"]}
    csp = CSP(variables, domains, neighbors, different)
    result = ac3(csp)
    assert result is True
    assert csp.domains["X"] == [2]
