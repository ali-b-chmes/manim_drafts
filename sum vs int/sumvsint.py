from manim import *
import numpy as np

summer = 0
last_k = 4

class TheScene(Scene):
    def construct(self):
        global summer, last_k
        self.camera.frame_height = 16
        self.camera.frame_width = 9

        for i in range(4):
            summer += np.sin((i + 0.5) * np.pi / 4) * np.pi / 4

        title = Title("Sum vs. Integration", include_underline=True, underline_buff=0.1, 
                      match_underline_width_to_text=True, 
                      fill_color = [GRAY_A, GOLD], font_size=96).shift(UP*4)
        self.add(title)
        self.wait()

        ax = Axes(
            x_range=[0, np.pi+0.3, np.pi/2],
            y_range=[0, 1+0.3, 0.5],
            x_length= 8,
            y_length= 5,
            axis_config= {"color" : "#686662"}
        ).next_to(title, DOWN, buff = 0.4)
        
        self.play(Create(ax))
        self.wait()

        n = ValueTracker(4)

        def update_summer():
            global summer, last_k
            k = int(np.ceil(n.get_value()))
            if k != last_k:
                summer = 0
                dx = np.pi / k
                for i in range(k):
                    x_center = (i + 0.5) * dx
                    summer += np.sin(x_center) * dx
                last_k = k
            return summer

        eq = MathTex("y \; = \; \sin(x)", color = GOLD).next_to(title, DOWN, buff = 0.5)
        sinGraph = ax.plot(lambda t: np.sin(t), x_range=[0, np.pi], color = WHITE)
        
        self.play(Create(sinGraph), Write(eq))

        rects = always_redraw(lambda: ax.get_riemann_rectangles(
            sinGraph,
            x_range = [0, np.pi],
            dx = (np.pi / n.get_value()),
            input_sample_type = "center",
            fill_opacity = 0.7,
            color=[BLUE_A, BLUE_E], 
            stroke_width=0
        ))

        show_n = always_redraw(
            lambda: MathTex(
                f"n = {int(np.ceil(n.get_value()))}"
            ).next_to(ax, DOWN, buff=1.5)
        )

        Sum = always_redraw(
            lambda: MathTex(
                f"\\Sigma \\Delta x \\cdot \\sin(x) \\approx {update_summer():.7f}"
            ).next_to(show_n, DOWN, buff=1.5)
        )
        
        Int = MathTex(r"\int^\pi_0 \sin(x) \, dx = 2", color = GOLD).next_to(Sum, DOWN, buff=1.5).scale(1.4)
        
        n_rect = always_redraw(lambda: SurroundingRectangle( 
            show_n,
            color=WHITE,
            buff=0.2,
            corner_radius=0.2
        ))
        Sum_rect = always_redraw(lambda: SurroundingRectangle( 
            Sum,
            color=WHITE,
            buff=0.2,
            corner_radius=0.2
        ))
        Int_rect = always_redraw(lambda: SurroundingRectangle(
            Int,
            color=GOLD,
            buff=0.2,
            corner_radius=0.2
        ))

        self.play(FadeIn(rects), FadeIn(show_n), FadeIn(Sum), FadeIn(Int), FadeIn(n_rect), FadeIn(Sum_rect), FadeIn(Int_rect))
        self.wait()
        
        self.play(n.animate.set_value(100), run_time=10)
        self.wait(2)