from unittest import TestCase
from unittest.mock import Mock, patch, call

from mock import GPIO
from mock.ibs import IBS
from src.cleaning_robot import CleaningRobot


class TestCleaningRobot(TestCase):

    def test_robot_initialization_axis_X(self):
        robot = CleaningRobot()
        robot.initialize_robot()
        self.assertEqual(0, robot.pos_x)


