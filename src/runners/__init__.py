"""Runners: adaptadores por proveedor para el experimento needle-in-haystack."""

from .base import Runner
from .mock_runner import MockRunner

__all__ = ["Runner", "MockRunner"]

# Los runners reales requieren librerías externas. Import condicional para que
# el repo se pueda usar con solo el MockRunner si no quieres claves API.
try:
    from .openai_runner import OpenAIRunner
    __all__.append("OpenAIRunner")
except ImportError:
    pass

try:
    from .anthropic_runner import AnthropicRunner
    __all__.append("AnthropicRunner")
except ImportError:
    pass
