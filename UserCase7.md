## User Story #7: 
The robot detects whether it is stuck by checking all possible movement paths. If every path is blocked by an obstacle,
the robot triggers the buzzer to alert that it is unable to proceed.

The communication with the buzzer happens via the GPIO.output(channel, value) function, where channel is the pin number
and value is False | True. The buzzer is connected to pin 14 (BOARD mode), and has already been configured in the constructor
of the CleaningRobot class.

To track the status of the buzzer (i.e., buzzing or not buzzing), use the boolean instance variable CleaningRobot.buzzer_on.

### Requirement:

Implement CleaningRobot.make_buzzer_buzz(self, actual_heading: str, next_commands: list) -> None to manage the behavior of the buzzer when the robot is stuck.

