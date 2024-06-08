from enum import Enum
from typing import List, Tuple, Union
from icecream import ic
import copy


class Position:
    x: int = 0
    y: int = 0

    def __init__(self, pos: Tuple[int, int]) -> None:
        self.x = pos[0]
        self.y = pos[1]

    def distance(self, other_pos: "Position"):
        return abs(self.x - other_pos.x) + abs(self.y - other_pos.y)

    def __str__(self) -> str:
        return f"{str(self.x)}:{str(self.y)}"


class Team(Enum):
    BLUE = 1
    RED = 2


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


class RobotActionName(Enum):
    MOVE = 1
    AIM = 2
    SHOOT = 3


class RobotAction:
    name: RobotActionName
    valid: bool = None

    def __init__(self) -> None:
        pass

    def is_valid(self):
        raise NotImplementedError


class RobotMove(RobotAction):

    direction: Direction = None

    def __init__(self, dir: Direction) -> None:
        self.name = RobotActionName.MOVE
        self.direction = dir

    def apply(self, pos: Position):
        #  perform update
        if self.direction == Direction.UP:
            pos.y -= 1
        elif self.direction == Direction.DOWN:
            pos.y += 1
        elif self.direction == Direction.LEFT:
            pos.x -= 1
        elif self.direction == Direction.RIGHT:
            pos.x += 1
        else:
            raise ValueError

    def is_valid(self, pos: Position, max_x: int, max_y: int):
        currentPos = copy.deepcopy(pos)
        self.apply(currentPos)
        # perform check
        if currentPos.y < 0 or currentPos.x < 0:
            return False
        if currentPos.y >= max_y or currentPos.x >= max_x:
            return False
        return True


class RobotAim(RobotAction):
    target: str
    my_pos: Position
    range: int

    def __init__(self, target: str, my_pos: Position, range: int) -> None:
        self.name = RobotActionName.AIM
        self.target = target
        self.range = range
        self.my_pos = my_pos

    def apply(self):
        pass  # this action has no consequences on the game

    def is_valid(self, oponents: List["Robot"]):
        for r in oponents:
            if r.id == self.target:
                return self.my_pos.distance(r.position) <= self.range
        return False


class RobotShoot(RobotAction):
    target: str
    my_pos: Position
    range: int

    def __init__(self, target: str, my_pos: Position, range: int) -> None:
        self.name = RobotActionName.SHOOT
        self.target = target
        self.my_pos = my_pos
        self.range = range

    def apply(self):
        return self.target

    def is_valid(self, oponents: List["Robot"]):
        for r in oponents:
            if r.id == self.target:
                return self.my_pos.distance(r.position) <= self.range
        return False


class PlayerRobot:
    """Robot proxy"""

    def intelligence(self):
        raise NotImplementedError

    def move(self, dir: Direction):
        return [RobotActionName.MOVE, dir]

    def aim(self, target: str):
        return [RobotActionName.AIM, target]

    def shoot(self, target: str):
        return [RobotActionName.SHOOT, target]

    # read only
    id: str
    position: Position
    team: Team
    is_alive: bool
    allies_pos: List[Position]
    surroundings: List[Tuple[str, Position]]
    lastAction: RobotActionName

    # writeable
    nextaction = []


class Robot:
    """Robot defines the capabilities of robots. Their behavior will be defined by the players"""

    range = 3

    id: str = "robot"
    lastAction: RobotAction = None
    nextAction: RobotAction = None
    position: Position
    team: Team = Team
    is_alive: bool = True
    allies: List["Robot"] = []
    surroundings: List[Tuple[str, Position]] = []

    proxy: PlayerRobot = None

    def __init__(
        self, id: str, pos: Tuple[int, int], team: Team, customRobot: PlayerRobot
    ) -> None:
        self.id = id
        self.proxy = customRobot()
        self.position = Position(pos)
        self.team = team

    def in_range(self, pos: Position) -> bool:
        """Get if provided position is in range of the robot"""
        return self.position.distance(pos) <= self.range

    def next_tick(
        self, allies: List["Robot"], surroundings: List[Tuple[str, Position]]
    ):
        self.lastAction = copy.deepcopy(self.nextAction)
        self.allies = allies
        self.surroundings = surroundings

        self.proxy.id = self.id
        self.proxy.position = self.position
        self.proxy.is_alive = self.is_alive
        self.proxy.allies = self.allies
        self.proxy.surroundings = self.surroundings

        match self.lastAction:
            case RobotMove():
                self.proxy.lastAction = (
                    RobotActionName.MOVE,
                    self.lastAction.is_valid,
                    self.lastAction.direction,
                )
            case RobotAim():
                self.proxy.lastAction = (
                    RobotActionName.AIM,
                    self.lastAction.is_valid,
                    self.lastAction.target,
                )
            case RobotShoot():
                self.proxy.lastAction = (
                    RobotActionName.SHOOT,
                    self.lastAction.is_valid,
                    self.lastAction.target,
                )
            case _:
                self.proxy.lastAction = None

        self.nextAction = None

    def get_next_action(self) -> RobotAction:
        if self.nextAction != None:
            return self.nextAction

        name = self.proxy.nextaction[0]

        match name:
            case RobotActionName.MOVE:
                self.nextAction = RobotMove(self.proxy.nextaction[1])
            case RobotActionName.AIM:
                self.nextAction = RobotAim(
                    self.proxy.nextaction[1], self.position, self.range
                )
            case RobotActionName.SHOOT:
                self.nextAction = RobotShoot(
                    self.proxy.nextaction[1], self.position, self.range
                )
            case _:
                raise ValueError

        return self.nextAction
