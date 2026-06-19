from manim import *
import numpy as np


class GymAdvertisement(ThreeDScene):
    def construct(self):
        #config.frame_height = 8
        #config.frame_width = 14.22  # 16:9

        self.intro_sequence()
        self.safe_chair_demo()

        self.dangerous_chair_demo()
        self.force_visualization()
        self.dumbbell_imbalance_demo()
        self.gym_pitch()

    def intro_sequence(self):
        # Getting injured at the gym is every man's nightmare. But it often starts with something we all think is harmless.

        title = Text(
            "The Chair Challenge",
            font_size=48,
            color=BLUE,
            weight=BOLD
        ).to_edge(UP)

        subtitle = Text(
            "Looks harmless, right?",
            font_size=32,
            color=WHITE
        ).next_to(title, DOWN)

        self.play(
            Write(title),
            FadeIn(subtitle, shift=UP),
            run_time=2
        )
        self.wait(1)


        self.play(FadeOut(VGroup(title, subtitle), shift=UP), run_time=1)

    def safe_chair_demo(self):
        # You've seen the chair challenge. Looks easy, right? Anybody can pick up a chair.
        # When you hold it from the top, the centre of mass hangs directly beneath your hand. Your force and the chair's weight lie on the same line. No rotation. Almost zero effort, harmless…

        leg_height = 3
        leg_width = 0.3
        leg_depth = 0.3


        WOOD_COLOR = "#8B6914"
        METAL_COLOR = "#C0C0C0"

        leg_fr = Prism(dimensions=[leg_width, leg_height, leg_depth], fill_color=WOOD_COLOR).move_to(
            [1, -leg_height / 2, 1])
        leg_fl = Prism(dimensions=[leg_width, leg_height, leg_depth], fill_color=WOOD_COLOR).move_to(
            [-1, -leg_height / 2, 1])
        leg_br = Prism(dimensions=[leg_width, leg_height, leg_depth], fill_color=WOOD_COLOR).move_to(
            [1, -leg_height / 2, -1])
        leg_bl = Prism(dimensions=[leg_width, leg_height, leg_depth], fill_color=WOOD_COLOR).move_to(
            [-1, -leg_height / 2, -1])
        seat = Prism(dimensions=[2.5, 0.2, 2.5], fill_color=WOOD_COLOR).move_to([0, 0, 0])
        backrest = Prism(dimensions=[0.2, 2.5, 2.5], fill_color=WOOD_COLOR).move_to([1, 1.25, 0])

        chair = VGroup(leg_fr, leg_fl, leg_br, leg_bl, seat, backrest)
        chair.rotate(15 * DEGREES, Z_AXIS).rotate(10 * DEGREES, Y_AXIS).shift(DOWN)


        glow = Circle(
            radius=2.5,
            color=GREEN,
            fill_opacity=0.1,
            stroke_width=0
        ).move_to(chair.get_center())

        self.play(
            ShowIncreasingSubsets(chair),
            FadeIn(glow, scale=0.5, run_time=1),
            run_time=3
        )
        self.wait(1)

        grip_point = chair.get_edge_center(UP) + np.array([0, 0.5, 0])
        safe_indicator = Dot3D(
            point=grip_point,
            color=GREEN,
            radius=0.15
        )
        pulse = Circle(
            radius=0.2,
            color=GREEN,
            fill_opacity=0.3
        ).move_to(grip_point)

        self.play(
            FadeIn(safe_indicator, scale=2),
            Create(pulse),
            run_time=1
        )

        self.play(
            pulse.animate.scale(3).set_opacity(0),
            run_time=2,
            rate_func=rate_functions.ease_out_sine
        )
        self.remove(pulse)

        hand_end = grip_point + np.array([0, 1, 0])
        hands_force = Arrow3D(
            start=grip_point,
            end=hand_end,
            color=GREEN,
            thickness=0.01
        )

        com = chair.get_center_of_mass() + np.array([0, 0.7, 0])
        weight_end = chair.get_center_of_mass() + np.array([0, -1, 0])
        weight_force = Arrow3D(
            start=com,
            end=weight_end,
            color=BLUE,
            thickness=0.01
        )

        hand_label = Text("Force", color=GREEN, font_size=24).next_to(hand_end, UP)
        weight_label = Text("Weight", color=BLUE, font_size=24).next_to(weight_end, DOWN)

        carrier = Line3D(
            start=hand_end + np.array([0, 0.5, 0]),
            end=weight_end + np.array([0, -1, 0]),
            color=GREEN,
            thickness=0.005
        )

        self.play(
            GrowArrow(hands_force),
            GrowArrow(weight_force),
            Write(hand_label),
            Write(weight_label),
            run_time=2
        )
        self.wait(0.5)

        self.play(Create(carrier), run_time=1.5)
        self.wait(1)

        safe_text = Text(
            "✓ Forces align - No rotation",
            color=GREEN,
            font_size=30
        ).to_edge(DOWN)

        self.play(Write(safe_text), run_time=1.5)
        self.wait(2)

        self.play(
            FadeOut(VGroup(chair, glow, safe_indicator, hands_force, weight_force,
                           hand_label, weight_label, carrier, safe_text)),
            run_time=1.5
        )

    def dangerous_chair_demo(self):
        # But grab it by the leg… and everything changes. Now gravity is pulling down far away from your grip. The two forces are far apart. You're no longer just lifting weight you're fighting a rotational force that wants to twist the chair out of your hand.

        leg_height = 3
        leg_width = 0.3
        leg_depth = 0.3
        WOOD_COLOR = "#8B6914"

        leg_fr = Prism(dimensions=[leg_width, leg_height, leg_depth], fill_color=WOOD_COLOR).move_to(
            [1, -leg_height / 2, 1])
        leg_fl = Prism(dimensions=[leg_width, leg_height, leg_depth], fill_color=WOOD_COLOR).move_to(
            [-1, -leg_height / 2, 1])
        leg_br = Prism(dimensions=[leg_width, leg_height, leg_depth], fill_color=WOOD_COLOR).move_to(
            [1, -leg_height / 2, -1])
        leg_bl = Prism(dimensions=[leg_width, leg_height, leg_depth], fill_color=WOOD_COLOR).move_to(
            [-1, -leg_height / 2, -1])
        seat = Prism(dimensions=[2.5, 0.2, 2.5], fill_color=WOOD_COLOR).move_to([0, 0, 0])
        backrest = Prism(dimensions=[0.2, 2.5, 2.5], fill_color=WOOD_COLOR).move_to([1, 1.25, 0])

        chair = VGroup(leg_fr, leg_fl, leg_br, leg_bl, seat, backrest)
        chair.rotate(15 * DEGREES, Z_AXIS).rotate(10 * DEGREES, Y_AXIS).shift(DOWN).scale(0.7)


        self.move_camera(zoom=1.3, frame_center=chair.get_center(), run_time=1.5)


        self.play(
            chair.animate.rotate(-15 * DEGREES, Z_AXIS).rotate(-10 * DEGREES, Y_AXIS),
            chair.animate.set_color(RED_A),
            run_time=2,
            rate_func=rate_functions.ease_in_quad
        )

        danger_glow = Circle(
            radius=2,
            color=RED,
            fill_opacity=0.15,
            stroke_width=0
        ).move_to(chair.get_center())

        self.play(FadeIn(danger_glow), run_time=1)

        grip_point = leg_fr.get_edge_center(DOWN) + np.array([0.15, 0, 0])
        danger_indicator = Dot3D(
            point=grip_point,
            color=RED,
            radius=0.15
        )

        danger_pulses = VGroup(*[
            Circle(
                radius=0.2 * i,
                color=RED,
                fill_opacity=0.3 - i * 0.05,
                stroke_width=2
            ).move_to(grip_point)
            for i in range(1, 4)
        ])

        self.play(
            FadeIn(danger_indicator, scale=2),
            *[Create(pulse) for pulse in danger_pulses],
            run_time=1.5
        )

        self.play(
            *[pulse.animate.scale(3).set_opacity(0) for pulse in danger_pulses],
            run_time=2,
            rate_func=rate_functions.ease_out_sine
        )
        self.remove(*danger_pulses)

        hand_end = grip_point + np.array([0, 1, 0])
        hands_force = Arrow3D(
            start=grip_point,
            end=hand_end,
            color=RED,
            thickness=0.01
        )

        com = chair.get_center_of_mass() + np.array([0, 0.7, 0])
        weight_end = chair.get_center_of_mass() + np.array([0, -1.5, 0])
        weight_force = Arrow3D(
            start=com,
            end=weight_end,
            color=BLUE,
            thickness=0.01
        )

        weight_t = CurvedArrow(
            start_point=[1.5, -1, 0],
            end_point=[0, -2.5, 0],
            angle=3 * PI / 2,
            stroke_color=YELLOW
        )

        self.play(
            GrowArrow(hands_force),
            GrowArrow(weight_force),
            run_time=1.5
        )
        self.wait(0.5)

        # To stop it, your grip must do two things: hold the weight and generate a massive opposite torque.
        self.play(Create(weight_t), run_time=2)
        self.wait(1)

        self.play(FadeOut(weight_force), run_time=1)
        self.wait()

        # Here things get dangerous because the real weak link isn't your muscle, it's the ligaments and tendons in your wrist affected by forces your wrist isn't made to handle, forces that doesn't directly push on your wrist movement range.

        wrist_warning = Text(
            "Your wrist isn't made for this!",
            color=RED,
            font_size=32,
            weight=BOLD
        ).to_edge(DOWN)

        self.play(Write(wrist_warning), run_time=1.5)
        self.wait(2)

        self.play(
            FadeOut(VGroup(chair, danger_glow, danger_indicator, hands_force,
                           weight_force, weight_t, wrist_warning)),
            run_time=2
        )

        self.move_camera(zoom=1, run_time=1.5)

    def force_visualization(self):
        # and the same goes for unbalanced dumbbells, or any unbalanced weight that has its center of mass shifted accidentally by lack of precision

       title = Text(
            "The Physics of wrist and ankle Injury",
            color=YELLOW,
            font_size=40,
            weight=BOLD
        ).to_edge(UP)

       self.play(Write(title), run_time=1.5)

       safe_diagram = self.create_safe_diagram()

       danger_diagram = self.create_danger_diagram()


       safe_diagram.shift(LEFT * 3)
       danger_diagram.shift(RIGHT * 3)

       safe_label = Text("SAFE", color=GREEN, font_size=30, weight=BOLD).next_to(safe_diagram, UP)
       danger_label = Text("DANGEROUS", color=RED, font_size=30, weight=BOLD).next_to(danger_diagram, UP)

       self.play(
            FadeIn(safe_diagram, scale=0.5),
            FadeIn(danger_diagram, scale=0.5),
            Write(safe_label),
            Write(danger_label),
            run_time=2
        )

       safe_torque_bar = Rectangle(
            height=0.3,
            width=0.01,
            color=GREEN
       ).next_to(safe_diagram, DOWN, buff=0.5)

       danger_torque_bar = Rectangle(
            height=0.3,
            width=0.01,
            color=RED
       ).next_to(danger_diagram, DOWN, buff=0.5)

       safe_torque_label = Text("Torque: 0", color=GREEN, font_size=20).next_to(safe_torque_bar, DOWN)
       danger_torque_label = Text("Torque: HIGH", color=RED, font_size=20).next_to(danger_torque_bar, DOWN)

       self.play(
            FadeIn(safe_torque_bar),
            FadeIn(danger_torque_bar),
            Write(safe_torque_label),
            Write(danger_torque_label),
            run_time=1.5
       )

       self.play(
            danger_torque_bar.animate.set_width(3),
            danger_torque_bar.animate.set_color(YELLOW),
            run_time=2,
            rate_func=rate_functions.ease_out_quad
       )

       self.play(
            Flash(danger_diagram, color=RED, line_length=0.3),
            run_time=1
       )

       self.wait(1.5)
       self.play(FadeOut(VGroup(title, safe_diagram, danger_diagram, safe_label,
                                 danger_label, safe_torque_bar, danger_torque_bar,
                                 safe_torque_label, danger_torque_label)), run_time=1.5)

    def create_safe_diagram(self):
        center = Dot3D(color=WHITE, radius=0.1)
        force_up = Arrow3D(
            start=center.get_center() + np.array([0, -0.5, 0]),
            end=center.get_center() + np.array([0, 0.5, 0]),
            color=GREEN
        )
        force_down = Arrow3D(
            start=center.get_center() + np.array([0, 0.5, 0]),
            end=center.get_center() + np.array([0, -0.5, 0]),
            color=BLUE
        )
        return VGroup(center, force_up, force_down)

    def create_danger_diagram(self):
        center = Dot3D(color=WHITE, radius=0.1)
        force_up = Arrow3D(
            start=center.get_center() + np.array([-0.5, -0.5, 0]),
            end=center.get_center() + np.array([-0.5, 0.5, 0]),
            color=RED
        )
        force_down = Arrow3D(
            start=center.get_center() + np.array([0.5, 0.5, 0]),
            end=center.get_center() + np.array([0.5, -0.5, 0]),
            color=BLUE
        )
        torque_curve = CurvedArrow(
            start_point=center.get_center() + np.array([-0.3, 0, 0]),
            end_point=center.get_center() + np.array([0.3, 0, 0]),
            angle=PI / 4,
            color=YELLOW
        )
        return VGroup(center, force_up, force_down, torque_curve)

    def dumbbell_imbalance_demo(self):
        # and the same goes for unbalanced dumbbells, or any unbalanced weight that has its center of mass shifted accidentally by lack of precision

        cyheight = 1
        bar = Cylinder(
            radius=0.1,
            height=cyheight,
            direction=X_AXIS,
            fill_color=GRAY,
            fill_opacity=0.8
        )

        left_weight = Cylinder(
            radius=0.3,
            height=0.1,
            direction=X_AXIS,
            color=WHITE,
            fill_opacity=0.9
        )
        right_weight = Cylinder(
            radius=0.3,
            height=0.1,
            direction=X_AXIS,
            color=WHITE,
            fill_opacity=0.9
        )

        bar_center = bar.get_center()
        left_weight.move_to(bar_center + np.array([-0.5 * cyheight, 0, 0]))
        right_weight.move_to(bar_center + np.array([0.5 * cyheight, 0, 0]))

        dumbbell = VGroup(bar, left_weight, right_weight)
        dumbbell.scale(2)

        self.play(ShowIncreasingSubsets(dumbbell), run_time=2)
        self.wait(1)

        com_dot = Dot3D(color=RED, radius=0.12)
        initial_com = dumbbell.get_center_of_mass()
        com_dot.move_to(initial_com)
        self.add(com_dot)

        def update_com(mob):
            left_pos = left_weight.get_center_of_mass()
            right_pos = right_weight.get_center_of_mass()
            right_mass = right_weight.width
            left_mass = left_weight.width
            total_mass = left_mass + right_mass
            new_com = (left_mass * left_pos + right_mass * right_pos) / total_mass
            mob.move_to(new_com)

        self.play(
            right_weight.animate.scale(2, about_point=right_weight.get_center()),
            UpdateFromFunc(com_dot, update_com),
            run_time=2
        )
        self.wait()

        # So if you don't want to twist your wrist like you ankle with reps just choose a Gym that cares about having precise dumbbells and weights.

        self.play(FadeOut(VGroup(dumbbell, com_dot)), run_time=2)

    def gym_pitch(self):
        # So if you don't want to twist your wrist like you ankle with reps just choose a Gym that cares about having precise dumbbells and weights.

        self.move_camera(zoom=0.7, run_time=2)

        logo = Star(
            color=GOLD,
            fill_opacity=0.8
        ).scale(0.5)

        brand_name = Text(
            "X GYM",
            color=GOLD,
            font_size=60,
            weight=BOLD
        )

        tagline = Text(
            "Because your joints deserve better (LOL)",
            color=WHITE,
            font_size=32
        )

        tagline2 = Text(
            "✓ Balanced weights ✓ Safe equipment ✓ Expert trainers",
            color=GREEN,
            font_size=28
        )

        final_group = VGroup(
            logo,
            brand_name,
            tagline,
            tagline2
        ).arrange(DOWN, buff=0.8, center=True)

        self.play(
            FadeIn(logo, scale=0.5),
            run_time=1.5
        )

        self.play(Write(brand_name), run_time=2)

        self.play(
            FadeIn(tagline, shift=UP),
            run_time=1.5
        )

        self.play(
            FadeIn(tagline2, shift=UP),
            run_time=1.5
        )

        self.wait(2)

        self.play(FadeOut(final_group), run_time=2)

        thank_you = Text(
            "Your health is our priority",
            color=WHITE,
            font_size=36
        )
        self.play(Write(thank_you), run_time=1.5)
        self.wait(2)