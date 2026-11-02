import keyword
import comedian
import demographic
import ReaderWriter
import timetable
import random
import math

class Scheduler:

	def __init__(self, comedian_List, demographic_List):
		"""Store the problem lists, the weekday names and an empty list of annealing candidates."""
		self.comedian_List = comedian_List
		self.demographic_List = demographic_List
		#list of the keys used for the timetable dictionary, they are used quite often hence why placed in the initializer function
		self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		#initiated an empty list which will consist of timetables created from simulated annealing
		self.minCostList = list()

	#Using the comedian_List and demographic_List, the this class will create a timetable of slots for each of the 5 weekdays in a week.
	#The slots are labelled 1-5, and so when creating the timetable, they can be assigned as such:
	#	timetableObj.addSession("Monday", 1, comedian_Obj, demographic_Obj, "main")
	#This line will set the session slot '1' on Monday to a main show with comedian_obj, which is being marketed to demographic_obj.
	#Note here that the comedian and demographic are represented by objects, not strings.
	#The day (1st argument) can be assigned the following values: "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
	#The slot (2nd argument) can be assigned the following values: 1, 2, 3, 4, 5 in Task 1 and 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 in Tasks 2 and 3.
	#Comedian (3rd argument) and Demographic (4th argument) can be assigned any value, but if the comedian or demographic are not in the original lists,
	#	your solution will be marked incorrectly.
	#The final, 5th argument, is the show type. For Task 1, all shows should be "main". For Tasks 2 and 3, you should assign either "main" or "test" as the show type.
	#In Tasks 2 and 3, all shows will either be a 'main' show or a 'test' show

	#demographic_List is a list of Demographic objects. A Demographic object, 'd' has the following attributes:
	# d.reference  - the reference code of the demographic
	# d.topics - a list of strings, describing the topics that the demographic likes to see in their comedy shows e.g. ["Politics", "Family"]

	#comedian_List is a list of Comedian objects. A Comedian object, 'c', has the following attributes:
	# c.name - the name of the Comedian
	# c.themes - a list of strings, describing the themes that the comedian uses in their comedy shows e.g. ["Politics", "Family"]

	#For Task 1:
	#Keep in mind that a comedian can only have their show marketed to a demographic
	#	if the comedian's themes contain every topic the demographic likes to see in their comedy shows.
	#Furthermore, a comedian can only perform one main show a day, and a maximum of two main shows over the course of the week.
	#There will always be 25 demographics, one for each slot in the week, but the number of comedians will vary.
	#In some problems, demographics will have 2 topics and in others 3 topics.
	#A comedian will have between 3-8 different themes.

	#For Tasks 2 and 3:
	#A comedian can only have their test show marketed to a demographic if the comedian's themes contain at least one topic
	#	that the demographic likes to see in their comedy shows.
	#Comedians can only manage 4 hours of stage time a week, where main shows are 2 hours and test shows are 1 hour.
	#A Comedian cannot be on stage for more than 2 hours a day.

	#You should not use any other methods and/or properties from the classes, these five calls are the only methods you should need.
	#Furthermore, you should not import anything else beyond what has been imported above.
	#To reiterate, the five calls are timetableObj.addSession, d.reference, d.topics, c.name, c.themes

	#This method should return a timetable object with a schedule that is legal according to all constraints of Task 1.
	"""
	This method implements a backtracking algorithm with the additions constraints of MRV (Minimum Remaining Value) and LCV (Least Constraining Value) 
	to generate a schedule for a comedy show. The algorithm takes into consideration the demographic and comedian information provided, to create a valid 
	schedule that maximizes the number of comedians that are well-suited for each demographic. The schedule is represented as a timetable object which is
	returned as the final output.
	MRV and LCV are implemented by sorting the demographics in ascending order of number of suitable comedians and sorting the available comedians in 
	ascending order of compatible demographics. This helps the algorithm to focus on the most constrained demographics and comedians first, which reduces
	the search space and improves the efficiency of the algorithm.
	The backtracking algorithm is a classic technique used in constraint satisfaction problems, where the goal is to find a solution that adheres to certain
	constraints while maximizing a specific objective function. The use of MRV and LCV heuristics helps to enhance the performanca of the algorithm by
	reducing the search space and guiding the algorithm to make more informed decisions. The algorithm is simple and efficient, making it well suited for
	solving scheduling problems such asthis one. The use of backtracking algorithm with MRV and LCV in this scenario is supported by its ability to find 
	a valid schedule that maximizes the number of well-suited comedians per demographic, while also reducing the number of branches to explore in the search space.
	"""
	def createSchedule(self):
		"""Return a Task 1 timetable: 25 main shows, 5 a day, found by backtracking."""
		#Do not change this line
		timetableObj = timetable.Timetable(1)

		#Here is where you schedule your timetable
		#This line generates a random timetable, that is unlikely to be valid. You can use this or delete it.
		#self.randomMainSchedule(timetableObj)

		#create an array of all the demographics and how many compatible comedians they have
		comediansPerDemographic = []
		for demographic in self.demographic_List:
			count = 0
			comedians = []
			for comedian in self.comedian_List:
				if set(demographic.topics).issubset(set(comedian.themes)):
					count += 1
					comedians.append(comedian)

			comediansPerDemographic.append( (demographic, count) )

		#via MRV sort the list out in order of ascending number of suitable comedians
		comediansPerDemographic = sorted(comediansPerDemographic, key=lambda x: x[1])
		#task 1 only has 5 slots
		slotsPerDay = 5
		#call the backtrackinh fun
		#                  dayIndex,     currentSlot
		self.backtrack(self.days, 0, slotsPerDay, 1, comediansPerDemographic, timetableObj)
		
		#Do not change this line
		return timetableObj

	#Now, for Task 2 we introduce test shows. Each day now has ten sessions, and we want to allocate one main show and one test show
	#	to each demographic.
	#All slots must be either a main or a test show, and each show requires a comedian and a demographic.
	#A comedian can have their test show marketed to a demographic if the comedian's themes include at least one topic the demographic likes.
	#We are also concerned with stage hours. A comedian can be on stage for a maximum of four hours a week.
	#Main shows are 2 hours long, test shows are 1 hour long.
	#A comedian cannot be on stage for more than 2 hours a day.
	"""
	The method uses backtracking again, as well as the additional constraints of MRV and LCV to generate a schedule for a comedy show that
	includes both main and test shows. Unlike the previous function, this algorithm takes into account the allocation of n=both "main" and "test"
	shows to each demographic, with a total of 10 slots per day. The algorithm also considers the additional constraints of stage hours and maximum
	hours per day for a comedian, ensuring that no comedian exceeds their allottede stage time.
	MRV and LCV used in a similar way, helping the algorithm to focus on the most constrained demographics first, which
	reduces the search space and improves the efficiency of the algorithm.
	The backtracking algorithm has been modified to consider the additional constraints and objectives of allocating both main and test shows, while
	also ensuring the stage hours and maximum hours per day for a comedian are not exceeded. The use of MRV and LCV heuristics helps to enhance the
	performance of the algorithm by reduxing the search space and guiding the algorithm to make more informed decisions. Overall, this approach is able
	to find a valid schedule that meets the additional constraints and objectives while also reducing the number of branchs to explore in the search space.
	"""
	def createTestShowSchedule(self):
		"""Return a Task 2 timetable: one main and one test show per demographic, 10 a day."""
		#Do not change this line
		timetableObj = timetable.Timetable(2)

		#Here is where you schedule your timetable
		#This line generates a random timetable, that is unlikely to be valid. You can use this or delete it.
		#self.randomMainAndTestSchedule(timetableObj)

		#calling a function that provides MRV sorted demographics
		comediansPerDemographic = self.sortedDemographics()
		#task 2 and 3 both have 10 slots
		slotsPerDay = 10
		#call the bacltrack function with all the interview
		self.backtrack(self.days, 0, slotsPerDay, 1, comediansPerDemographic, timetableObj)

		#Do not change this line
		return timetableObj

	#Now, in Task 3 it costs £500 to hire a comedian for a single main show.
	#If we hire a comedian for a second show, it only costs £300. (meaning 2 shows cost £800 compared to £1000)
	#If those two shows are run on consecutive days, the second show only costs £100. (meaning 2 shows cost £600 compared to £1000)

	#It costs £250 to hire a comedian for a test show, and then £50 less for each extra test show (i.e., £200, £150 and £100)
	#If a test shows occur on the same day as anything else a comedian is in, then its cost is halved.

	#Using this method, return a timetable object that produces a schedule that is close, or equal, to the optimal solution.
	#You are not expected to always find the optimal solution, but you should be as close as possible.
	#You should consider the lecture material, particular the discussions on heuristics, and how you might develop a heuristic to help you here.
	"""
	This method uses a combination of backtracking and simulated annealing algorithm to generate a schedule for a comedy show that minimizes the
	cost of hiring comedians while still considering the demographic and comedian information provided. The algorithm takes into account the additional 
	costs associated with hiring comedians for main and test shows, with a total of 10 slots per day.
	The backtracking algorithm is used as the initial run to generate a valid schedule, and then a simulated annealing algorithm is applied to find the 
	solution that is close or equal to the optimal solution. The simulated annealing algorithm is a heuristic optimization method that is particularly well-suited 
	for solving scheduling problems with multiple constraints and objectives, such as this one, where the goal is to minimize the cost of hiring comedians 
	while still ensuring that the schedule is valid and meets the demographic and comedian information provided. The simulated annealing algorithm starts with 
	a high temperature, where it can accept solutions that are not optimal, and gradually decreases the temperature, causing it to converge to a near-optimal solution.
	Overall, this approach combines the strengths of both backtracking and simulated annealing algorithm to find an efficient schedule that minimizes the cost of hiring
	comedians while still ensuring that the schedule is valid and meets the demographic and comedian information provided.
	"""
	def createMinCostSchedule(self):
		"""Return a Task 3 timetable: a Task 2 backtracking schedule improved by simulated annealing."""
		#Do not change this line
		timetableObj = timetable.Timetable(3)

		#Here is where you schedule your timetable
		#This line generates a random timetable, that is unlikely to be valid. You can use this or delete it.
		#self.randomMainAndTestSchedule(timetableObj)
		
		#aquiring MRV sorted demographics
		comediansPerDemographic = self.sortedDemographics()
		#task 3 has 10 slots
		slotsPerDay = 10
		#calling backtrack as the initial run
		self.backtrack(self.days, 0, slotsPerDay, 1, comediansPerDemographic, timetableObj)

		#perform simulated annealing to find a solution
		timetableObj = self.simulatedAnnealing(timetableObj)

		#Do not change this line
		return timetableObj


	#This simplistic approach merely assigns each demographic and comedian to a random slot, iterating through the timetable.
	def randomMainSchedule(self,timetableObj):
		"""Fill a Task 1 timetable with random comedians. The result is rarely legal."""

		sessionNumber = 1
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		dayNumber = 0
		for demographic in self.demographic_List:
			comedian = self.comedian_List[random.randrange(0, len(self.comedian_List))]

			timetableObj.addSession(days[dayNumber], sessionNumber, comedian, demographic, "main")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 6:
				sessionNumber = 1
				dayNumber = dayNumber + 1

	#This simplistic approach merely assigns each demographic to a random main and test show, with a random comedian, iterating through the timetable.
	def randomMainAndTestSchedule(self,timetableObj):
		"""Fill a Task 2 timetable with random comedians. The result is rarely legal."""

		sessionNumber = 1
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		dayNumber = 0
		for demographic in self.demographic_List:
			comedian = self.comedian_List[random.randrange(0, len(self.comedian_List))]

			timetableObj.addSession(days[dayNumber], sessionNumber, comedian, demographic, "main")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 11:
				sessionNumber = 1
				dayNumber = dayNumber + 1

		for demographic in self.demographic_List:
			comedian = self.comedian_List[random.randrange(0, len(self.comedian_List))]

			timetableObj.addSession(days[dayNumber], sessionNumber, comedian, demographic, "test")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 11:
				sessionNumber = 1
				dayNumber = dayNumber + 1

	#applying MRV by sorting the list of demographics in ascending order of main and test comedians
	def sortedDemographics(self):
		"""Return (demographic, comedian names, count, show type) tuples sorted by count (MRV)."""
		comediansForDemographic = []
		for demographic in self.demographic_List:
			countMain = 0
			countTest = 0
			mainComedians = []
			testComedians = []
			for comedian in self.comedian_List:
				if set(demographic.topics).issubset(set(comedian.themes)):
					countMain += 1
					mainComedians.append(comedian.name)
				elif set(demographic.topics) & set(comedian.themes):
					countTest += 1
					testComedians.append(comedian.name)

			comediansForDemographic.append( (demographic, mainComedians, countMain, "main") )
			comediansForDemographic.append( (demographic, testComedians, countTest, "test") )
		
		comediansForDemographic = sorted(comediansForDemographic, key=lambda x: x[2])
		
		return comediansForDemographic

	#this is a backtracking approach
	def backtrack(self, days, currentDayIndex, slotsPerDay, currentSlot, sortedDemographics, timetableObj):
		"""Fill slots in day order by recursive backtracking. Return True when every slot is filled."""
		#change to next day when iterated through 5 slots
		if currentSlot > slotsPerDay:
			#slot can only be 1, 2, 3, 4 or 5
			currentSlot = 1
			currentDayIndex += 1
			#finish if iterated through all the days
			if currentDayIndex == len(days):
				return True

		#produce the unassigned variable, in this case it is the list of the demographics yet to be placed in a slot
		#an entry counts as placed when its demographic (and, for tasks 2 and 3, its show type) is already in the timetable
		unassignedDemographics = []
		for demographic in sortedDemographics:
			placed = False
			for day, slots in timetableObj.schedule.items():
				for slot, values in slots.items():
					if demographic[0] == values[1] and (slotsPerDay == 5 or demographic[3] == values[2]):
						placed = True
			if not placed:
				unassignedDemographics.append(demographic[0])

		demographicsPerComedian = []
		for comedian2 in self.comedian_List:
			countMain = 0
			countTest = 0
			mainDemographics = []
			testDemographics = []
			for demographic2 in unassignedDemographics:
				if set(demographic2.topics).issubset(set(comedian2.themes)):
					countMain += 1
					mainDemographics.append(demographic2.reference)
				elif (set(demographic2.topics) & set(comedian2.themes)) and slotsPerDay==10:
					countTest += 1
					testDemographics.append(demographic2.reference)

			demographicsPerComedian.append((comedian2, countMain, "main"))
			if slotsPerDay == 10:
				demographicsPerComedian.append((comedian2, countTest, "test"))

		demographicsPerComedian = sorted(demographicsPerComedian, key=lambda y: y[1])
		
		for aDemographic in unassignedDemographics:
			#find a suitable comedian and then check for the constraints
			for comedian in demographicsPerComedian:
				theComedian = comedian[0] 
				#check for the constaints, if met criteria add
				type = self.typeChecker(theComedian, aDemographic)
				#if slotsPerDay == 5:
				if self.slotChecker(slotsPerDay, days, currentDayIndex, theComedian, aDemographic, type, timetableObj):
					#                     day, slot, comedian, demographic, type
					timetableObj.addSession(days[currentDayIndex], currentSlot, theComedian, aDemographic, type)
					#recursive backtrack, return true if works
					if self.backtrack(days, currentDayIndex, slotsPerDay, currentSlot + 1, sortedDemographics, timetableObj):
						return True
					#remove session from the timetable
					del timetableObj.schedule[days[currentDayIndex]][currentSlot]

		return False
	#check the type of show it is
	def typeChecker(self, theComedian, aDemographic):
		"""Return 'main' if the comedian covers every topic, 'test' if one topic, else 'invalid'."""
		if set(aDemographic.topics).issubset(set(theComedian.themes)):
			return "main"
		elif set(aDemographic.topics) & set(theComedian.themes):
			return "test"
		else:
			return "invalid"
	#checks according to task number
	def slotChecker(self, slotsPerDay, days, currentDayIndex, theComedian, aDemographic, type, timetableObj):
		"""Dispatch to the Task 1 or Task 2/3 constraint check based on the slots per day."""
		if slotsPerDay == 5:
			return self.validSlot1(days, currentDayIndex, theComedian, aDemographic, type, timetableObj)
		elif slotsPerDay == 10:
			return self.validSlot2(days, currentDayIndex, theComedian, aDemographic, type, timetableObj)


	#this checks for the constraints for task 1
	def validSlot1(self, days, currentDayIndex, theComedian, aDemographic, type, timetableObj):
		"""Return True if the Task 1 constraints still hold after adding this main show."""
		repeatComedian = 0
		#check if comedian is suitable for the demographic
		if type != "main":
			return False
		for day, slots in timetableObj.schedule.items():
			#if comedian already exists
			for slot, values in slots.items():
				#if demographic already exists
				if aDemographic == values[1]:
					return False
				#comedian exists and is on the same day
				if theComedian == values[0]:
					#if comedian exists on the same day
					if day == days[currentDayIndex]:
						return False
					else:
						repeatComedian += 1
						#comedian cannot perform more than twice a week
						if repeatComedian == 2:
							return False
		return True

	#this checks for the constraints for task 1
	def validSlot2(self, days, currentDayIndex, theComedian, aDemographic, type, timetableObj):
		"""Return True if the Task 2/3 constraints still hold after adding this show."""
		comedianHours = 0
		#check if comedian is either main or test
		if type == "main":
			comedianHours += 2
		elif type == "test":
			comedianHours += 1
		else:
			return False
		#hours on the target day are tracked apart from the weekly total
		dayHours = comedianHours

		for day, slots in timetableObj.schedule.items():
			#if comedian already exists
			for slot, values in slots.items():
				#if demographic already exists, make sure it is of a different show type
				if aDemographic == values[1] and type == values[2]:
					return False
				#if comedian exists and is a main show
				if theComedian == values[0]:
					if values[2] == "main":
						showHours = 2
					else:
						showHours = 1
					comedianHours += showHours
					if day == days[currentDayIndex]:
						dayHours += showHours
						if dayHours > 2:
							return False
					if comedianHours > 4:
						return False
					
		return True

	def simulatedAnnealing(self, initialState):
		"""Search for a lower cost schedule from the initial state. Return the cheapest state seen."""
		#set the temperatures
		initialTemperature = 30000
		alpha = 0.999
		finalTemperature = 0.01
		currentTemperature = initialTemperature
		#initialize current state with the initial state
		currentState = initialState
		solution = currentState
		#start each run with only the initial state, so the result is never worse than the backtracking schedule
		self.minCostList = [(initialState, self.calculateCost(initialState))]

		while currentTemperature > finalTemperature:
			neighbour = self.swap(currentState)
			neighbourCost = self.calculateCost(neighbour)
			costDifference = self.calculateCost(currentState) - neighbourCost
			#accept new solution if better
			if costDifference > 0:
				currentState = neighbour
				self.minCostList.append((neighbour, neighbourCost))
			#if new solution not better, accept it with probability of e^(-cost/temp)
			#costDifference is zero or negative here, so the probability is at most 1
			else:
				try:
					if random.random() < math.exp(costDifference/currentTemperature):
						currentState = neighbour
						self.minCostList.append((neighbour, neighbourCost))
				except:
					pass

			currentTemperature *= alpha

		self.minCostList = sorted(self.minCostList, key=lambda z: z[1])
		solution = self.minCostList[0][0]

		return solution
	#uses random values from the schedule to attemot decreasing cost
	def swap(self, timetableObj):
		"""Return a copy of the timetable after up to 100 random legal moves."""
		newTimetableObj = timetable.Timetable(3)
		#copy a timetable object onto a new one
		self.deepCopyTimetableObject(timetableObj, newTimetableObj)
		for repetition in range(random.randint(0, 100)):
			randomOption = random.choice([1, 2, 3])
			#option 1, swap any two days
			if randomOption == 1:
				originalKey = random.choice(list(newTimetableObj.schedule.keys()))
				targetKey = random.choice(list(newTimetableObj.schedule.keys()))
				temp = newTimetableObj.schedule[originalKey]
				newTimetableObj.schedule[originalKey] = newTimetableObj.schedule[targetKey]
				newTimetableObj.schedule[targetKey] = temp
			#option 2, swap any two demographics
			elif randomOption == 2:
				originalKey = random.choice(list(newTimetableObj.schedule.keys()))
				originalSlot = random.choice(list(newTimetableObj.schedule[originalKey].keys()))
				targetKey = random.choice(list(newTimetableObj.schedule.keys()))
				targetSlot = random.choice(list(newTimetableObj.schedule[targetKey].keys()))
				if originalKey == targetKey and originalSlot == targetSlot:
					continue
				#lift both sessions out first, so validSlot2 does not reject a session for clashing with itself
				originalSession = newTimetableObj.schedule[originalKey].pop(originalSlot)
				targetSession = newTimetableObj.schedule[targetKey].pop(targetSlot)
				checkChangedOriginalSlot = self.validSlot2(self.days, self.days.index(originalKey), targetSession[0], targetSession[1], targetSession[2], newTimetableObj)
				checkChangedTargetSlot = False
				if checkChangedOriginalSlot:
					newTimetableObj.schedule[originalKey][originalSlot] = targetSession
					checkChangedTargetSlot = self.validSlot2(self.days, self.days.index(targetKey), originalSession[0], originalSession[1], originalSession[2], newTimetableObj)
				if checkChangedOriginalSlot and checkChangedTargetSlot:
					newTimetableObj.schedule[targetKey][targetSlot] = originalSession
				else:
					newTimetableObj.schedule[originalKey][originalSlot] = originalSession
					newTimetableObj.schedule[targetKey][targetSlot] = targetSession
			#option 3, swap comedian
			elif randomOption == 3:
				randomComedian = random.choice(list(self.comedian_List))
				randomKey = random.choice(list(newTimetableObj.schedule.keys()))
				randomSlot = random.choice(list(newTimetableObj.schedule[randomKey].keys()))
				[oldComedian, slotDemographic, slotType] = newTimetableObj.schedule[randomKey][randomSlot]
				#the new comedian must suit the demographic for this show type
				suitability = self.typeChecker(randomComedian, slotDemographic)
				if suitability == "invalid" or (slotType == "main" and suitability != "main"):
					continue
				#lift the session out first, so validSlot2 does not reject it for clashing with itself
				oldSession = newTimetableObj.schedule[randomKey].pop(randomSlot)
				if self.validSlot2(self.days, self.days.index(randomKey), randomComedian, slotDemographic, slotType, newTimetableObj):
					newTimetableObj.schedule[randomKey][randomSlot] = [randomComedian, slotDemographic, slotType]
				else:
					newTimetableObj.schedule[randomKey][randomSlot] = oldSession

		return newTimetableObj

	def deepCopyTimetableObject(self, timetableObj, newTimetableObj):
		"""Copy each day and slot of one timetable into another. Slot lists are shared."""
		for key, value in timetableObj.schedule.items():
			for key2, value2 in value.items():
				newTimetableObj.schedule[key][key2] = value2
		return newTimetableObj

	def calculateCost(self, timetableObj):
		"""Return the Task 3 cost of a timetable, using the same rules as the checker."""
		scheduleCost = 0
		comediansYesterday = list()
		mainShowCount = dict()
		testShowCount = dict()

		for comedian in self.comedian_List:
			mainShowCount[comedian.name] = 0
			testShowCount[comedian.name] = 0


		for day in timetableObj.schedule:
			dayList = timetableObj.schedule[day]

			comediansToday = dict()
			possibleDiscount = dict()

			#process the validity of each entry
			for entry in timetableObj.schedule[day]:
				[comedian, demographic, showType] = dayList[entry]
				#We now go through every comedian to make sure they are not on stage for too long in a week
				if comedian.name in comediansToday:
					#We calculate the cost for the show, if it is a main show.
					if showType == "main":
						comediansToday[comedian.name] = comediansToday[comedian.name] + 2
						mainShowCount[comedian.name] = mainShowCount[comedian.name] + 1
						if mainShowCount[comedian.name] == 1:
							scheduleCost = scheduleCost + 500
						elif comedian.name in comediansYesterday:
							scheduleCost = scheduleCost + 100
						else:
							scheduleCost = scheduleCost + 300
					else:
						#We calculate the cost of a test show
						comediansToday[comedian.name] = comediansToday[comedian.name] + 1
						testShowCount[comedian.name] = testShowCount[comedian.name] + 1
						initialTestShowCost = (300 - (50 * testShowCount[comedian.name])) / 2
						scheduleCost = scheduleCost + initialTestShowCost

						if comedian.name in possibleDiscount:
							scheduleCost = scheduleCost - possibleDiscount.pop(comedian.name)
				else:
					#This branch means the comedian has not yet been on stage today
					#We calculate the costs correspondingly
					if showType == "main":
						comediansToday[comedian.name] = 2
						mainShowCount[comedian.name] = mainShowCount[comedian.name] + 1
						if mainShowCount[comedian.name] == 1:
							scheduleCost = scheduleCost + 500
						elif comedian.name in comediansYesterday:
							scheduleCost = scheduleCost + 100
						else:
							scheduleCost = scheduleCost + 300
					else:
						comediansToday[comedian.name] = 1

						testShowCount[comedian.name] = testShowCount[comedian.name] + 1
						initialTestShowCost = (300 - (50 * testShowCount[comedian.name]))
						scheduleCost = scheduleCost + initialTestShowCost
						possibleDiscount[comedian.name] = initialTestShowCost / 2

			comediansYesterday = comediansToday

		#If we get here, schedule is legal, so we assign the cost and return True
		cost = scheduleCost

		return cost
