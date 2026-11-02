"""ReaderWriter: load every example problem and round-trip a file."""

import pytest

import ReaderWriter
from conftest import PROBLEMS, load


def test_eight_example_problems_exist():
	assert len(PROBLEMS) == 8


@pytest.mark.parametrize("name", PROBLEMS)
def test_problem_loads(name):
	comedians, demographics = load(name)
	assert len(demographics) == 25
	assert len(comedians) >= 10
	for c in comedians:
		# The preamble says 3 to 8 themes, but Problem8 holds a comedian with 9.
		assert c.name and len(c.themes) >= 3
	for d in demographics:
		assert d.reference and len(d.topics) in (2, 3)
	assert len({d.reference for d in demographics}) == 25


def test_write_then_read_round_trip(tmp_path):
	comedians, demographics = load(PROBLEMS[0])
	out = tmp_path / "copy.txt"
	rw = ReaderWriter.ReaderWriter()
	rw.writeRequirements(comedians, demographics, str(out))
	comedians2, demographics2 = rw.readRequirements(str(out))
	assert [(c.name, c.themes) for c in comedians2] == [(c.name, c.themes) for c in comedians]
	assert [(d.reference, d.topics) for d in demographics2] == [(d.reference, d.topics) for d in demographics]
