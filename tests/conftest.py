"""Shared helpers. The project uses flat imports, so put the project root on sys.path."""

import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
	sys.path.insert(0, ROOT)

import ReaderWriter  # noqa: E402

PROBLEM_DIR = os.path.join(ROOT, "ExampleProblems")
PROBLEMS = sorted(f for f in os.listdir(PROBLEM_DIR) if f.endswith(".txt"))


def load(name):
	"""Return [comedian list, demographic list] for one example problem file."""
	return ReaderWriter.ReaderWriter().readRequirements(os.path.join(PROBLEM_DIR, name))


@pytest.fixture
def problem_path():
	"""Return a function that maps a problem file name to its full path."""
	return lambda name: os.path.join(PROBLEM_DIR, name)
