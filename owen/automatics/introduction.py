from manimlib.imports import *
from owen.automatics.inverted_pendulum import InvertedPendulumCart

class TitleScreen(Scene):
	def construct(self):
		title = TextMobject("Automation")
		title.scale(3)
		name = TextMobject("Owen Allemang")
		spec = TextMobject("ELSS")
		VGroup(title, name, spec).arrange(DOWN)
		self.play(
			Write(title),
			Write(name),
			Write(spec)
		)
		self.wait()

class IntroductionToControl(TeacherStudentsScene):
	CONFIG = {
		"camera_config": {
			"background_color": BLACK,
		}
	}

	# def setup(self):
	# 	PiCreatureScene.setup(self)

	# def construct(self):
	# 	morty = self.pi_creature
	# 	self.add(morty)
	# 	self.play(morty.change, "pondering")
	# 	self.wait(2)
	def construct(self):
		# before bunch of example like circuit or stuff
		# see ionisx

		title = TextMobject("Introduction to Control System")
		title.to_edge(UP)
		self.add(title)

		# self.teacher.change("pondering")
		# for student in self.students:
		# 	student.change("pondering", screen)
		self.teacher_says(
			"Let's say a drone is trying\\\\"
			"to get somwhere..",
			target_mode="speaking",
		)
		self.wait()
		self.teacher_says(
			"You have to control its\\\\"
			"speed given its position",
			target_mode="speaking",
		)
		self.teacher.change("pondering")
		self.wait(5)
		self.student_says(
			"How can I do that\\\\"
			"for any cases?",
			target_mode="pondering"
		)
		self.wait(5)
		self.teacher_says(
			"Easy!!\\\\"
			"Use Control System",
			target_mode="speaking"
		)
		self.wait()


class SomeOfYouWatching(TeacherStudentsScene):

	def construct(self):
		screen = self.screen
		screen.scale(1.25, about_edge=UL)
		screen.set_fill(BLACK, 1)
		self.add(screen)

		self.teacher.change("pondering")
		for student in self.students:
			student.change("pondering", screen)

		self.student_says(
			"Well...yeah",
			target_mode="plain"
		)
		self.wait(3)
