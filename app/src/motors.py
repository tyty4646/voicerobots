import RPi.GPIO as GPIO          

class Motors:
    '''
    Abstracts GPIO initialization and PWM
    signal management to provide functions for moving the robot.

    Parameters:
        - left_dir (int): direction pin of left motor
        - left_step (int): step pin of left motor
        - right_dir (int): direction pin of right motor
        - right_step (int): step pin of right motor
    '''
    MAX_FREQUENCY = 1000

    def __init__(self, left_dir, left_step, right_dir, right_step):
        self.left_dir = left_dir
        self.left_step = left_step
        self.right_dir = right_dir
        self.right_step = right_step

        # setup motor control pins as outputs
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(left_dir, GPIO.OUT)
        GPIO.setup(left_step, GPIO.OUT)
        GPIO.setup(right_dir, GPIO.OUT)
        GPIO.setup(right_step, GPIO.OUT)

        GPIO.output(left_dir, GPIO.LOW)
        GPIO.output(right_dir, GPIO.LOW)

        self.left_pwm = GPIO.PWM(left_step, 100)
        self.right_pwm = GPIO.PWM(right_step, 100)

        self.left_pwm.start(100)
        self.left_pwm.ChangeDutyCycle(50)
        self.right_pwm.start(100)
        self.right_pwm.ChangeDutyCycle(50)




    def set_stepper_speed(self, x, y):
        '''
        Sets direction and speed of stepper motors based on x and y inputs
        on the interval [-1, 1].
        The robot will be stationary with (0, 0), move straight forward with
        (0, 1), rotate left with (-1, 0), etc.
        
        Parameters:
            - x (int): turning/rotation
            - y (int): forward/backward movement
        '''
        # Calculate motor speeds
        left_speed = (y + x) / 2
        right_speed = (y - x) / 2

        # Ensure motor speeds are within valid range [-1, 1]
        left_speed = max(min(left_speed, 1), -1)
        right_speed = max(min(right_speed, 1), -1)

        if left_speed < 0:
            GPIO.output(self.left_dir, GPIO.LOW)
        else:
            GPIO.output(self.left_dir, GPIO.HIGH)

        if right_speed < 0:
            GPIO.output(self.right_dir, GPIO.LOW)
        else:
            GPIO.output(self.right_dir, GPIO.HIGH)

        if left_speed == 0:
            self.left_pwm.ChangeDutyCycle(0)
        else:
            self.left_pwm.ChangeDutyCycle(50)

        if right_speed == 0:
            self.right_pwm.ChangeDutyCycle(0)
        else:
            self.right_pwm.ChangeDutyCycle(50)

        print(f"Setting speed: {left_speed}, {right_speed}.")
        self.left_pwm.ChangeFrequency(max(self.MAX_FREQUENCY * left_speed, 100))
        self.right_pwm.ChangeFrequency(max(self.MAX_FREQUENCY * right_speed, 100))
            