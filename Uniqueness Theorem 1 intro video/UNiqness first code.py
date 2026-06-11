from manim import *
import numpy as np
from scipy.spatial import ConvexHull
import random

config.frame_aspect_ratio = (16, 9)
config.frame_width = 10


def CheckMark(color=GREEN, scale=1):
    return VGroup(
        Line([0, 0, 0], [0.3, -0.3, 0], color=color, stroke_width=15),
        Line([0.3, -0.3, 0], [1, 0.4, 0], color=color, stroke_width=15)
    ).scale(scale)


def CrossMark(color=RED, scale=1):
    return VGroup(
        Line([-0.5, -0.5, 0], [0.5, 0.5, 0], color=color, stroke_width=15),
        Line([-0.5, 0.5, 0], [0.5, -0.5, 0], color=color, stroke_width=15)
    ).scale(scale)


class IntroTwoBoxes(Scene):
    def construct(self):
        bg = Rectangle(
            width=10,
            height=160 / 9,
            fill_color=["#000814", "#001B44"],  # deep → bright space blue
            fill_opacity=1,
            stroke_width=0
        )
        bg.move_to(ORIGIN)
        self.add(bg)

        # --- BOXES ---
        box1 = Rectangle(color=WHITE, height=4, width=7).shift(UP*3)
        box2 = Rectangle(color=WHITE, height=4, width=7).shift(DOWN*3)

        self.play(Create(box1), Create(box2))

        # --- VALID FIELD (TOP BOX) ---
        valid_field = self.create_dipole_field().shift(UP*3)

        # --- INVALID FIELD (BOTTOM BOX) ---
        invalid_field = self.create_invalid_field().shift(DOWN*3)

        self.play(
            LaggedStart(*[GrowArrow(a) for a in valid_field], lag_ratio=0.001),
            LaggedStart(*[GrowArrow(a)
                        for a in invalid_field], lag_ratio=0.001),
        )
        self.wait(0.5)

        # --- CHECKMARK AND X ---
        check = CheckMark(scale=1.5).move_to(box1.get_center())
        cross = CrossMark(scale=1.5).move_to(box2.get_center())

        self.play(FadeIn(check), FadeIn(cross))
        self.wait(1)

    # ----------------------------------------------------------
    # VALID ELECTRIC FIELD (dipole + tiny center charge)
    # ----------------------------------------------------------
    def create_dipole_field(self):
        arrows = VGroup()

        q1_pos = np.array([-1.5, 0, 0])
        q2_pos = np.array([1.5, 0, 0])

        q1 = 1
        q2 = -1

        for x in np.linspace(-3, 3, 15):
            for y in np.linspace(-1.5, 1.5, 10):
                p = np.array([x, y, 0])

                r1 = p - q1_pos
                r2 = p - q2_pos

                E1 = q1 * r1 / np.linalg.norm(r1)**3
                E2 = q2 * r2 / np.linalg.norm(r2)**3

                E = E1 + E2

                mag = np.linalg.norm(E)
                if mag > 1:
                    E = 2 * E / mag
                    mag = 2

                arrow = Arrow(
                    p,
                    p + 0.3 * E,
                    buff=0,
                    stroke_width=2
                )

                # BLUE → RED gradient
                color = interpolate_color(BLUE, RED, mag / 2)
                arrow.set_color(color)

                arrows.add(arrow)

        return arrows

    # ----------------------------------------------------------
    # INVALID FIELD (random-ish wrong field)
    # ----------------------------------------------------------
    def create_invalid_field(self):
        arrows = VGroup()

        q1_pos = np.array([-1.5, 0, 0])
        q2_pos = np.array([1.5, 0, 0])
        q3_pos = np.array([0, 0, 0])
        q1, q2, q3 = 1, -1, -0.1

        for x in np.linspace(-3, 3, 15):
            for y in np.linspace(-1.5, 1.5, 10):
                p = np.array([x, y, 0])

                r1 = p - q1_pos
                r2 = p - q2_pos
                r3 = p - q3_pos

                E = q1 * r1 / np.linalg.norm(r1)**3 + \
                    q2 * r2 / np.linalg.norm(r2)**3 + \
                    q3 * r3 / np.linalg.norm(r3)**3

                mag = np.linalg.norm(E)
                if mag > 1:
                    E = 2 * E / mag
                    mag = 2

                arrow = Arrow(
                    p,
                    p + 0.3 * E,
                    buff=0,
                    stroke_width=2
                )

                color = interpolate_color(BLUE, RED, mag / 2)
                arrow.set_color(color)

                arrows.add(arrow)

        return arrows


