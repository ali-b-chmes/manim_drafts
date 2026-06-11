from manim import *
import numpy as np


class Scene1(ThreeDScene):
    def construct(self):
        
        line1 = Tex("Visualising Euler's formula in 3D !", color = "#D88A31").to_edge(UP, buff=0.7).scale(0.45)
        line2 = MathTex(r"\left(\text{Euler's Formula : } e^{ix} = \cos(x) + i\sin(x)\right)").scale(0.4).next_to(line1, DOWN)

        self.play(FadeIn(line1), run_time = 1)
        self.wait()
        self.play(Write(line2))
        self.wait()

        ax = ThreeDAxes(
            x_range = [-2, 2, 1],
            y_range = [-2, 2, 1],
            z_range = [0, 20, 2],

            x_length=4,
            y_length=4,
            z_length=20,
        ).scale(0.7).rotate(-15*DEGREES, Y_AXIS).rotate(15*DEGREES, X_AXIS).move_to(ORIGIN + DOWN + LEFT*1.5)
        
        xlab = ax.get_x_axis_label("Re", direction=RIGHT, buff=0.1).scale(0.7)
        ylab = ax.get_y_axis_label("Im", direction=UP, buff=0.1).scale(0.7).rotate(-PI/2, Z_AXIS)

        x_axis = ax.x_axis
        y_axis = ax.y_axis
        z_axis = ax.z_axis

        self.play(Create(x_axis), FadeIn(xlab))
        self.wait(0.3)

        self.play(Create(y_axis), FadeIn(ylab))
        self.wait(0.3)

        self.play(Create(z_axis))
        self.wait(0.3)

        SinGraph = ParametricFunction(
            lambda t: ax.c2p(0, np.sin(2*t), t),
            t_range=[0, 20], # type: ignore
            color=YELLOW
        )
        sinlabelplace = SinGraph.point_from_proportion(0.1) 
        sinlabel = MathTex("\sin(x)", color = YELLOW).scale(0.7).move_to(sinlabelplace + UP*1.5)

        CosGraph = ParametricFunction(
            lambda t: ax.c2p(np.cos(2*t), 0, t),
            t_range=[0, 20], # type: ignore
            color=GREEN
        )
        coslabelplace = CosGraph.point_from_proportion(0.1) 
        coslabel = MathTex("\cos(x)", color= GREEN).scale(0.7).move_to(coslabelplace + RIGHT*1.5)


        self.play(Create(CosGraph), run_time = 2)
        self.play(Write(coslabel))
        self.wait()
        self.play(Create(SinGraph), run_time = 2)
        self.play(Write(sinlabel))
        self.wait()

        k = ValueTracker(0)

        doty = always_redraw(
            lambda: Dot3D(color=RED).move_to(ax.c2p([
                np.cos(2 * k.get_value()),
                np.sin(2 * k.get_value()),
                k.get_value()
            ])
        ))

        trail = TracedPath(doty.get_center, stroke_color=RED, stroke_width=3)

        self.add(trail, doty)
        self.play(k.animate.set_value(10), run_time=5)
