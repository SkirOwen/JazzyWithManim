from manimlib.imports import *
from from_3b1b.active.diffyq.part1.shared_constructs import *
# from from_3b1b.active.diffyq.part1.pendulum import Pendulum
import matplotlib.pyplot as plt


class InvertedPendulumCart(VGroup):
    CONFIG = {
        "length": 3,
        "gravity": 9.81,
        "weight_diameter": 0.5,
        "cart_width": 2,
        "cart_height": 1,
        "initial_theta": PI -0.01,
        "initial_position": -2,
        "omega": 0,
        "speed": 0,
        "damping": 0.5,
        "friction": 0.5,
        "cart_mass": 2,
        "weight_mass": 1,
        "force": 0,
        "torque": 0,
        "moment_of_inertia": 1,
        "top_point": 2 * UP,
        "rod_style": {
            "stroke_width": 3,
            "stroke_color": LIGHT_GREY,
            "sheen_direction": UP,
            "sheen_factor": 1,
        },
        "cart_style": {
            "stroke_color": WHITE,
            "stroke_width": 2,
        },
        "weight_style": {
            "stroke_width": 0,
            "fill_opacity": 1,
            "fill_color": GREY_BROWN,
            "sheen_direction": UL,
            "sheen_factor": 0.5,
            "background_stroke_color": BLACK,
            "background_stroke_width": 3,
            "background_stroke_opacity": 0.5,
        },
        "rail_style": {
            "stroke_color": WHITE,
            "stroke_width": 2,
        },
        "dashed_line_config": {
            "num_dashes": 25,
            "stroke_color": BLACK,
            "stroke_width": 2,
        },
        "angle_arc_config": {
            "radius": 1,
            "stroke_color": WHITE,
            "stroke_width": 2,
        },
        "velocity_vector_config": {
            "color": RED,
        },
        "theta_label_height": 0.25,
        "set_theta_label_height_cap": False,
        "n_steps_per_frame": 100,
        "include_theta_label": True,
        "include_velocity_vector": False,
        "velocity_vector_multiple": 0.5,
        "max_velocity_vector_length_to_length_ratio": 0.5,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_fixed_point()
        self.create_cart()
        
        self.create_rod()
        self.create_weight()
        self.create_rail()
        self.rotating_group = VGroup(self.rod, self.weight)
        self.moving_group = VGroup(self.cart, self.rotating_group)
        self.create_dashed_line()
        self.create_angle_arc()
        if self.include_theta_label:
            self.add_theta_label()
        if self.include_velocity_vector:
            self.add_velocity_vector()

        self.set_theta(self.initial_theta)
        self.set_position(self.initial_position)
        self.create_ori()
        self.update()

    

    def create_fixed_point(self):
        self.fixed_point_tracker = VectorizedPoint(ORIGIN)
        self.add(self.fixed_point_tracker)
        return self

    def create_cart(self):
        cart = self.cart = Rectangle()
        cart.set_width(self.cart_width)
        cart.set_height(self.cart_height)
        cart.set_style(**self.cart_style)
        cart.move_to(self.get_fixed_point())
        self.add(cart)

    def create_rail(self):
        rail = self.rail = Line(LEFT, RIGHT)
        rail.set_length(20)
        rail.set_style(**self.rail_style)
        self.add(rail)

    def create_ori(self):
        dot = self.dot = Dot(self.get_position())
        self.add(dot)

    def create_rod(self):
        rod = self.rod = Line(UP, DOWN)
        rod.set_height(self.length)
        rod.set_style(**self.rod_style)
        rod.move_to(self.get_fixed_point(), UP)
        # rod.move_to(self.cart.get_center(), UP)
        self.add(rod)

    def create_weight(self):
        weight = self.weight = Circle()
        weight.set_width(self.weight_diameter)
        weight.set_style(**self.weight_style)
        weight.move_to(self.rod.get_end())
        self.add(weight)

    def create_dashed_line(self):
        line = self.dashed_line = DashedLine(
            self.get_fixed_point(),
            self.get_fixed_point() + self.length * DOWN,
            **self.dashed_line_config
        )
        line.add_updater(
            lambda l: l.move_to(self.get_fixed_point(), UP)
        )
        self.add_to_back(line)

    def create_angle_arc(self):
        self.angle_arc = always_redraw(lambda: Arc(
            arc_center=self.get_fixed_point(),
            start_angle=-90 * DEGREES,
            angle=self.get_arc_angle_theta(),
            **self.angle_arc_config,
        ))
        # self.add(self.angle_arc)

    def get_arc_angle_theta(self):
        return self.get_theta()

    def add_velocity_vector(self):
        def make_vector():
            omega = self.get_omega()
            theta = self.get_theta()
            mvlr = self.max_velocity_vector_length_to_length_ratio
            max_len = mvlr * self.rod.get_length()
            vvm = self.velocity_vector_multiple
            multiple = np.clip(
                vvm * omega, -max_len, max_len
            )
            vector = Vector(
                multiple * RIGHT,
                **self.velocity_vector_config,
            )
            vector.rotate(theta, about_point=ORIGIN)
            vector.shift(self.rod.get_end())
            return vector

        self.velocity_vector = always_redraw(make_vector)
        self.add(self.velocity_vector)
        return self

    def add_theta_label(self):
        self.theta_label = always_redraw(self.get_label)
        self.add(self.theta_label)

    def get_label(self):
        label = TexMobject("\\theta")
        label.set_height(self.theta_label_height)
        if self.set_theta_label_height_cap:
            max_height = self.angle_arc.get_width()
            if label.get_height() > max_height:
                label.set_height(max_height)
        top = self.get_fixed_point()
        arc_center = self.angle_arc.point_from_proportion(0.5)
        vect = arc_center - top
        norm = get_norm(vect)
        vect = normalize(vect) * (norm + self.theta_label_height)
        label.move_to(top + vect)
        return label

    #
    def get_theta(self):
        theta = self.rod.get_angle() - self.dashed_line.get_angle()
        theta = (theta + PI) % TAU - PI
        return theta

    def set_theta(self, theta):
        self.rotating_group.rotate(
            theta - self.get_theta()
        )
        self.rotating_group.shift(
            # self.get_fixed_point() - self.rod.get_start(),
            self.get_position() - self.rod.get_start(),
        )
        return self

    def get_omega(self):
        return self.omega

    def set_omega(self, omega):
        self.omega = omega
        return self

    def get_fixed_point(self):
        return self.fixed_point_tracker.get_location()

    def get_position(self):
        position = self.cart.get_center()
        return position

    def set_position(self, position):
        self.moving_group.shift(
            (position * RIGHT) - self.get_position()
        )
        return self

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.speed = speed
        return self

    #
    def start_swinging(self):
        self.add_updater(InvertedPendulumCart.update_by_gravity)

    def end_swinging(self):
        self.remove_updater(InvertedPendulumCart.update_by_gravity)

    # def of the ODE
    def update_by_gravity(self, dt):
        theta = self.get_theta()
        omega = self.get_omega()
        position = self.get_position()
        speed = self.get_speed()
        nspf = self.n_steps_per_frame
        for x in range(nspf):
            d_theta = omega * dt / nspf
            d_position = speed * dt / nspf
            # d_speed = self.force / (self.cart_mass + self.weight_mass) * dt / nspf

            # d_omega = op.add(
            #     -self.damping * omega,
            #     -(self.gravity / self.length) * np.sin(theta),
            # ) * dt / nspf

            # d_omega = op.add(
            #     -(self.weight_mass / self.moment_of_inertia * self.gravity * self.length * np.sin(theta)),
            #     -(self.length / self.moment_of_inertia * np.cos(theta))
            # ) * dt / nspf 

            # d_speed = op.truediv(
            #     (op.add(
            #         ((self.moment_of_inertia + self.weight_mass * self.length**2) * d_omega),
            #         (self.weight_mass * self.gravity * np.sin(theta))
            #     )),
            #     (- self.weight_mass * self.length * np.cos(theta))
            # ) * dt / nspf
            d_speed = op.truediv(
                (op.add(
                    op.add(
                        (-self.friction * speed + self.force + np.cos(theta) * self.torque / self.length),
                        (self.weight_mass * self.gravity * np.cos(theta) * np.sin(theta))),
                    (self.weight_mass * self.length * d_theta**2 * np.sin(theta)))),
                (self.cart_mass + self.weight_mass - self.weight_mass * np.cos(theta)**2)
            ) * dt / nspf
            
            d_omega = op.add(
                op.add(
                    (self.torque / (self.weight_mass * self.length**2)),
                    (d_speed * np.cos(theta) * self.force / self.length)),
                (-self.damping * omega)-(self.gravity / self.length * np.sin(theta))
            ) * dt / nspf
            
            theta += d_theta
            position += d_position
            omega += d_omega
            speed += d_speed
        self.set_theta(theta)
        self.set_position(position)
        self.set_omega(omega)
        self.set_speed(speed)
        return self


class IntroducePendulum(Scene):
    CONFIG = {
        "pendulum_config": {
            "length": 3,
            "gravity": 9.81,
            "weight_diameter": 0.5,
            "cart_width": 2,
            "cart_height": 1,
            "initial_theta": PI + 0.1,
            "initial_position": -3,
            "omega": 0,
            "speed": 0,
            "damping": 0,
            "friction": 0,
            "cart_mass": 2,
            "weight_mass": 1,
            "force": 0,
            "torque": 0,
            "moment_of_inertia": 1,
            "top_point": 2 * UP,
            "include_theta_label": False,

        },
        "theta_vs_t_axes_config": {
            "y_max": PI / 4,
            "y_min": -PI / 4,
            "y_axis_config": {
                "tick_frequency": PI / 16,
                "unit_size": 2,
                "tip_length": 0.3,
            },
            "x_max": 12,
            "axis_config": {
                "stroke_width": 2,
            }
        },
    }

    # def setup(self):
    #     MovingCameraScene.setup(self)
    #     PiCreatureScene.setup(self)

    def construct(self):
        self.add_pendulum()
        self.label_pendulum()

    def add_pendulum(self):
        pendulum = self.pendulum = InvertedPendulumCart(**self.pendulum_config)
        pendulum.start_swinging()
        # frame = self.camera_frame
        # frame.save_state()
        # frame.scale(0.5)
        # frame.move_to(pendulum.dashed_line)

        # self.add(pendulum, frame)
        self.add(pendulum)
        self.wait()

    def label_pendulum(self):
        pendulum = self.pendulum
        # label = pendulum.theta_label
        # rect = SurroundingRectangle(label, buff=0.5 * SMALL_BUFF)
        # rect.add_updater(lambda r: r.move_to(label))

        # self.play(
        #     ShowCreationThenFadeOut(rect),
        # )
        self.wait(20)

