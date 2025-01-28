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

    @patch.object(GPIO, "output")
    @patch.object(IBS, "get_charge_left")
    def test_charge_left_more_10_led_off(self, mock_battery: Mock, mock_led: Mock):
        mock_battery.return_value = 11
        robot = CleaningRobot()
        robot.manage_cleaning_system()
        calls = [((robot.RECHARGE_LED_PIN, False),)]
        mock_led.assert_has_calls(calls)
        self.assertFalse(robot.recharge_led_on)

    @patch.object(GPIO, "output")
    @patch.object(IBS, "get_charge_left")
    def test_charge_left_more_10_cleaning_system_on(self, mock_battery: Mock, mock_cleaning_system: Mock):
        mock_battery.return_value = 11
        robot = CleaningRobot()
        robot.manage_cleaning_system()
        calls = [((robot.CLEANING_SYSTEM_PIN, True),)]
        mock_cleaning_system.assert_has_calls(calls)
        self.assertTrue(robot.cleaning_system_on)

    @patch.object(GPIO, "output")
    @patch.object(IBS, "get_charge_left")
    def test_charge_left_less_10_led_on(self, mock_battery: Mock, mock_led: Mock):
        mock_battery.return_value = 9
        robot = CleaningRobot()
        robot.manage_cleaning_system()
        calls = [((robot.RECHARGE_LED_PIN, True),)]
        mock_led.assert_has_calls(calls)
        self.assertTrue(robot.recharge_led_on)

    @patch.object(GPIO, "output")
    @patch.object(IBS, "get_charge_left")
    def test_charge_left_less_10_cleaning_system_off(self, mock_battery: Mock, mock_cleaning_system: Mock):
        mock_battery.return_value = 9
        robot = CleaningRobot()
        robot.manage_cleaning_system()
        calls = [((robot.CLEANING_SYSTEM_PIN, False),)]
        mock_cleaning_system.assert_has_calls(calls)
        self.assertFalse(robot.cleaning_system_on)

    @patch.object(GPIO, "output")
    @patch.object(IBS, "get_charge_left")
    def test_charge_left_equal_10_led_on_and_cleaning_off(self, mock_battery: Mock, mock_pins: Mock):
        mock_battery.return_value = 10
        robot = CleaningRobot()
        robot.manage_cleaning_system()
        calls = [((robot.CLEANING_SYSTEM_PIN, False),),
                 ((robot.RECHARGE_LED_PIN, True),)]
        mock_pins.assert_has_calls(calls, any_order=True)
        self.assertFalse(robot.cleaning_system_on)

    @patch.object(IBS, "get_charge_left")
    @patch.object(CleaningRobot, "activate_wheel_motor")
    def test_execute_command_forward_Y_axis(self, mock_robot: Mock, mock_battery: Mock):
        mock_battery.return_value = 11
        robot = CleaningRobot()
        robot.initialize_robot()
        result = robot.execute_command(robot.FORWARD)
        mock_robot.assert_called_once()
        self.assertEqual("(0,1,N)", result)

    @patch.object(IBS, "get_charge_left")
    @patch.object(CleaningRobot, "activate_wheel_motor")
    def test_execute_command_forward_X_axis(self, mock_robot: Mock, mock_battery: Mock):
        mock_battery.return_value=11
        robot = CleaningRobot()
        robot.initialize_robot()
        robot.heading = robot.W
        result = robot.execute_command(robot.FORWARD)
        mock_robot.assert_called_once()
        self.assertEqual("(1,0,W)", result)

    @patch.object(IBS, "get_charge_left")
    @patch.object(CleaningRobot, "activate_rotation_motor")
    def test_execute_command_left(self, mock_robot: Mock, mock_battery: Mock):
        mock_battery.return_value = 11
        robot = CleaningRobot()
        robot.initialize_robot()
        result = robot.execute_command(robot.LEFT)
        mock_robot.assert_called_once()
        self.assertEqual("(0,0,W)", result)

    @patch.object(IBS, "get_charge_left")
    @patch.object(CleaningRobot, "activate_rotation_motor")
    def test_execute_command_right(self, mock_robot: Mock, mock_battery: Mock):
        mock_battery.return_value = 11
        robot = CleaningRobot()
        robot.initialize_robot()
        result = robot.execute_command(robot.RIGHT)
        mock_robot.assert_called_once()
        self.assertEqual("(0,0,E)", result)

    @patch.object(IBS, "get_charge_left")
    @patch.object(CleaningRobot, "obstacle_found")
    @patch.object(GPIO, "input")
    def test_detect_obstacle_true_y_axis(self, mock_infrared_distance: Mock, mock_obstacle: Mock, mock_battery: Mock):
        mock_battery.return_value = 11
        mock_infrared_distance.return_value = True
        robot = CleaningRobot()
        robot.initialize_robot()
        result = robot.execute_command(robot.FORWARD)
        mock_obstacle.assert_called_once()
        self.assertEqual("(0,0,N)(0,1)", result)

    @patch.object(IBS, "get_charge_left")
    @patch.object(CleaningRobot, "obstacle_found")
    @patch.object(GPIO, "input")
    def test_detect_obstacle_true_x_axis(self, mock_infrared_distance: Mock, mock_obstacle: Mock, mock_battery: Mock):
        mock_battery.return_value = 11
        mock_infrared_distance.return_value = True
        robot = CleaningRobot()
        robot.initialize_robot()
        robot.heading = robot.E
        result = robot.execute_command(robot.FORWARD)
        mock_obstacle.assert_called_once()
        self.assertEqual("(0,0,E)(1,0)", result)

    @patch.object(GPIO, "output")
    @patch.object(IBS, "get_charge_left")
    @patch.object(CleaningRobot, "robot_status")
    def test_charge_left_less_10_cleaningOff_ledOn_stayStill_commandForward(self, mock_robot_status: Mock, mock_battery: Mock, mock_pins: Mock):
        mock_battery.return_value = 9
        mock_robot_status.return_value = "(1,1,N)"
        robot = CleaningRobot()
        result = robot.execute_command(robot.FORWARD)
        calls = [((robot.CLEANING_SYSTEM_PIN, False),),
                 ((robot.RECHARGE_LED_PIN, True),)]
        mock_pins.assert_has_calls(calls, any_order=True)
        self.assertFalse(robot.cleaning_system_on)
        self.assertTrue(robot.recharge_led_on)
        self.assertEqual("!(1,1,N)",result)

    @patch.object(GPIO, "output")
    @patch.object(IBS, "get_charge_left")
    @patch.object(CleaningRobot, "robot_status")
    def test_charge_left_equal_10_cleaningOff_ledOn_stayStill_commandForward(self, mock_robot_status: Mock,
                                                                            mock_battery: Mock, mock_pins: Mock):
        mock_battery.return_value = 10
        mock_robot_status.return_value = "(1,1,N)"
        robot = CleaningRobot()
        result = robot.execute_command(robot.FORWARD)
        calls = [((robot.CLEANING_SYSTEM_PIN, False),),
                 ((robot.RECHARGE_LED_PIN, True),)]
        mock_pins.assert_has_calls(calls, any_order=True)
        self.assertFalse(robot.cleaning_system_on)
        self.assertTrue(robot.recharge_led_on)
        self.assertEqual("!(1,1,N)", result)