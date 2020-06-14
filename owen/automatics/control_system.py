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
		"top_point": 6 * LEFT + 2 * UP
	}

	# TODO: Need to position links more efficiently by get their length

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.create_fixed_point()
		self.create_input_line()
		if self.close:
			self.create_comparator()
			self.add_comparator_labels()
			self.create_link_CC()


			if self.pid:
				self.create_feedback_loop()
				self.create_pid()
		self.create_controller()
		self.create_link_CP()
		self.create_plant()
		self.create_output_line()
		if self.close:
			self.add_feedback_line_in()
			self.create_sensor()
			if self.pid:
				pass
			else:
				self.create_feedback_line_out()
		
		if self.labels_on_box:
			self.add_labels()

	def create_fixed_point(self):
		self.fixed_point_tracker = VectorizedPoint(self.top_point)
		self.add(self.fixed_point_tracker)
		return self
	
	def create_input_line(self):
		input_line = self.input_line = Arrow(LEFT, RIGHT)
		input_line.move_to(self.get_fixed_point())
		self.add(input_line)

	def create_link_CC(self):
		link_CC = self.link_CC = Arrow(LEFT, RIGHT)
		link_CC.move_to(self.get_edge_controller(1, RIGHT))
		self.add(link_CC)

	def create_controller(self):
		controller = self.controller = Rectangle()
		controller.set_width(self.box_width)
		controller.set_height(self.box_height)
		# controller.set_style(**self.controller_style)
		controller.move_to(self.link_CC.get_end() + (0.5 * self.box_width) * RIGHT)
		self.add(controller)

	def create_link_CP(self):
		link = self.link = Arrow(LEFT, RIGHT)
		link.move_to(self.controller.get_center() + (0.88 * self.box_width) * RIGHT)
		self.add(link)

	def create_plant(self):
		plant = self.plant = Rectangle()
		plant.set_width(self.box_width)
		plant.set_height(self.box_height)
		# plant.set_style(**self.controller_style)
		plant.move_to(self.link.get_end() + (0.5 * self.box_width) * RIGHT)
		self.add(plant)

	def create_output_line(self):
		output_line = self.output_line = Arrow(LEFT, RIGHT)
		output_line.set_length(3)
		output_line.move_to(self.plant.get_center() + (1.25 * self.box_width) * RIGHT)
		self.add(output_line)

	def add_feedback_line_in(self):
		splitter = Dot(self.output_line.get_center())
		line1 = Line(UP, DOWN)
		line1.stroke_width = 6
		line1.set_length(3)
		line1.move_to(self.output_line.get_center() + 1.5 * DOWN)
		line2 = self.fb_in_line2 = Arrow(RIGHT, LEFT)
		line2.set_length(3)
		line2.move_to(line1.get_end() + 1.5 * LEFT)
		fb_in_lines = self.fb_in_lines = VGroup(line1, line2)
		self.add(splitter, fb_in_lines)

	def create_sensor(self):
		sensor = self.sensor = Rectangle()
		sensor.set_width(self.box_width)
		sensor.set_height(self.box_height)
		# plant.set_style(**self.controller_style)
		sensor.move_to(self.fb_in_line2.get_end() + (0.5 * self.box_width) * LEFT)
		self.add(sensor)

	def create_feedback_line_out(self):
		line2_out = Arrow(DOWN, UP)
		line2_out.set_length(2.25)
		line2_out.move_to(self.get_edge_controller((0.5 + 2.25 / 3), DOWN))
		line1_out = Line(RIGHT, LEFT)
		line1_out.stroke_width = 6
		line1_out.set_length(abs(line2_out.get_start() - (self.sensor.get_center() - 0.5 * self.box_width)))
		line1_out.move_to(line2_out.get_start() +  (0.5 * line1_out.get_length()) * RIGHT)
		self.add(line2_out, line1_out)

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

	def get_edge_controller(self, distance, direction):
		return self.comparator.get_center() + distance * self.comparator_diamater * direction


class EquationOfTheSystem(Scene):
	def construct(self):
		eq = TexMobject("\\ddot{y}(t) + 3\\dot{y}(t) + 2y(t) = 3e(t)")
		transform_eq = TexMobject("\\ddot{y}(t) + 3\\dot{y}(t) + 2y(t) = 3e(t)")
		transform_eq = transform_eq.to_edge(UP)
		LT_eq = TexMobject("s^2Y(s)+3sY(s)+2Y(s)=3E(s)")
		open_eq = TexMobject("G(s)=\\frac{Y(s)}{E(s)}=\\frac{3}{s^2+3s+2}")
		self.play(Write(eq, run_time=2))
		self.wait(3)
		self.play(
			Transform(eq, LT_eq, run_time=1),
			# LaggedStart(Write(LT_eq, run_time=2))
		)
		self.wait(3)
		self.play(
			Transform(eq, open_eq, run_time=1),
			# LaggedStart(Write(LT_eq, run_time=2))
		)
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