class RandomPotato(ThreeDScene):
    def construct(self):
        bg = Rectangle(
            width=100,
            height=1600 / 9,
            fill_color=["#000814", "#001B44"],
            fill_opacity=1,
            stroke_width=0
        )
        bg.set_z_index(-1)
        bg.move_to([0, 0, -10])
        self.add(bg)
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)

        random.seed(42)
        num_bumps = 3
        bumps = [
            (
                random.uniform(0.1, 0.2),
                random.randint(2, 6),
                random.randint(2, 6),
                random.uniform(0, 2 * PI),
                random.uniform(0, 2 * PI)
            )
            for _ in range(num_bumps)
        ]

        def potato_func(u, v):
            R = 2.0
            distortion = 0
            for amp, freq_u, freq_v, phase_u, phase_v in bumps:
                distortion += amp * \
                    np.sin(freq_u * u + phase_u) * np.cos(freq_v * v + phase_v)

            r = R + distortion
            x = r * np.sin(v) * np.cos(u)
            y = r * np.sin(v) * np.sin(u)
            z = r * np.cos(v)
            return np.array([x, y, z])

        potato = Surface(
            potato_func,
            resolution=(32, 32),
            u_range=[0, 2 * PI],
            v_range=[0, PI],
        )
        potato.set_color(GREEN)
        potato.set_z_index(2)
        potato.set_opacity(0.2)

        self.play(FadeIn(potato), run_time=1.5)
        self.wait(1)

        c1 = Sphere(radius=0.2).move_to(
            [2, 3, 0]).set_color(RED).set_opacity(1)
        c2 = Sphere(radius=0.2).move_to(
            [1, -3, 0]).set_color(BLUE).set_opacity(1)
        c3 = Sphere(radius=0.2).move_to(
            [-3, 1, 0]).set_color(RED).set_opacity(1)

        l1 = MathTex("q_1").next_to(c1, RIGHT)
        l2 = MathTex("q_2").next_to(c2, UP)
        l3 = MathTex("q_3").next_to(c3, LEFT)

        charges = VGroup(c1, l1, c2, l2, c3, l3)
        charges.set_z_index(1)

        self.play(FadeIn(charges), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(charges), run_time=1.5)
        self.wait(1)

        self.play(potato.animate.set_color(RED).set_opacity(0.5), run_time=0.5)

        arrow = Arrow(start=LEFT, end=RIGHT, color=YELLOW)
        arrow.scale(0.7)

        center = potato.get_center()
        radius = 3.0
        arrow.move_to(center + RIGHT * radius)

        arrow.rotate(PI)

        val_tracker = ValueTracker(1.0)

        phi_label = always_redraw(lambda:
                                  MathTex(
                                      f"\\Phi = {val_tracker.get_value():.2f}").to_corner(UR)
                                  )

        self.add(arrow, phi_label)
        self.wait(1)

        def rotate_arrow(mob, dt):

            speed = 1.0

            mob.rotate(
                angle=speed * dt,
                about_point=center
            )

        arrow.add_updater(rotate_arrow)

        self.play(
            val_tracker.animate.set_value(-1.0),
            run_time=6,
            rate_func=linear
        )

        arrow.remove_updater(rotate_arrow)
        self.wait(1)
        self.play(FadeOut(potato), FadeOut(arrow), FadeOut(phi_label))


class Stating(Scene):
    def construct(self):
        bg = Rectangle(
            width=10,
            height=160 / 9,
            fill_color=["#000814", "#001B44"],
            fill_opacity=1,
            stroke_width=0
        )
        bg.move_to(ORIGIN)
        self.add(bg)
        transition = Paragraph("Physics + Useful !?").scale(1)
        huh = Paragraph("Huh...!").scale(1)

        self.play(Write(transition))
        self.wait(1)
        self.play(FadeOut(transition))
        self.wait(0.2)
        self.play(Write(huh))
        self.wait(1.4)
        self.play(FadeOut(huh))


