import random


"""
ahrim: 6 pieces [0]
akrisae: 4 pieces [1]
dharok: 4 pieces [2]
guthan: 4 pieces [3]
karil: 6 pieces [4]
torag: 4 pieces [5]
verac: 4 pieces [6]
------
total: 32 pieces

linza: 5 pieces [7]
------



Theory A:
Linza is 1/512 per chest 

Theory B:
Linza is 1/512 per reward slot

Strategy "allbrothers":
Kill all brothers until the title is obtained

Strategy "linzaonly":
Kill all brothers until full sets of all non-linza armour are obtained,
then kill only Linza.

lotd: 1 --> luck of the dwarves used
lotd: 2 --> luck of the dwarves not used

"""


regular_brothers = ["ahrim", "akrisae", "dharok", "guthan", "karil", "torag", "verac"]
all_brothers = regular_brothers + ["linza"]

set_size = {
	"ahrim": 6,
	"akrisae": 4,
	"dharok": 4,
	"guthan": 4,
	"karil": 4,
	"torag": 4,
	"verac": 4,
	"linza": 5
}

maxkills = 100000

def roll(chance):
	return random.randint(0,chance-1) is 0

def run_simulations(iterations, theory, lotd, strategy):
	kc_to_title = []

	for i in range(iterations):
		r = Iteration()
		e = r.roll_until_title(theory, lotd, strategy)
		kc_to_title += [e]

	print(float(sum(kc_to_title))/max(len(kc_to_title),1))


class Iteration:
	def __init__(self):
		self.kills = 0
		self.drops = {}

		for brother in all_brothers:
			self.drops[brother] = [0] * set_size[brother]


	def check_non_linza_set(self):
		return all(all(piece > 0 for piece in self.drops[brother]) for brother in regular_brothers)

	def check_full_set(self):
		return all(all(piece > 0 for piece in self.drops[brother]) for brother in all_brothers)

	def roll_all_brothers(self, theory, lotd):
		
		self.kills += 1

		if theory is "A":
			# roll linza
			if roll(512-lotd):
				# roll which piece and increment
				self.drops["linza"][random.randint(0,set_size["linza"]-1)] += 1
			
			# roll other brothers, 7 times
			for i in range(7):
				# roll whether unique
				if roll(73-lotd):
					# roll which brother, which piece, and increment
					uniquebrother = random.choice(regular_brothers)
					self.drops[uniquebrother][random.randint(0,set_size[uniquebrother])-1] += 1

		if theory is "B":
			# 7 equivalent reward slots
			for i in range(7):
				# roll linza
				if roll(512-lotd):
				  # roll which piece and increment
				  self.drops["linza"][random.randint(0,set_size["linza"]-1)] += 1
				else:
					if roll(73-lotd):
					  # roll which brother, which piece, and increment
					  uniquebrother = random.choice(regular_brothers)
					  self.drops[uniquebrother][random.randint(0,set_size[uniquebrother])-1] += 1

	def roll_linza_only(self, theory, lotd):

		self.kills += 1

		# theories A and B almost coincide if you only kill linza
		# the only difference is that you only roll regular pieces if you fail linza with theory B
		# this actually doesn't change the expected kills to title with either of the considered strategies

		if theory is "A":
			# roll linza
			if roll(512-lotd):
				# roll which piece and increment
				self.drops["linza"][random.randint(0,set_size["linza"]-1)] += 1
	
			# roll other brothers, 1 time
			# roll whether unique
			if roll(450-lotd):
				# roll which brother, which piece, and increment
				uniquebrother = random.choice(regular_brothers)
				self.drops[uniquebrother][random.randint(0,set_size[uniquebrother])-1] += 1

		if theory is "B":
			# roll linza
			if roll(512-lotd):
				# roll which piece and increment
				self.drops["linza"][random.randint(0,set_size["linza"]-1)] += 1
			else:
				if roll(450-lotd):
					# roll which brother, which piece, and increment
					uniquebrother = random.choice(regular_brothers)
					self.drops[uniquebrother][random.randint(0,set_size[uniquebrother])-1] += 1

	def roll_until_title(self, theory, lotd, strategy):

		if strategy is "allbrothers":
			while (not self.check_full_set()) and self.kills <= maxkills:
				self.roll_all_brothers(theory, lotd)

			return self.kills

		if strategy is "linzaonly":
			while (not self.check_non_linza_set()) and self.kills <= maxkills:
				self.roll_all_brothers(theory, lotd)
			while (not self.check_full_set()) and self.kills <= maxkills:
				self.roll_linza_only(theory, lotd)

			return self.kills




