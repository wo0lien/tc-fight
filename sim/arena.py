from abc import ABC
from enum import Enum
from sim.robot import (
    Robot,
    PlayerRobot,
    RobotActionName,
    Team,
    RobotMove,
    RobotAim,
    RobotShoot,
)
from typing import List


class Drawer(ABC):
    def drawArena():
        raise NotImplementedError

    def drawResult(self):
        pass


class Arena:
    # ref at top left
    x_size = 20
    y_size = 10

    nb_robots_per_team = 10

    blue_spawns = [(x, 1) for x in range(5, 15)]
    red_spawns = [(x, 9) for x in range(5, 15)]

    custom_robot: PlayerRobot = None

    robots: List[Robot] = []

    drawer: Drawer

    def __init__(self, d: Drawer, customRobot: PlayerRobot) -> None:
        self.drawer = d()
        self.custom_robot = customRobot

    def draw(self):
        if self.drawer == None:
            return
        self.drawer.drawArena(self)

    def drawResult(self):
        if self.drawer == None:
            return
        self.drawer.drawResult()

    @property
    def alives(self):
        return [r for r in self.robots if r.is_alive]

    def allies(self, robot: Robot):
        return [r for r in self.alives if r.team == robot.team and r.id != robot.id]

    def opponents(self, robot: Robot):
        return [r for r in self.alives if r.team != robot.team]

    def spawn_robots(self):
        """Spawns all robots in the arena"""
        for i in range(self.nb_robots_per_team):
            self.robots.append(
                Robot(str(2 * i), self.blue_spawns[i], Team.BLUE, self.custom_robot)
            )
            self.robots.append(
                Robot(str(2 * i + 1), self.red_spawns[i], Team.RED, self.custom_robot)
            )

    def run_robots_intelligence(self):
        for r in self.alives:
            try:
                r.proxy.nextaction = r.proxy.intelligence()
            except:
                print("User algo failed")

    def verify_robots_action(self):
        for r in self.alives:
            r.get_next_action().valid = self.verify_action(r)

    def verify_action(self, robot: Robot):
        action = robot.get_next_action()

        match action:
            case RobotMove():
                return action.is_valid(robot.position, self.x_size, self.y_size)
            case RobotAim():
                return action.is_valid(self.opponents(robot))
            case RobotShoot():
                return action.is_valid(self.opponents(robot))
            case _:
                raise ValueError

    def apply_robot_action(self):
        for r in self.alives:
            action = r.get_next_action()
            if action.valid is not True:
                continue

            match action:
                case RobotMove():
                    action.apply(r.position)
                case RobotAim():
                    action.apply()
                case RobotShoot():
                    target = action.apply()
                    for ro in self.robots:
                        if ro.id == target:
                            ro.is_alive = False
                case _:
                    raise ValueError

    def next_tick(self):
        for robot in self.alives:
            # calculate surroundings
            surroundings = [
                (r.id, r.position)
                for r in self.opponents(robot)
                if r.in_range(robot.position)
            ]
            robot.next_tick(self.allies(robot), surroundings)


class NoOpDrawer(Drawer):
    def drawArena(self, arena: Arena):
        pass


class ConsoleDrawer(Drawer):
    def drawArena(self, arena: Arena):
        print("-" * (arena.x_size + 2))
        for l in range(arena.y_size):
            s = "." * arena.x_size
            for r in [ro for ro in arena.robots if ro.is_alive]:
                if r.position.y == l:
                    if r.team == Team.BLUE:
                        s = (
                            s[: max(r.position.x - 1, 0)]
                            + "B"
                            + s[max(r.position.x, 1) :]
                        )
                    else:
                        s = (
                            s[: max(r.position.x - 1, 0)]
                            + "R"
                            + s[max(r.position.x, 1) :]
                        )
            print("|" + s + "|")
        print("-" * (arena.x_size + 2))
