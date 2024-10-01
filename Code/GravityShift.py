# Import necessary modules
import novapi
import time
import math
from mbuild.encoder_motor import encoder_motor_class
from mbuild import power_expand_board
from mbuild import gamepad
from mbuild.led_matrix import led_matrix_class
from mbuild.smart_camera import smart_camera_class
from mbuild.ranging_sensor import ranging_sensor_class
from mbuild.smartservo import smartservo_class
from mbuild import power_manage_module

left_forward_wheel = encoder_motor_class("M2", "INDEX1")
right_forward_wheel = encoder_motor_class("M3", "INDEX1")
left_back_wheel = encoder_motor_class("M5", "INDEX1")
right_back_wheel = encoder_motor_class("M6", "INDEX1")

MAX_SPEED = 255
SPEED_MULTIPLIER = 1

class PID:
    def __init__(self, Kp, Ki, Kd, setpoint=0):
        self.Kp = Kp  # Proportional 
        self.Ki = Ki  # Integral 
        self.Kd = Kd  # Derivative 
        self.setpoint = setpoint  # Desired value (target)
        self.integral = 0  # Sum of errors over time
        self.previous_error = 0  # Previous error (used for derivative)

    def update(self, current_value):
        # Calculate the error (setpoint - current value)
        error = self.setpoint - current_value
        
        # Proportional term
        P = self.Kp * error
        
        # Integral term
        self.integral += error
        I = self.Ki * self.integral

        # Derivative term
        derivative = error - self.previous_error
        D = self.Kd * derivative

        # Calculate the output
        output = P + I + D

        # Save the current error for the next update
        self.previous_error = error

        return output

    def set_setpoint(self, setpoint):
        self.setpoint = setpoint
        self.integral = 0  # Reset the integral to avoid wind-up
        self.previous_error = 0  # Reset previous error to avoid a large derivative spike

class motors:
    
    def drive(lf: int, lb: int, rf: int, rb: int):
        left_back_wheel.set_speed(lb) # left back :DDDDD
        right_back_wheel.set_speed(-rb)  # RIGHT BACK  
        right_forward_wheel.set_speed(-(rf))      # RIGHT FORWARD
        left_forward_wheel.set_speed(lf)             # LEFT BACK
    
    def stop():
        motors.drive(0, 0, 0, 0)

class util:
    def restrict(val, minimum, maximum):
        return max(min(val, maximum), minimum)

class holonomic:        
    pids = {
        "lf": PID(Kp=1, Ki=0, Kd=0),
        "lb": PID(Kp=1, Ki=0, Kd=0),
        "rf": PID(Kp=1, Ki=0, Kd=0),
        "rb": PID(Kp=1, Ki=0, Kd=0),
    }
    def drive(vx, vy, wL, deadzone=5, pid=True):
        global SPEED_MULTIPLIER
        # Create a deadzone so that if the joystick isn't moved perfectly,
        # the controller can still make the robot move perfectly.
        if math.fabs(vx) < math.fabs(deadzone):
            vx = 0
        if math.fabs(vy) < math.fabs(deadzone):
            vy = 0
        if math.fabs(wL) < math.fabs(deadzone):
            wL = 0

        vFL = (vx + vy + wL) * SPEED_MULTIPLIER
        vFR = (-(vx) + vy - wL) * SPEED_MULTIPLIER
        vBL = (-(vx) + vy + wL) * SPEED_MULTIPLIER
        vBR = (vx + vy - wL) * SPEED_MULTIPLIER
        
        # Sliding check to not interfere with the normal movement, incase of tuning specific power
        if math.fabs(vx) > math.fabs(vy):
            vBR *= 0.8
        
        if pid:            
            # Left Forward
            holonomic.pids["lf"].set_setpoint(vFL)
            vFL = holonomic.pids["lf"].update(-left_forward_wheel.get_value("speed"))
            # Left Back
            holonomic.pids["lb"].set_setpoint(vBL)
            vBL = holonomic.pids["lb"].update(-left_back_wheel.get_value("speed"))
            # Right Forward
            holonomic.pids["rf"].set_setpoint(vFR)
            vFR = holonomic.pids["rf"].update(right_forward_wheel.get_value("speed"))
            # Right Back
            holonomic.pids["rb"].set_setpoint(vBR)
            vBR = holonomic.pids["rb"].update(right_back_wheel.get_value("speed"))
        # Velocity
        vFL = util.restrict(vFL, -MAX_SPEED, MAX_SPEED)
        vFR = util.restrict(vFR, -MAX_SPEED, MAX_SPEED)
        vBL = util.restrict(vBL, -MAX_SPEED, MAX_SPEED)
        vBR = util.restrict(vBR, -MAX_SPEED, MAX_SPEED)
        # Drive motor
        motors.drive(vFL, vBL, vFR, vBR)
        
    def move_forward(power):
        holonomic.drive(0, power, 0)
        
    def move_backward(power):
        holonomic.drive(0, -power, 0)
        
    def slide_right(power):
        holonomic.drive(power, 0, 0)
        
    def slide_left(power):
        holonomic.drive(-power, 0, 0)
        
    def turn_right(power):
        holonomic.drive(0, 0, power)
        
    def turn_left(power):
        holonomic.drive(0, 0, -power)

