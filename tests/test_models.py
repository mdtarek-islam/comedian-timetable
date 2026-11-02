"""Comedian and demographic models, and comedian to demographic matching."""

import comedian
import demographic
import scheduler
import timetable


def test_add_theme_appends_to_list():
	c = comedian.Comedian("A", ["Satire"])
	c.addTheme("Politics")
	assert c.themes == ["Satire", "Politics"]


def test_set_reference_uses_argument():
	d = demographic.Demographic("old", ["Satire"])
	d.setReference("new")
	assert d.reference == "new"


def test_default_lists_are_not_shared():
	a = demographic.Demographic()
	a.addTopic("Satire")
	assert demographic.Demographic().topics == []
	c = comedian.Comedian()
	c.addTheme("Satire")
	assert comedian.Comedian().themes == []


def make(themes, topics):
	return comedian.Comedian("C", themes), demographic.Demographic("D0001", topics)


def test_type_checker_main_test_invalid():
	sch = scheduler.Scheduler([], [])
	assert sch.typeChecker(*make(["Satire", "Politics", "Money"], ["Satire", "Politics"])) == "main"
	assert sch.typeChecker(*make(["Satire", "Money"], ["Satire", "Politics"])) == "test"
	assert sch.typeChecker(*make(["Money"], ["Satire", "Politics"])) == "invalid"


def test_type_checker_agrees_with_can_market():
	tt = timetable.Timetable(2)
	sch = scheduler.Scheduler([], [])
	cases = [
		(["Satire", "Politics", "Money"], ["Satire", "Politics"]),
		(["Satire", "Money"], ["Satire", "Politics"]),
		(["Money"], ["Satire", "Politics"]),
	]
	for themes, topics in cases:
		c, d = make(themes, topics)
		kind = sch.typeChecker(c, d)
		assert tt.canMarket(c, d, False) == (kind == "main")
		assert tt.canMarket(c, d, True) == (kind in ("main", "test"))


def test_valid_slot2_counts_daily_hours_apart_from_weekly_hours():
	sch = scheduler.Scheduler([], [])
	c = comedian.Comedian("C", ["Satire", "Politics"])
	tt = timetable.Timetable(2)
	tt.addSession("Monday", 1, c, demographic.Demographic("D0001", ["Satire"]), "test")
	tt.addSession("Tuesday", 1, c, demographic.Demographic("D0002", ["Satire"]), "test")
	# Tuesday holds 1 hour, so a second 1 hour test show is legal (2 a day, 3 a week).
	assert sch.validSlot2(sch.days, 1, c, demographic.Demographic("D0003", ["Satire"]), "test", tt)
