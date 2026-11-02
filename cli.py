"""Command line entry point: solve one problem file for Task 1, 2 or 3.

Example:
	python cli.py --problem ExampleProblems/Problem1.txt --task 3 --output schedule.csv
"""

import argparse
import csv
import os
import sys

import ReaderWriter
import scheduler

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PROBLEM = os.path.join(HERE, "ExampleProblems", "Problem1.txt")
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TASK_METHODS = {1: "createSchedule", 2: "createTestShowSchedule", 3: "createMinCostSchedule"}


def solve(problem, task):
	"""Read a problem file and return (timetable, comedian list, demographic list) for the task."""
	[comedian_List, demographic_List] = ReaderWriter.ReaderWriter().readRequirements(problem)
	sch = scheduler.Scheduler(comedian_List, demographic_List)
	tt = getattr(sch, TASK_METHODS[task])()
	return tt, comedian_List, demographic_List


def schedule_rows(tt):
	"""Return the timetable as (day, slot, comedian, demographic, show type) rows in day and slot order."""
	rows = []
	for day in DAYS:
		for slot in sorted(tt.schedule[day]):
			[com, demo, show_type] = tt.schedule[day][slot]
			rows.append((day, slot, com.name, demo.reference, show_type))
	return rows


def write_csv(rows, path):
	"""Write the schedule rows to a CSV file with a header line."""
	with open(path, "w", newline="", encoding="utf-8") as f:
		writer = csv.writer(f)
		writer.writerow(["day", "slot", "comedian", "demographic", "show_type"])
		writer.writerows(rows)


def main(argv=None):
	"""Parse arguments, build the schedule, check it and print the result. Return 0 if legal, else 1."""
	parser = argparse.ArgumentParser(description="Build a weekly comedian timetable for one problem file.")
	parser.add_argument("--problem", default=DEFAULT_PROBLEM, help="path to a problem file (default: ExampleProblems/Problem1.txt)")
	parser.add_argument("--task", type=int, choices=[1, 2, 3], default=1, help="1: main shows, 2: main and test shows, 3: minimum cost")
	parser.add_argument("--output", help="optional CSV path for the schedule")
	args = parser.parse_args(argv)

	tt, comedian_List, demographic_List = solve(args.problem, args.task)
	rows = schedule_rows(tt)
	for row in rows:
		print("%-9s %2d  %-14s %-6s %s" % row)

	legal = tt.scheduleChecker(comedian_List, demographic_List)
	if legal:
		print("Schedule is legal.")
		print("Schedule has a cost of " + str(tt.cost))
	else:
		print("Schedule is not legal.")

	if args.output:
		write_csv(rows, args.output)
		print("Schedule written to " + args.output)
	return 0 if legal else 1


if __name__ == "__main__":
	sys.exit(main())
