from sim.arena import Arena
from sim.robot import Robot, Team
import time
from typing import Union, Optional


class Fight:
    arena: Arena

    winner: Union[Team, None] = None
    ended = False

    max_tick = 100

    def __init__(self, arena: Arena) -> None:
        self.arena = arena

    def update_robots_state(self):
        for r in self.arena.robots:
            pass

    def check_victory(self):
        # count alive robots
        blue_robots_alive = 0
        red_robots_alive = 0
        for r in self.arena.robots:
            if r.is_alive:
                if r.team == Team.BLUE:
                    blue_robots_alive += 1
                else:
                    red_robots_alive += 1

        if blue_robots_alive == 0 and red_robots_alive == 0:
            return "DRAW"
        if blue_robots_alive == 0:
            return "RED"
        if red_robots_alive == 0:
            return "BLUE"
        return None

    def fight(self):
        # init fight
        current_tick = 0
        self.arena.spawn_robots()
        while self.ended == False and current_tick < self.max_tick:
            time.sleep(0.1)
            self.arena.draw()
            self.arena.next_tick()
            # run robot intelligence
            self.arena.run_robots_intelligence()
            # verify robot actions validity
            self.arena.verify_robots_action()
            # run robot actions
            self.arena.apply_robot_action()
            # check victory conditions
            if self.check_victory() != None:
                self.ended = True

            current_tick += 1
