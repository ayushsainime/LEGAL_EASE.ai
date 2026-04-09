from __future__ import annotations

from dataclasses import dataclass

from sympy import Equality, simplify, solveset
from sympy.core.relational import Relational
from sympy.parsing.latex import parse_latex


@dataclass
class MathAnalysis:
    problem_type: str
    structure_summary: str
    verification_summary: str
    normalized_expression: str


def classify_problem_type(latex_text: str, parsed_expr) -> str:
    """Classify the rough math topic with cheap rules."""
    latex_lower = latex_text.lower()

    if "\\int" in latex_lower or "\\frac{d" in latex_lower:
        return "Calculus"
    if "\\sin" in latex_lower or "\\cos" in latex_lower or "\\tan" in latex_lower:
        return "Trigonometry"
    if "\\begin{matrix}" in latex_lower or "\\begin{bmatrix}" in latex_lower:
        return "Linear Algebra"
    if isinstance(parsed_expr, Relational):
        return "Equation Solving"
    if parsed_expr.free_symbols:
        return "Algebra"
    return "Arithmetic"


def summarize_structure(parsed_expr) -> str:
    """Describe the structure of the parsed math expression."""
    symbols = sorted(str(symbol) for symbol in parsed_expr.free_symbols)
    symbol_text = ", ".join(symbols) if symbols else "none"
    root_type = type(parsed_expr).__name__

    if isinstance(parsed_expr, Equality):
        return (
            f"Structured as an equation with root node {root_type}. "
            f"Variables detected: {symbol_text}."
        )

    return (
        f"Structured as an expression with root node {root_type}. "
        f"Variables detected: {symbol_text}."
    )


def verify_expression(parsed_expr) -> tuple[str, str]:
    """Provide a basic symbolic verification summary."""
    if isinstance(parsed_expr, Equality):
        difference = simplify(parsed_expr.lhs - parsed_expr.rhs)

        if difference == 0:
            return (
                "This equation simplifies to a true identity, so the equality is mathematically correct.",
                str(parsed_expr.lhs),
            )

        symbols = list(parsed_expr.free_symbols)
        if len(symbols) == 1:
            solutions = solveset(parsed_expr.lhs - parsed_expr.rhs, symbols[0])
            return (
                "This is not an identity yet. It looks like an equation to solve, "
                f"and SymPy finds solutions {solutions}.",
                str(parsed_expr.lhs - parsed_expr.rhs),
            )

        return (
            "This equality does not simplify to a proven identity, so it should be treated as a relation to analyze further.",
            str(difference),
        )

    simplified = simplify(parsed_expr)
    return (
        f"This expression simplifies to {simplified}.",
        str(simplified),
    )


def analyze_math_expression(latex_text: str) -> MathAnalysis:
    """Parse LaTeX into SymPy and return a lightweight analysis."""
    try:
        parsed_expr = parse_latex(latex_text)
    except Exception as error:
        raise RuntimeError(f"Math parsing failed: {error}") from error

    problem_type = classify_problem_type(latex_text, parsed_expr)
    structure_summary = summarize_structure(parsed_expr)
    verification_summary, normalized_expression = verify_expression(parsed_expr)

    return MathAnalysis(
        problem_type=problem_type,
        structure_summary=structure_summary,
        verification_summary=verification_summary,
        normalized_expression=normalized_expression,
    )
