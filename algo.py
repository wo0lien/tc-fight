from sim.robot import PlayerRobot, RobotAction


def algo(r: PlayerRobot) -> RobotAction:
    return r.aim()
