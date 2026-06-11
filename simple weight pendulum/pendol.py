from manim import *
import numpy as np

class ThaScene(Scene):
    def construct(self):
        g = 9.81
        l = 1
        dt = 1/60


        th = PI/6
        dthdt = 0

        bob = Dot(radius=0.1, color=RED)
        rod = Line(ORIGIN, bob.get_center(), color=BLUE)
        path = TracedPath(bob.get_center, dissipating_time=0.5)
        Pendulum = Group(rod, bob)

        self.play(FadeIn(Pendulum))
        self.add(path)

        def update_pendulum(mob):
            nonlocal th, dthdt, dt

            d2thdt = -(g/l) * np.sin(th)

            dthdt += d2thdt * dt
            th += dthdt * dt

            x = l * np.sin(th)
            y = -l * np.cos(th)
            bob.move_to([x, y, 0])
            rod.put_start_and_end_on(ORIGIN, bob.get_center())

        Pendulum.add_updater(update_pendulum)

        self.wait(10)