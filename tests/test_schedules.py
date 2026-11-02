"""Run each task on each example problem and check the result with Timetable.scheduleChecker."""

import os
import random

import pytest

import scheduler
from conftest import PROBLEMS, load

RUN_SLOW = os.environ.get("RUN_SLOW") == "1"
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


def check_shape(tt, comedians, demographics, slots, types):
	"""Assert each day has the right slots, and every comedian and demographic comes from the problem."""
	names = {c.name for c in comedians}
	refs = {d.reference for d in demographics}
	seen = []
	for day in DAYS:
		assert sorted(tt.schedule[day]) == list(range(1, slots + 1))
		for com, demo, kind in tt.schedule[day].values():
			assert com.name in names and demo.reference in refs and kind in types
			seen.append((demo.reference, kind))
	assert sorted(seen) == sorted((r, t) for r in refs for t in types)


@pytest.mark.parametrize("name", PROBLEMS)
def test_task1_schedule_is_legal(name):
	comedians, demographics = load(name)
	tt = scheduler.Scheduler(comedians, demographics).createSchedule()
	assert tt.scheduleChecker(comedians, demographics)
	check_shape(tt, comedians, demographics, 5, ("main",))


@pytest.mark.parametrize("name", PROBLEMS)
def test_task2_schedule_is_legal(name):
	comedians, demographics = load(name)
	sch = scheduler.Scheduler(comedians, demographics)
	tt = sch.createTestShowSchedule()
	assert tt.scheduleChecker(comedians, demographics)
	check_shape(tt, comedians, demographics, 10, ("main", "test"))
	assert sch.calculateCost(tt) == tt.cost


@pytest.mark.parametrize("name", PROBLEMS[:2])
def test_swap_keeps_schedule_legal(name):
	comedians, demographics = load(name)
	sch = scheduler.Scheduler(comedians, demographics)
	tt = sch.createTestShowSchedule()
	random.seed(7)
	for _ in range(30):
		tt = sch.swap(tt)
		assert tt.scheduleChecker(comedians, demographics)
		check_shape(tt, comedians, demographics, 10, ("main", "test"))


def run_task3(name):
	comedians, demographics = load(name)
	sch = scheduler.Scheduler(comedians, demographics)
	baseline = sch.createTestShowSchedule()
	assert baseline.scheduleChecker(comedians, demographics)
	random.seed(1)
	tt = sch.createMinCostSchedule()
	assert tt.scheduleChecker(comedians, demographics)
	check_shape(tt, comedians, demographics, 10, ("main", "test"))
	assert sch.calculateCost(tt) == tt.cost
	assert tt.cost <= baseline.cost


def test_task3_schedule_is_legal_problem1():
	run_task3(PROBLEMS[0])


@pytest.mark.slow
@pytest.mark.skipif(not RUN_SLOW, reason="Task 3 annealing takes about 10 seconds per problem, 1 minute for all 7. Set RUN_SLOW=1 to run.")
@pytest.mark.parametrize("name", PROBLEMS[1:])
def test_task3_schedule_is_legal_other_problems(name):
	run_task3(name)
