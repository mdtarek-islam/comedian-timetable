"""Demographic model: an audience group with a reference code and liked topics."""

#Simple class representing a demographic, which includes the reference code, and the list of topics
#topics is a list of strings
#reference is a string

class Demographic:
	"""An audience demographic, defined by a reference code and a list of topics."""

	def __init__(self,reference="", topics=None):
		"""Store the reference and topics. A missing topics list becomes a new empty list."""
		self.reference = reference
		self.topics = list() if topics is None else topics

	#this is used during set up and should not be used in your solution
	def setReference(self,name):
		"""Replace the reference code."""
		self.reference = name

	#this is used during set up and should not be used in your solution
	def setTopics(self,topics):
		"""Replace the list of topics."""
		self.topics = topics

	#this is used during set up and should not be used in your solution
	def addTopic(self,topic):
		"""Append one topic to the list of topics."""
		self.topics.append(topic)

	def __str__(self):
		return str([self.reference, self.topics])

	def __repr__(self):
		return str(self)
