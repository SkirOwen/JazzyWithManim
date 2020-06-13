from manimlib.imports import *
from from_3b1b.active.diffyq.part1.shared_constructs import *


class LoopSystem(VGroup):
	CONFIG = {
		"close": False,
		"pid": False,
		"gain": False,
		"Error": True,
		"Simple": True,
		"box_width": 2,
		"box_height": 1,
		"labels_on_box": False,
		"comparator_diamater": 1.5,
	}

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.create_fixed_point()
		self.create_input_line()
		self.create_controller()
		self.create_plant()
		self.create_link_CP()
		self.create_output_line()
		if self.close:
			self.create_comparator()
			self.add_comparator_labels()
			# self.create_comparator_line()
			if self.pid:
				self.create_feedback_loop()
				self.create_pid()
		if self.labels_on_box:
			self.add_labels()

	def create_fixed_point(self):
		self.fixed_point_tracker = VectorizedPoint(ORIGIN)
		self.add(self.fixed_point_tracker)
		return self
	
	def create_input_line(self):
		input_line = self.input_line = Arrow(LEFT, RIGHT)
		input_line.move_to(20 * LEFT)
		self.add(input_line)

	def create_controller(self):
		controller = self.controller = Rectangle()
		controller.set_width(self.box_width)
		controller.set_height(self.box_height)
		# controller.set_style(**self.controller_style)
		self.move_to(3 * LEFT)
		self.add(controller)

	def create_plant(self):
		plant = self.plant = Rectangle()
		plant.set_width(self.box_width)
		plant.set_height(self.box_height)
		# plant.set_style(**self.controller_style)
		self.move_to(3 * RIGHT)
		self.add(plant)

	def create_link_CP(self):
		link = self.link = Arrow(LEFT, RIGHT)
		link.move_to(LEFT)
		self.add(link)

	def create_output_line(self):
		output_line = self.output_line = Arrow(LEFT, RIGHT)
		output_line.move_to(5 * RIGHT)
		self.add(output_line)

	def create_comparator(self):
		comparator = self.comparator = Circle()
		comparator.set_width(self.comparator_diamater)
		comparator.move_to(self.input_line.get_end())
		comparator.move_to(self.input_line.get_end() + 0.5 * self.comparator_diamater * RIGHT)
		self.add(comparator)

	def add_comparator_labels(self):
		cmp_label_in = TexMobject("+")
		cmp_label_in.move_to(self.comparator.get_center() + 0.35 * self.comparator_diamater * LEFT)
		cmp_label_feed = TexMobject("-")
		cmp_label_feed.move_to(self.comparator.get_center() + 0.35 * self.comparator_diamater * DOWN)
		labels_comparator_group = self.comparator_group = VGroup(cmp_label_in, cmp_label_feed)
		self.add(labels_comparator_group)

	def create_feedback_loop(self):
		pass

	def create_pid(self):
		pass

	def add_labels(self):
		pass

	def get_fixed_point(self):
		return self.fixed_point_tracker.get_location()

	def get_edge_controller(self):
		return self.comparator.get_center() + 0.5 * self.comparator_diamater


class IntroductionToControl(Scene):
	pass
	# Teacher Studetn Scene with a let's say a drone moving
	# left / right to go to the middle
	# dial:
	# How can i do that ??
	# Easy: Control System
	# What is control system.. ~ ponder ~
	# change scene


class EquationOfTheSystem(Scene):
	def construct(self):
		equation1 = TexMobject("x = 0")
		equation2 = TexMobject("\\dot{x} = 0")
		equation_group = VGroup(equation1, equation2).arrange(DOWN)

		simplify_eq = TexMobject("something")

		self.play(Write(equation_group))
		self.wait(5)
		self.play(Transform(equation_group, simplify_eq))
		self.wait()


class OpenLoop(Scene):
	CONFIG = {
		"loopsystem_config": {
			"close": False,
		},
	}

	def construct(self):
		self.add_system()

	def add_system(self):
		system = self.system = LoopSystem(**self.loopsystem_config)
		# self.add(system)
		self.add(system)
		self.wait(5)


