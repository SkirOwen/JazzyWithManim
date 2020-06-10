from manimlib.imports import *
from from_3b1b.active.diffyq.part1.shared_constructs import *


class LoopSystem(VGroup):
	CONFIG={
		"open": False,
		"Error": True,
	}

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

class OpenLoop(Scene):
	pass


class ClosedLoop(Scene):
	pass

class SISO_MIMO(Scene):
	pass
	# might need to change the Parent of this class 
	# Scene could not be the most easier choice


class LaplaceTransform(Scene):
	pass
	# and i think there might be a video in WIP somewhere
	# on github, need to get a look to this


class WhyLPTransform(PiCreatureScene):
	pass

class IntroduceRootLocus(Scene):
	pass


class GainControl(Scene):
	pass


class PIDControl(Scene):
	pass
