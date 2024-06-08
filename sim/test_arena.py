from io import StringIO
import pytest
from sim.arena import Arena, ConsoleDrawer
from sim.robot import Robot
import pytest
from io import StringIO
from sim.arena import Arena, ConsoleDrawer
from sim.robot import Robot


class TestConsoleDrawer:
    def test_drawArena(self):
        arena = Arena()
        robot1 = Robot()
        robot1.position.x = 5
        robot1.position.y = 0
        arena.robots.append(robot1)

        expected_output = "     x               \n"
        with pytest.patch("sys.stdout", new=StringIO()) as fake_output:
            ConsoleDrawer.drawArena(arena)
            assert fake_output.getvalue() == expected_output
