# calculator/pkg/calculator.py

from collections.abc import Callable


class Calculator:
    """Infix arithmetic expression calculator with operator precedence."""

    def __init__(self) -> None:
        self.operators: dict[str, Callable[[float, float], float]] = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.precedence: dict[str, int] = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression: str) -> float | None:
        """Evaluate an infix arithmetic expression string.

        Parameters
        ----------
        expression : str
            The arithmetic expression to evaluate (e.g. '3 + 5 * 2').

        Returns
        -------
        float | None
            Calculated numeric result, or None if the expression is empty.
        """
        if not expression or expression.isspace():
            return None
        tokens = expression.strip().split()
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens: list[str]) -> float:
        """Evaluate a list of tokenized infix strings.

        Parameters
        ----------
        tokens : list[str]
            Tokens containing operands and operators.

        Returns
        -------
        float
            Final evaluated result.

        Raises
        ------
        ValueError
            If a token is invalid or the expression syntax is malformed.
        """
        values: list[float] = []
        operators: list[str] = []

        for token in tokens:
            if token in self.operators:
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            else:
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"invalid token: {token}")

        while operators:
            self._apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("invalid expression")

        return values[0]

    def _apply_operator(self, operators: list[str], values: list[float]) -> None:
        """Apply top operator from stack to operands and append result.

        Parameters
        ----------
        operators : list[str]
            Stack of operator tokens.
        values : list[float]
            Stack of numeric values.

        Raises
        ------
        ValueError
            If there are insufficient operands for the operator.
        """
        if not operators:
            return

        operator = operators.pop()
        if len(values) < 2:
            raise ValueError(f"not enough operands for operator {operator}")

        b = values.pop()
        a = values.pop()
        values.append(self.operators[operator](a, b))
