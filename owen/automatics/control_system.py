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


class RLCCircuit(VGroup):
	CONFIG = {
		"generator_diameter": 1,
		"generator_style": {
			"stroke_color": WHITE,
		},
		"resistance_style": {
			"stroke_color": WHITE,
		},
	}

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.create_generator()
		self.create_gen_res()
		self.create_resistance()
		self.create_res_coil()
		self.create_coil()
		self.create_c_gen()
		self.create_cap_circuit()
		self.create_capacitor()
		self.add_labels()

	def create_generator(self):
		generator = self.generator = Circle()
		generator.set_width(self.generator_diameter)
		generator.scale(2)
		generator.set_style(**self.generator_style)
		generator.move_to(3.5 * LEFT)
		sine1 = Arc(0, PI)
		sine1.set_width(0.75)
		sine1.move_to(self.generator.get_center() + 0.75 / 2 * LEFT + 0.75 / 4 * UP)
		sine2 = Arc(0, -PI)
		sine2.set_width(0.75)
		sine2.move_to(self.generator.get_center() + 0.75 / 2 * RIGHT + 0.75 / 4 * DOWN)
		sine_wave = VGroup(sine1, sine2)
		self.add(generator, sine_wave)

	def create_gen_res(self):
		line1_in = self.line1_in = Line(DOWN, UP)
		line1_in.set_length(1)
		line1_in.move_to(self.generator.get_center() + 1.5 * UP)
		line2_in = self.line2_in = Line(LEFT, RIGHT)
		line2_in.set_length(1.5)
		line2_in.move_to(line1_in.get_end() + 0.75 * RIGHT)
		self.add(line1_in, line2_in)

	def create_resistance(self):
		resistance = self.resistance = Rectangle()
		resistance.set_height(0.75)
		resistance.set_width(1.5)
		resistance.set_style(**self.resistance_style)
		resistance.move_to(self.line2_in.get_end() + 0.75 * RIGHT)
		self.add(resistance)

	def create_res_coil(self):
		line1_coil = self.line1_coil = Line(LEFT, RIGHT)
		line1_coil.set_length(3.5)
		line1_coil.move_to(self.resistance.get_center() + 2.5 * RIGHT)
		line2_coil = self.line2_coil = Line(UP, DOWN)
		line2_coil.set_length(1)
		line2_coil.move_to(line1_coil.get_end() + 0.5 * DOWN)
		self.add(line1_coil, line2_coil)

	def create_coil(self):
		coil1 = Arc(PI / 2, -PI)
		coil1.set_width(0.2)
		coil1.move_to(self.line2_coil.get_end() + 0.2 * DOWN + 0.1 * RIGHT)
		coil2 = Arc(PI / 2, -PI)
		coil2.set_width(0.2)
		coil2.move_to(coil1.get_end() + 0.2 * DOWN + 0.1 * RIGHT)
		coil3 = Arc(PI / 2, -PI)
		coil3.set_width(0.2)
		coil3.move_to(coil2.get_end() + 0.2 * DOWN + 0.1 * RIGHT)
		coil4 = Arc(PI / 2, -PI)
		coil4.set_width(0.2)
		coil4.move_to(coil3.get_end() + 0.2 * DOWN + 0.1 * RIGHT)
		coil5 = self.coil_out = Arc(PI / 2, -PI)
		coil5.set_width(0.2)
		coil5.move_to(coil4.get_end() + 0.2 * DOWN + 0.1 * RIGHT)
		coil = VGroup(coil1, coil2, coil3, coil4, coil5)
		self.add(coil)

	def create_c_gen(self):
		line1 = Line(UP, DOWN)
		line1.set_length(1)
		line1.move_to(self.coil_out.get_end() + 0.5 * DOWN)
		line2 = Line(DOWN, UP)
		line2.set_length(1)
		line2.move_to(self.generator.get_center() + 1.5 * DOWN)
		line3 = self.line_to_gen =  Line(RIGHT, LEFT)
		line3.set_length(abs(line2.get_start() - line1.get_end()))
		line3.move_to(line1.get_end() + 0.5 * line3.get_length() * LEFT)
		line_out = VGroup(line1, line2, line3)
		self.add(line_out)


	def create_cap_circuit(self):
		dot1 = Dot(self.line_to_gen.get_center() + RIGHT)
		dot2 = Dot(self.line_to_gen.get_center() * np.array([1,-1,1]) + RIGHT)
		line1 = self.line_out_cap = Line(DOWN, UP)
		line1.set_length(1.8)
		line1.move_to(dot1.get_center() + 0.9 * UP)
		line2 = self.line_in_cap = Line(UP, DOWN)
		line2.set_length(1.8)
		line2.move_to(dot2.get_center() + 0.9 * DOWN)

		self.add(dot1, dot2, line1, line2)

	def create_capacitor(self):
		top = Line(LEFT, RIGHT)
		top.set_length(1)
		top.move_to(self.line_in_cap.get_end())
		bottom = Line(LEFT, RIGHT)
		bottom.set_length(1)
		bottom.move_to(self.line_out_cap.get_end())
		self.add(top, bottom)

	def add_labels(self):
		r_label = TextMobject("R")
		r_label.move_to(self.resistance.get_center() + 0.7 * DOWN)
		l_label = TextMobject("L")
		l_label.move_to(3.5 * RIGHT)
		c_label = TextMobject("C")
		c_label.move_to(ORIGIN)

		vi_arrow = Arrow(DOWN, UP)
		vi_label = TexMobject("V_{i}")
		vi_arrow.set_length(4)
		vi_arrow.move_to(5 * LEFT)
		vi_label.move_to(vi_arrow.get_center() + 0.5 * LEFT)
		vo_arrow = Arrow(DOWN, UP)
		vo_label = TexMobject("V_{0} = \\dot{x}")
		vo_arrow.set_length(4)
		vo_arrow.move_to(4 * RIGHT)
		vo_label.move_to(vo_arrow.get_center() + 1 * RIGHT)
		self.add(
			r_label, c_label, l_label,
			vi_arrow, vi_label,
			vo_arrow, vo_label
		)



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


class RLCfilter(Scene):
	CONFIG = {
		"RLC_config": {
			"generator_diameter": 1,
		}
	}
	def construct(self):
		title = TextMobject("RLC Filter")
		title.to_corner(UP + LEFT)
		

		RLC_circuit = RLCCircuit(**self.RLC_config)

		eq = TexMobject(
			"V_{i} = \\dot{x} + RC\\ddot{x} + \\frac{R}{L}x"
		)

		LT = TexMobject(
			"V_{i}(s) = RC^2X(s)+sX(s)+\\frac{R}{L}X(s)"
		)
		
		tf = TexMobject(
			"\\frac{X(s)}{V_{i}(s)} = \\frac{1}{RCs^2+s+\\frac{R}{L}}"
		)

		self.play(
			FadeInFrom(title, LEFT),
			Write(RLC_circuit, run_time=2)
		)
		self.wait(1)
		self.play(Transform(RLC_circuit, eq))
		self.wait(1.5)
		self.play(Transform(RLC_circuit, LT))
		self.wait(1.5)
		self.play(Transform(RLC_circuit, tf))
		self.wait()


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
