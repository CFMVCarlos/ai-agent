"""Output formatting helpers for JSON calculation results."""

# calculator/pkg/render.py

import json


def format_json_output(expression: str, result: float, indent: int = 2) -> str:
    """Format an expression and its calculated result as a JSON string.

    Parameters
    ----------
    expression : str
        The mathematical expression evaluated.
    result : float
        The numerical result of the expression.
    indent : int, default=2
        JSON indentation spaces.

    Returns
    -------
    str
        Indented JSON string with expression and integer/float result.
    """
    if isinstance(result, float) and result.is_integer():
        result_to_dump = int(result)
    else:
        result_to_dump = result

    output_data = {
        "expression": expression,
        "result": result_to_dump,
    }
    return json.dumps(output_data, indent=indent)
