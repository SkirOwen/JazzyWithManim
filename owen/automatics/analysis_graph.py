from manimlib.imports import *


class BodeDiagram(Scene):
	CONFIG = {
		"step_size": 0.05,
		"axes_config": {
			"x_min": -1,
			"x_max": 11,
			"y_min": -10,
			"y_max": 100,
			"y_axis_config": {
				"unit_size": 0.06,
				"tick_frequency": 10,
			},
		},
		"y_labels": range(20, 100, 20),
		"graph_x_min": 0,
		"graph_x_max": 10,
		"midpoint": 5,
		"max_temp": 90,
		"min_temp": 10,
		"wait_time": 30,
		"default_n_rod_pieces": 20,
		"alpha": 1.0,
	}
	
	def construct(self):
		self.setup_axes()
		self.setup_graph()
		self.wait()

	def setup_axes(self):
		axes = Axes(**self.axes_config)
		axes.center().to_edge(UP)

		y_label = axes.get_y_axis_label("\\text{Temperature}")
		y_label.to_edge(UP)
		axes.y_axis.label = y_label
		axes.y_axis.add(y_label)
		axes.y_axis.add_numbers(*self.y_labels)

		self.axes = axes
		self.y_label = y_label

	def setup_graph(self):
		graph = self.axes.get_graph(
			self.initial_function,
			x_min=self.graph_x_min,
			x_max=self.graph_x_max,
			step_size=self.step_size,
			discontinuities=[self.midpoint],
		)
		graph.color_using_background_image("VerticalTempGradient")

		self.graph = graph

	def temp_func(self, x, t):
		new_x = TAU * x / 10
		return 50 + 20 * np.sum([
			amp * np.sin(freq * new_x) *
			np.exp(-(self.alpha * freq**2) * t)
			for freq, amp in self.freq_amplitude_pairs
		])

	def initial_function(self, x, time=0):
		return self.temp_func(x, 0)

class NyquistDiagram(Scene):
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
