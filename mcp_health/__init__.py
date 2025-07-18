"""MCP-Health: AI Productivity Analysis for Medical Fees in Japan

A Python package for analyzing the economic impact of AI implementation
in Japan's healthcare system, focusing on administrative efficiency and
clinical productivity improvements.
"""

__version__ = "0.1.0"
__author__ = "Tatsuru Kikuchi"
__email__ = "tatsuru.kikuchi@example.com"
__description__ = "AI Productivity Analysis for Medical Fees in Japan"

from .core.data_analysis import HealthcareProductivityAnalyzer
from .core.data_generator import HealthcareDataGenerator
from .core.visualization import HealthcareVisualizer

__all__ = [
    "HealthcareProductivityAnalyzer",
    "HealthcareDataGenerator", 
    "HealthcareVisualizer"
]