from sim.fight import Fight
from sim.arena import Arena, ConsoleDrawer
from sim.robot import PlayerRobot, Direction, RobotActionName
import random


# User algo
class PlayerRobotTom(PlayerRobot):

    def intelligence(self):
        if len(self.surroundings) > 0:
            if self.lastAction[0] == RobotActionName.AIM:
                return self.shoot(self.lastAction[2])
            else:
                return self.aim(self.surroundings[0][0])
        d = random.choice(list(Direction))
        a = self.move(d)
        return a


a = Arena(ConsoleDrawer, PlayerRobotTom)

fight = Fight(a)

fight.fight()
