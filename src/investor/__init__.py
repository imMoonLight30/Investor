"""Investor: tools for stock research inspired by Benjamin Graham's
"The Intelligent Investor".

The package helps a defensive investor manage stock research through
analysis that favors safety of principal and an adequate, rather than
speculative, return.
"""

from .models import Stock
from .analysis import CriterionResult, analyze

__all__ = ["Stock", "CriterionResult", "analyze"]

__version__ = "0.1.0"
