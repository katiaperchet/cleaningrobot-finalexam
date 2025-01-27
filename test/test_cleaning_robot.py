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

    def test_robot_initialization_axis_Y(self):
        robot = CleaningRobot()
        robot.initialize_robot()
        self.assertEqual(0, robot.pos_y)

    def test_robot_initialization_heading(self):
        robot = CleaningRobot()
        robot.initialize_robot()
        self.assertEqual(robot.N, robot.heading)

    def test_robot_status_initial(self):
        robot = CleaningRobot()
        robot.initialize_robot()
        self.assertEqual("(0,0,N)", robot.robot_status())

    def test_robot_status_not_initial(self):
        robot = CleaningRobot()
        robot.pos_x = 1
        robot.pos_y = 1
        robot.heading = robot.S
        self.assertEqual("(1,1,S)", robot.robot_status())