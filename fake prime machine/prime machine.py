from manim import *

class ThaCLass(Scene):
    def construct(self):
        title = Text("Prime Machine?", font="Cinzel", gradient=(RED, YELLOW, BLUE), font_size=30)
        title = title.to_edge(UP)
        self.add(title)
        self.wait()

        stat_eq = MathTex("f(x) = x^2 + x + 41").next_to(title, DOWN).scale(0.5)
        self.play(Write(stat_eq))
        self.wait()

        contour = Square(side_length = 4).next_to(title, 8*DOWN)
        pri = Text("Prime ✓", color = GREEN_E, font_size = 15).move_to(contour.get_corner(UP + LEFT) + 0.5 * RIGHT + 0.15 * DOWN)
        self.play(DrawBorderThenFill(contour), FadeIn(pri))
        u=0


        for i in range(8):
            for j in range(5):
                f = u**2 + u + 41
                equa = MathTex(f"f({u}) = {f}").next_to(stat_eq, DOWN*0.5).scale(0.6)
                self.play(Write(equa), run_time = 0.2)
                self.wait(0.1)
                item = Tex(f"{f}").scale(0.3).move_to(contour.get_corner(UP + LEFT) + (j + 0.7) * 0.7 * RIGHT + (i+1)* 0.444 * DOWN)
                self.play(Transform(equa, item), run_time = 0.2)
                u+=1

        paroles = Text("A hidden prime-generating machine?", color = GOLD_B).next_to(stat_eq, DOWN*0.5).scale(0.35)
        self.play(Write(paroles))

        self.play(FadeOut(paroles))

        l1 = MathTex("f(","40",")", "=", "1681").next_to(stat_eq, DOWN*0.5).scale(0.7)
        l2 = MathTex("=", "40^2", "+", "40", "+", "41").next_to(stat_eq, DOWN*0.5).scale(0.7)
        l3 = MathTex("=", "40", "\cdot", "41", "+", "41", "=", "41^2", color=RED).next_to(stat_eq, DOWN*0.5).scale(0.7)

        self.play(Write(l1))
        self.wait(0.5)
        self.play(TransformMatchingTex(l1, l2))
        self.wait(0.5)
        self.play(TransformMatchingTex(l2, l3))
        self.wait()