class ClosedLoop(Scene):
	CONFIG = {
		"loopsystem_config": {
			"close": True,
		},
	}

	def construct(self):
		self.add_system()

	def add_system(self):
		system = self.system = LoopSystem(**self.loopsystem_config)
		self.add(system)
		# self.play(
		# 	Write(system)
		# )
		self.wait(5)


class LaplaceTransform(Scene):
	pass
	# and i think there might be a video in WIP somewhere
	# on github, need to get a look to this
	# address the issue where we are in discrte space -> Z-Transform


class WhyLPTransform(PiCreatureScene):
	pass
	# Teacher: well it is easier to solve, whem we go in phase domaine
	# Student: Awh
	# Teacher: but thats is for continous system, for discret ~ shows
	# equation ~ we use Z-Transfomr ~ eq moves to the LEFT to show
	# fromula


class TransferFunctions(Scene):
	def construct(self):
		open_loop_title = TextMobject("Open Loop transfer function")
		close_loop_title = TextMobject("Closed Loop transfer function")

		open_loop_tf= TexMobject(
			"GH(s) = G(s) H(s)"
		)
		close_loop_tf = TexMobject(
			"\\frac{Y(s)}{R(s)} = \\frac{G(s)}{1+G(s)H(s)}"
		)
		open_loop_title.to_corner(UP + LEFT)
		close_loop_title.to_corner(UP + LEFT)

		self.play(Write(open_loop_title))
		self.wait()
		self.play(Write(open_loop_tf))
		self.wait(5)
		self.play(
			Transform(open_loop_title, close_loop_title),
			Transform(open_loop_tf, close_loop_tf)
		)
		self.wait()


class AboutRootAndZero(Scene):
	pass


class IntroduceRootLocus(Scene):
	CONFIG = {
		"initial_unit_size" : 1,
		"final_unit_size" : 1,
		"plane_center" : 1 * RIGHT,
		"x_label_range" : list(range(-8, 6, 2)),
		"y_label_range" : list(range(-3, 4, 2)),
		"dot_color" : YELLOW,
		"square_color" : MAROON_B,
		"big_dot_radius" : 0.075,
		"dot_radius" : 0.05,
	}
	
	def construct(self):
		self.add_plane()
		self.wait(5)

	def add_plane(self):
		width = (FRAME_X_RADIUS+abs(self.plane_center[0]))/self.final_unit_size
		height = (FRAME_Y_RADIUS+abs(self.plane_center[1]))/self.final_unit_size
		background_plane = ComplexPlane(
			x_radius = width,
			y_radius = height,
			stroke_width = 2,
			stroke_color = BLUE_E,
			secondary_line_ratio = 0,
		)
		background_plane.axes.set_stroke(width = 4)

		background_plane.scale(self.initial_unit_size)
		background_plane.shift(self.plane_center)

		coordinate_labels = VGroup()
		z_list = np.append(
			self.x_label_range,
			complex(0, 1)*np.array(self.y_label_range)
		)
		for z in z_list:
			if z == 0:
				continue
			if z.imag == 0:
				tex = str(int(z.real))
			else:
				tex = str(int(z.imag)) + "i"
			label = TexMobject(tex)
			label.scale(0.75)
			label.add_background_rectangle()
			point = background_plane.number_to_point(z)
			if z.imag == 0:
				label.next_to(point, DOWN, SMALL_BUFF)
			else:
				label.next_to(point, LEFT, SMALL_BUFF)
			coordinate_labels.add(label)

		self.add(background_plane, coordinate_labels)
		self.background_plane = background_plane
		self.coordinate_labels = coordinate_labels


class GainControl(Scene):
	pass


class PIDControl(Scene):
	pass


class SISO_MIMO(Scene):
	pass
	# might need to change the Parent of this class 
	# Scene could not be the most easier choice
	# PiCreatureScence:
	# What if i have multiple variable? ~ students
	# Well you'll use Matrix notation for that..
	#For instance, insert transfer function of inv_pend?
