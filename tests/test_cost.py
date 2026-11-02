"""Task 3 cost rules from the scheduler preamble, checked by hand."""

import comedian
import demographic
import scheduler
import timetable

A = comedian.Comedian("A", ["Satire", "Politics", "Money"])
B = comedian.Comedian("B", ["Satire", "Politics", "Money"])


def demo(i):
	return demographic.Demographic("D%04d" % i, ["Satire", "Politics"])


def cost(sessions):
	"""Return calculateCost for a list of (day, slot, comedian, show type) tuples."""
	tt = timetable.Timetable(3)
	for i, (day, slot, com, kind) in enumerate(sessions):
		tt.addSession(day, slot, com, demo(i), kind)
	return scheduler.Scheduler([A, B], []).calculateCost(tt)


def test_single_main_show_costs_500():
	assert cost([("Monday", 1, A, "main")]) == 500


def test_second_main_show_costs_300():
	assert cost([("Monday", 1, A, "main"), ("Wednesday", 1, A, "main")]) == 800


def test_second_main_show_next_day_costs_100():
	assert cost([("Monday", 1, A, "main"), ("Tuesday", 1, A, "main")]) == 600


def test_test_shows_cost_250_then_50_less():
	sessions = [("Monday", 1, B, "test"), ("Tuesday", 1, B, "test"), ("Wednesday", 1, B, "test"), ("Thursday", 1, B, "test")]
	assert cost(sessions) == 250 + 200 + 150 + 100


def test_two_test_shows_same_day_are_both_halved():
	assert cost([("Monday", 1, B, "test"), ("Monday", 2, B, "test")]) == 125 + 100


def test_different_comedians_are_priced_apart():
	assert cost([("Monday", 1, A, "main"), ("Monday", 2, B, "main")]) == 1000
