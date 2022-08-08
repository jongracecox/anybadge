from enum import Enum


# Define some templates that can be used for common badge types, saving
# from having to provide thresholds and labels each time.
class Style(Enum):
    """A style that can be used for common badge types."""

    PYLINT = ("default.svg", "2=red 4=orange 8=yellow 10=green", "pylint")
    COVERAGE = ("default.svg", "50=red 60=orange 80=yellow 100=green", "coverage", "%")

    def __init__(self, template, threshold, label, suffix=None):
        self.template = template
        self.threshold = threshold
        self.label = label
        self.suffix = suffix

    @classmethod
    def exists(cls, name: str) -> bool:
        """Test whether a style exists."""
        try:
            _ = cls[name]
            return True
        except KeyError:
            return False
