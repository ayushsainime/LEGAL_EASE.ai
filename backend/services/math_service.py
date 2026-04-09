from __future__ import annotations

from dataclasses import dataclass
import re

from sympy import Equality, simplify, solveset
from sympy.core.relational import Relational
from sympy.parsing.latex import parse_latex


@dataclass
class MathAnalysis:
    problem_type: str
    structure_summary: str
    verification_summary: str
    normalized_expression: str


def _flatten_array_blocks(latex_text: str) -> str:
    """Convert LaTeX array blocks into plain line-separated text."""
    text = re.sub(r"\\begin\{array\}\{[^}]*\}", "", latex_text)
    text = text.replace(r"\end{array}", "")
    text = text.replace(r"\\", "\n")
    text = text.replace("&", " ")
    return text


def _strip_text_macros(latex_text: str) -> str:
    """Remove noisy text wrappers that OCR often injects."""
    text = latex_text
    text = re.sub(r"\\left\s*[\|\(\[\{]", "", text)
    text = re.sub(r"\\right\s*[\|\)\]\}]", "", text)
    text = text.replace(r"\displaystyle", "")
    text = re.sub(r"\\operatorname\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\mathrm\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\mathbf\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"[^a-zA-Z0-9\\+\-*/^_=().{}\[\] \n]", " ", text)
    text = text.replace("~", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _extract_best_equation_candidate(latex_text: str) -> str:
    """Pick the line most likely to contain the usable equation."""
    flattened = _flatten_array_blocks(latex_text)
    raw_lines = [line for line in flattened.splitlines() if line.strip()]
    cleaned_lines = [_strip_text_macros(line).strip(" {}") for line in raw_lines]
    lines = [line for line in cleaned_lines if line]
    equation_lines = [line for line in lines if "=" in line]
    if equation_lines:
        return equation_lines[0]
    if lines:
        return lines[0]
    return _strip_text_macros(flattened)


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
    """Parse LaTeX into SymPy and return a lightweight analysis.

    If raw OCR output is too noisy, try cleaned candidates before giving up.
    """
    candidates = [
        latex_text,
        _extract_best_equation_candidate(latex_text),
        _strip_text_macros(latex_text),
    ]

    parsed_expr = None
    selected_candidate = latex_text
    for candidate in candidates:
        if not candidate or candidate.isspace():
            continue
        try:
            parsed_expr = parse_latex(candidate)
            selected_candidate = candidate
            break
        except Exception:
            pass

    if parsed_expr is None:
        return MathAnalysis(
            problem_type="Needs Cleaner Image",
            structure_summary=(
                "The OCR output included too much non-math text, so symbolic parsing could not run."
            ),
            verification_summary=(
                "No symbolic verification was possible yet. Try cropping tightly around the equation."
            ),
            normalized_expression=selected_candidate,
        )

    problem_type = classify_problem_type(selected_candidate, parsed_expr)
    structure_summary = summarize_structure(parsed_expr)
    verification_summary, normalized_expression = verify_expression(parsed_expr)

    return MathAnalysis(
        problem_type=problem_type,
        structure_summary=structure_summary,
        verification_summary=verification_summary,
        normalized_expression=normalized_expression,
    )