class IntroThreeBoxes(Scene):
    def construct(self):
        bg = Rectangle(
            width=10,
            height=160 / 9,
            fill_color=["#000814", "#001B44"],
            fill_opacity=1,
            stroke_width=0
        )
        bg.move_to(ORIGIN)
        self.add(bg)

        box1 = Rectangle(color=WHITE, height=3, width=7).shift(UP * 3.5)
        box2 = Rectangle(color=WHITE, height=3, width=7).shift(ORIGIN)
        box3 = Rectangle(color=WHITE, height=3, width=7).shift(DOWN * 3.5)

        self.play(Create(box1), Create(box2), Create(box3))

        valid_field = self.create_valid_field(box1)
        invalid_field_1 = self.create_invalid_field_A(box2)
        invalid_field_2 = self.create_invalid_field_B(box3)

        if len(valid_field) > 0:
            self.play(
                LaggedStart(*[GrowArrow(a)
                            for a in valid_field], lag_ratio=0.001),
                LaggedStart(*[GrowArrow(a)
                            for a in invalid_field_1], lag_ratio=0.001),
                LaggedStart(*[GrowArrow(a)
                            for a in invalid_field_2], lag_ratio=0.001),
                run_time=2
            )
        else:
            print("Warning: No arrows generated.")

        self.wait(0.5)

        check = CheckMark(scale=1.5).move_to(box1.get_center())
        cross1 = CrossMark(scale=1.5).move_to(box2.get_center())
        cross2 = CrossMark(scale=1.5).move_to(box3.get_center())

        self.play(FadeIn(check), FadeIn(cross1), FadeIn(cross2))
        self.wait(2)

    def clip_arrows_to_box(self, arrows, box):
        final_arrows = VGroup()
        box_center = box.get_center()
        box_width = box.width / 2
        box_height = box.height / 2

        for arrow in arrows:
            start = arrow.get_start()

            rel_x = abs(start[0] - box_center[0])
            rel_y = abs(start[1] - box_center[1])

            if rel_x < box_width and rel_y < box_height:
                final_arrows.add(arrow)

        return final_arrows

    def create_valid_field(self, box):
        arrows = VGroup()
        box_center = box.get_center()

        q1_pos = box_center + np.array([-4.0, 0, 0])
        q2_pos = box_center + np.array([4.0, 0, 0])
        q1, q2 = 1, 1

        for x in np.linspace(-3.5, 3.5, 15):
            for y in np.linspace(-1.5, 1.5, 8):
                p = box_center + np.array([x, y, 0])

                r1 = p - q1_pos
                r2 = p - q2_pos

                E1 = q1 * r1 / (np.linalg.norm(r1)**3 + 1e-5)
                E2 = q2 * r2 / (np.linalg.norm(r2)**3 + 1e-5)
                E = E1 + E2

                mag = np.linalg.norm(E)
                if mag > 0.01:
                    E = 0.6 * E / mag
                    mag = 0.6

                arrow = Arrow(
                    p,
                    p + E,
                    buff=0,
                    stroke_width=3
                )

                color = interpolate_color(BLUE, YELLOW, min(mag / 0.5, 1))
                arrow.set_color(color)
                arrows.add(arrow)

        return self.clip_arrows_to_box(arrows, box)

    def create_invalid_field_A(self, box):
        arrows = VGroup()
        box_center = box.get_center()

        # Charge below the box
        q1_pos = box_center + np.array([0, -4.0, 0])
        q1 = 2.0

        for x in np.linspace(-3.5, 3.5, 15):
            for y in np.linspace(-1.5, 1.5, 8):
                p = box_center + np.array([x, y, 0])

                r1 = p - q1_pos
                E = q1 * r1 / (np.linalg.norm(r1)**3 + 1e-5)

                mag = np.linalg.norm(E)
                if mag > 0.01:
                    E = 0.6 * E / mag

                arrow = Arrow(p, p + E, buff=0, stroke_width=3)
                arrow.set_color(RED)
                arrows.add(arrow)

        return self.clip_arrows_to_box(arrows, box)

    def create_invalid_field_B(self, box):
        arrows = VGroup()
        box_center = box.get_center()

        # Charges above the box
        q1_pos = box_center + np.array([-4.0, 4.0, 0])
        q2_pos = box_center + np.array([4.0, 4.0, 0])
        q1, q2 = 1.5, 1.5

        for x in np.linspace(-3.5, 3.5, 15):
            for y in np.linspace(-1.5, 1.5, 8):
                p = box_center + np.array([x, y, 0])

                r1 = p - q1_pos
                r2 = p - q2_pos

                E1 = q1 * r1 / (np.linalg.norm(r1)**3 + 1e-5)
                E2 = q2 * r2 / (np.linalg.norm(r2)**3 + 1e-5)
                E = E1 + E2

                mag = np.linalg.norm(E)
                if mag > 0.01:
                    E = 0.6 * E / mag

                arrow = Arrow(p, p + E, buff=0, stroke_width=3)
                arrow.set_color(GREEN)
                arrows.add(arrow)

        return self.clip_arrows_to_box(arrows, box)


class congrats(Scene):
    def construct(self):
        bg = Rectangle(
            width=10,
            height=160 / 9,
            fill_color=["#000814", "#001B44"],
            fill_opacity=1,
            stroke_width=0
        )
        bg.move_to(ORIGIN)
        self.add(bg)
        text = Text("Congratulations! ").scale(1.5)
        self.play(Write(text))
        self.wait(2)


class Outro(Scene):
    def construct(self):
        bg = Rectangle(
            width=10,
            height=160 / 9,
            fill_color=["#000814", "#001B44"],
            fill_opacity=1,
            stroke_width=0
        )
        bg.move_to(ORIGIN)
        self.add(bg)
        next = Text("Next Video").scale(1.4)
        self.play(Write(next.move_to(ORIGIN)))
        self.wait(2)
        self.play(FadeOut(next))

        text1 = Text("The First Uniqueness ").scale(1.4)
        text2 = Text("Theorem of").scale(1.4)
        text3 = Text("Electrostatics").scale(1.4)
        self.play(Write(text1.move_to(ORIGIN + UP)))
        self.play(Write(text2.next_to(text1, DOWN)))
        self.play(Write(text3.next_to(text2, DOWN)))
        self.wait(2)
