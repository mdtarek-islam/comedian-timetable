"""Command line entry point."""

import csv

import pytest

import cli


def test_cli_task1_writes_csv(tmp_path, problem_path):
	out = tmp_path / "schedule.csv"
	assert cli.main(["--problem", problem_path("Problem2.txt"), "--task", "1", "--output", str(out)]) == 0
	with open(out, newline="", encoding="utf-8") as f:
		rows = list(csv.reader(f))
	assert rows[0] == ["day", "slot", "comedian", "demographic", "show_type"]
	assert len(rows) == 26


def test_cli_rejects_unknown_task():
	with pytest.raises(SystemExit):
		cli.main(["--task", "4"])
