"""Comedian model: a named performer with a list of comedy themes."""

import demographic

#Class for storing a comedian object, which tracks their name, and themes
#themes are a list of strings
#name is a string

class Comedian:
	"""A comedian, defined by a name and the list of themes they perform."""

	def __init__(self,name="", themes=None):
		"""Store the name and themes. A missing themes list becomes a new empty list."""
		self.name=name
		self.themes=list() if themes is None else themes

	#this is used during set up and should not be used in your solution
	def setName(self,name):
		"""Replace the comedian name."""
		self.name = name

	#this is used during set up and should not be used in your solution
	def setThemes(self,themes):
		"""Replace the list of themes."""
		self.themes = themes

	#this is used during set up and should not be used in your solution
	def addTheme(self,theme):
		"""Append one theme to the list of themes."""
		self.themes.append(theme)

	def __str__(self):
		return str([self.name, self.themes])

	def __repr__(self):
		return str(self)
