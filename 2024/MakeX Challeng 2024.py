import novapi
from mbuild import gamepad 
from mbuild.encoder_motor import encoder_motor_class
from mbuild.servo_driver import servo_driver_class
from mbuild import power_expand_board
from mbuild.smartservo import smartservo_class
from mbuild import power_manage_module
from mbuild.ranging_sensor import ranging_sensor_class
import math

smartservo_1 = smartservo_class("M6", "INDEX1")

# def auto():
#         #define ranging_sensor and set the distance varable
#         ranging_sensor_1 = ranging_sensor_class("PORT1", "INDEX1") 
#         cm = ranging_sensor_1.get_distance()

#         #condition of the ranging_sensor
#         if(cm == 5):
#                 pass
#         else:
#                 pass

#encode motor
def active_motor(motor, type, speed=65):
    strMotor = "M{}".format(motor)
    strP = speed
    if(type == 'f'):
        if(motor == 2):
           encoder_motor_class(strMotor, "INDEX1").set_power(-strP)
        elif(motor == 3):
           encoder_motor_class(strMotor, "INDEX1").set_power(-strP)
        elif(motor == 4):
           encoder_motor_class(strMotor, "INDEX1").set_power(strP)
        elif(motor == 5):
           encoder_motor_class(strMotor, "INDEX1").set_power(strP)
    elif(type == 'b'):
        if(motor == 2):
           encoder_motor_class(strMotor, "INDEX1").set_power(strP)
        elif(motor == 3):
           encoder_motor_class(strMotor, "INDEX1").set_power(strP)
        elif(motor == 4):
           encoder_motor_class(strMotor, "INDEX1").set_power(-strP)
        elif(motor == 5):
           encoder_motor_class(strMotor, "INDEX1").set_power(-strP)
    elif(type == 'off'):
        encoder_motor_class(strMotor, "INDEX1").set_power(0)

def movement():
        left = gamepad.is_key_pressed("Left")
        right = gamepad.is_key_pressed("Right")
        up = gamepad.is_key_pressed("Up")
        down = gamepad.is_key_pressed("Down")
        if(left and right == False and up == False and down == False):
                active_motor(2, 'b')
                active_motor(5, 'f')
                active_motor(3, 'f')
                active_motor(4, 'b')
        elif(right and left == False and up == False and down == False):
                active_motor(2, 'f')
                active_motor(5, 'b')
                active_motor(3, 'b')
                active_motor(4, 'f')
        elif(up and down == False and right == False and left == False):
                active_motor(2, 'f')
                active_motor(5, 'f')
                active_motor(3, 'f')
                active_motor(4, 'f')
        elif(down and up == False and right == False and left == False):
                active_motor(2, 'b')
                active_motor(5, 'b')
                active_motor(3, 'b')
                active_motor(4, 'b')
        elif(left and up and right == False and down == False):
                active_motor(2, 'off')
                active_motor(5, 'f')
                active_motor(3, 'f')
                active_motor(4, 'off')
        elif(right and up and left == False and down == False):
                active_motor(2, 'f')
                active_motor(5, 'off')
                active_motor(3, 'off')
                active_motor(4, 'f')
        elif(left and down and right == False and up == False):
                active_motor(2, 'off')
                active_motor(5, 'b')
                active_motor(3, 'b')
                active_motor(4, 'off')
        elif(right and down and left == False and up == False):
                active_motor(2, 'b')
                active_motor(5, 'off')
                active_motor(3, 'off')
                active_motor(4, 'b')
        elif(gamepad.is_key_pressed("N4")):
                active_motor(4, 'f')    #expand 
                active_motor(5, 'f')   
                active_motor(2, 'b')    #extends
                active_motor(3, 'b')
        elif(gamepad.is_key_pressed("N1")):
                active_motor(4, 'b')
                active_motor(5, 'b')   

                active_motor(2, 'f')
                active_motor(3, 'f')
        else:
                active_motor(2, 'off')
                active_motor(5, 'off')
                active_motor(3, 'off')
                active_motor(4, 'off')

def feed_control():
        if(gamepad.get_joystick("Ry") == 100):
                power_expand_board.set_power("DC2", -100)
        elif(gamepad.get_joystick("Ry") == -100):
                power_expand_board.set_power("DC2", 100)
        else:
                power_expand_board.set_power("DC2", 0)

def feed_blushless():
        if(gamepad.get_joystick("Rx") == 100):
                power_expand_board.set_power("DC3", -100)
        elif(gamepad.get_joystick("Rx") == -100):
                power_expand_board.set_power("DC3", 100)
        else:
                power_expand_board.set_power("DC3", 0)



Front_feed = False
Laser = False
RY = gamepad.get_joystick("Ry")

servo_driver_1 = servo_driver_class("PORT1", "INDEX1")
smartservo_1 = smartservo_class("M1", "INDEX1")
while True:
        smartservo_1 = smartservo_class("M6", "INDEX1")
        movement()
        if(gamepad.get_joystick("Ly") <= 100 or gamepad.get_joystick("Ly") <= -100):
                smartservo_1.move_to(-gamepad.get_joystick("Ly"), 15)
        else:
                smartservo_1.set_angle(0)
        #Use right analog to control feed
        feed_control()
        feed_blushless()
        #power_expand_board("DC2", -gamepad.get_joystick("Ry")) {Not working}

        #Lazer control and condition
        if(gamepad.is_key_pressed("+")):
                if(Laser == True):
                        Laser = False
                else:
                        Laser = True
        if(Laser == True):
                power_expand_board.set_power("DC8",-50)
        else:
                power_expand_board.set_power("DC8",0)

        #Blushless motor control
        if(gamepad.is_key_pressed('L1') or gamepad.is_key_pressed("R1")):
                power_expand_board.set_power("BL1",100)
                power_expand_board.set_power("BL2",100)
        else:
                power_expand_board.set_power("BL1",0)
                power_expand_board.set_power("BL2",0)
        #condition for controling Front_feed
        if(gamepad.is_key_pressed("L2")):
                if(Front_feed == True):
                        Front_feed = False
                else:
                        Front_feed = True
        #condition for motor at the Front_feed
        if(Front_feed == True):
                power_expand_board.set_power("DC1", -100)
        else:
                power_expand_board.set_power("DC1", 0)        
