from PIL import Image, ImageDraw
import os
from sim.arena import Drawer, Arena
from sim.robot import Team

RED_FILL = (255, 0, 0)
BLUE_FILL = (0, 0, 255)
BACKGROUND_FILL = (255, 255, 255)
BORDERS_FILL = (0, 0, 0)

SCALE_FACTOR = 10


class GifDrawer(Drawer):
    frames = []

    def drawArena(self, arena: "Arena"):
        img = Image.new(
            "RGB",
            ((arena.x_size + 2) * SCALE_FACTOR, (arena.y_size + 2) * SCALE_FACTOR),
            BACKGROUND_FILL,
        )
        draw = ImageDraw.Draw(img)
        fill = BORDERS_FILL
        # Draw rectangle border on the sides of the arena
        draw.rectangle(
            [
                0,
                0,
                (arena.x_size + 1) * SCALE_FACTOR,
                (arena.y_size + 1) * SCALE_FACTOR,
            ],
            outline=fill,
            width=2,
        )
        for r in arena.alives:
            fill = self.fill(r.team)
            draw.ellipse(
                [
                    r.position.x * SCALE_FACTOR,
                    r.position.y * SCALE_FACTOR,
                    (r.position.x + 1) * SCALE_FACTOR,
                    (r.position.y + 1) * SCALE_FACTOR,
                ],
                fill,
            )

        self.frames.append(img)

    def drawResult(self):
        # Save frames as an animated GIF
        self.frames[0].save(
            "animated.gif",
            save_all=True,
            append_images=self.frames[1:],
            duration=100,  # duration of each frame in milliseconds
            loop=0,  # loop forever
        )

    def fill(self, t: Team):
        if t == Team.BLUE:
            return BLUE_FILL
        return RED_FILL