class dc_motor:
    # Default DC port
    dc_port = "DC1"
    # Default direction (not reversed)
    reverse = False
    
    # Initialize DC motor with a specific port
    def __init__(self, port: str) -> None:
        self.dc_port = port
        
    # Method to set the direction of the motor
    def set_reverse(self, rev: bool) -> None:
        self.reverse = rev
        
    # Method to turn on the DC motor
    def on(self) -> None:
        power = -100 if self.reverse else 100
        power_expand_board.set_power(self.dc_port, power)
        
    # Method to turn off the DC motor
    def off(self) -> None:
        power_expand_board.stop(self.dc_port)
        
class brushless_motor:
    # Default brushless motor port
    bl_port = "BL1"
    
    # Initialize brushless motor with a specific port
    def __init__(self, port: str) -> None:
        self.bl_port = port
        
    # Method to turn on the brushless motor
    def on(self) -> None:
        power_expand_board.set_power(self.bl_port, 100)
        
    # Method to turn off the brushless motor
    def off(self) -> None:
        power_expand_board.stop(self.bl_port)
           

class runtime:
    # Define control mode
    CTRL_MODE = 0
    
    # Robot state
    ENABLED = True
    def move():
        if math.fabs(gamepad.get_joystick("Lx")) > 20 or math.fabs(gamepad.get_joystick("Ly")) > 20 or math.fabs(gamepad.get_joystick("Rx")) > 20:
            holonomic.drive(-gamepad.get_joystick("Lx"), gamepad.get_joystick("Ly"), -gamepad.get_joystick("Rx"), pid=True)
        else:
            motors.drive(0,0,0,0)
    def change_mode():
        if novapi.timer() > 0.9:
            entrance_feed.off()
            feeder.off()
            if runtime.CTRL_MODE == 0:
                runtime.CTRL_MODE = 1
            else:
                runtime.CTRL_MODE = 0
            novapi.reset_timer()

class shoot_mode:

    # Method to control various robot functions based on button inputs
    def control_button():
        if gamepad.is_key_pressed("R2"):
            entrance_feed.set_reverse(False)
            feeder.set_reverse(False)
            entrance_feed.on()
            feeder.on()
            conveyer.set_reverse(False)
            conveyer.on()
        elif gamepad.is_key_pressed("L2"):
            entrance_feed.set_reverse(True)
            feeder.set_reverse(True)
            entrance_feed.on()
            feeder.on()
            conveyer.set_reverse(True)
            conveyer.on()
        if gamepad.is_key_pressed("L1"):
            entrance_feed.off()
            feeder.off()
            conveyer.off()
        if gamepad.is_key_pressed("R1"):
            bl_1.on()
            bl_2.on()
        else:
            bl_1.off()
            bl_2.off()
        if gamepad.is_key_pressed("≡"):
            laser.set_reverse(True)
            laser.on()
        else:
            laser.off()
        #shooter_angle control
        if gamepad.is_key_pressed("Up"):
            shooter.move(-5, 10)
        elif gamepad.is_key_pressed("Down"):
            shooter.move(5, 10)
        else:
            shooter.move(None, 0)

            
class gripper_mode:
    # Method to control various robot functions based on button inputs
    def control_button():
        if gamepad.is_key_pressed("N2"):
            lift.set_reverse(True)
            lift.on()
        elif gamepad.is_key_pressed("N3"):
            lift.set_reverse(False)
            lift.on()
        else:
            lift.off()
        if gamepad.is_key_pressed("N1"):
            gripper.set_reverse(True)
            gripper.on()
        elif gamepad.is_key_pressed("N4"):
            gripper.set_reverse(False)
            gripper.on()
        else:
            gripper.off()
        

# Instantiate DC motors
lift = dc_motor("DC2")
gripper = dc_motor("DC1")
conveyer = dc_motor("DC5")
entrance_feed = dc_motor("DC6")
feeder = dc_motor("DC7")
bl_1 = brushless_motor("BL1")
bl_2 = brushless_motor("BL2")
shooter = smartservo_class("M1", "INDEX1") # only for angles
laser = dc_motor("DC8")

while True:
    
    if power_manage_module.is_auto_mode():
        pass
        while power_manage_module.is_auto_mode():
            pass
    else:
        if gamepad.is_key_pressed("L2") and gamepad.is_key_pressed("R2"):
            runtime.change_mode()
        else:
            runtime.move()
            if runtime.CTRL_MODE == 0:
                shoot_mode.control_button()
            else:
                gripper_mode.control_button()
