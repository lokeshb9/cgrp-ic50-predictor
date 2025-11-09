"""
Views Module
============

Separate view components for each tab of the application.
Clean separation following MVC pattern.

Author: Dani Geiger
"""

from .predictor_view import PredictorView
from .resume_view import ResumeView
from .biography_view import BiographyView

__all__ = [
    "PredictorView",
    "ResumeView",
    "BiographyView",
]
