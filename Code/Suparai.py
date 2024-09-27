# codes make you happy
import novapi
from mbuild import power_manage_module
from mbuild.encoder_motor import encoder_motor_class
from mbuild import gamepad
from mbuild import power_expand_board
import time

# initialize variables
Move = 0

# new class
encoder_motor_M1 = encoder_motor_class("M1", "INDEX1")
encoder_motor_M2 = encoder_motor_class("M2", "INDEX1")
encoder_motor_M3 = encoder_motor_class("M3", "INDEX1")
encoder_motor_M4 = encoder_motor_class("M4", "INDEX1")
encoder_motor_M5 = encoder_motor_class("M5", "INDEX1")

def Laser():
    global Move
    if gamepad.is_key_pressed("N1"):
      power_expand_board.set_power("DC5", -50)

def feedbon():
    global Move
    if gamepad.is_key_pressed("N4"):
      power_expand_board.set_power("DC2", 100)

    else:
      if gamepad.is_key_pressed("N1"):
        power_expand_board.set_power("DC2", -100)

      else:
        power_expand_board.stop("DC2")

def Block():
    global Move
    if gamepad.is_key_pressed("N2"):
      power_expand_board.set_power("DC4", 100)

    else:
      if gamepad.is_key_pressed("N3"):
        power_expand_board.set_power("DC4", -100)

      else:
        power_expand_board.stop("DC4")

def BL():
    global Move
    if gamepad.is_key_pressed("R1"):
      power_expand_board.set_power("BL1", 100)
      power_expand_board.set_power("BL2", -100)
      power_expand_board.set_power("BL2", 100)

    else:
      power_expand_board.stop("BL1")
      power_expand_board.stop("BL2")

def Move():
    global Move
    if gamepad.is_key_pressed("Down"):
      encoder_motor_M2.set_power(-60)
      encoder_motor_M3.set_power(-60)
      encoder_motor_M4.set_power(60)
      encoder_motor_M5.set_power(60)

    else:
      if gamepad.is_key_pressed("Up"):
        encoder_motor_M2.set_power(60)
        encoder_motor_M3.set_power(60)
        encoder_motor_M4.set_power(-60)
        encoder_motor_M5.set_power(-60)

      else:
        if gamepad.get_joystick("Lx") == 100:
          encoder_motor_M2.set_power(-60)
          encoder_motor_M3.set_power(60)
          encoder_motor_M4.set_power(60)
          encoder_motor_M5.set_power(-60)

        else:
          if gamepad.get_joystick("Lx") == -100:
            encoder_motor_M2.set_power(60)
            encoder_motor_M3.set_power(-60)
            encoder_motor_M4.set_power(-60)
            encoder_motor_M5.set_power(60)

          else:
            if gamepad.is_key_pressed("Left"):
              encoder_motor_M2.set_power(-40)
              encoder_motor_M3.set_power(-40)
              encoder_motor_M4.set_power(-40)
              encoder_motor_M5.set_power(-40)

            else:
              if gamepad.is_key_pressed("Right"):
                encoder_motor_M2.set_power(40)
                encoder_motor_M3.set_power(40)
                encoder_motor_M4.set_power(40)
                encoder_motor_M5.set_power(40)

              else:
                encoder_motor_M2.set_power(0)
                encoder_motor_M3.set_power(0)
                encoder_motor_M4.set_power(0)
                encoder_motor_M5.set_power(0)

def feed__E0_B8_AB_E0_B8_99_E0_B9_89_E0_B8_B2():
    global Move
    if gamepad.is_key_pressed("R2"):
      power_expand_board.set_power("DC3", -100)

    else:
      if gamepad.is_key_pressed("L2"):
        power_expand_board.stop("DC3")

def Feed():
    global Move
    if gamepad.get_joystick("Ry") == 100:
      power_expand_board.set_power("DC1", 100)

    else:
      if gamepad.get_joystick("Ry") == -100:
        power_expand_board.set_power("DC1", -100)

      else:
        power_expand_board.stop("DC1")

def autowheels():
    global Move
    encoder_motor_M2.set_power(30)
    encoder_motor_M3.set_power(30)
    encoder_motor_M4.set_power(-30)
    encoder_motor_M5.set_power(-30)
    time.sleep(2)
    for i in range(2):
        encoder_motor_M2.set_power(-30)
        encoder_motor_M3.set_power(-30)
        encoder_motor_M4.set_power(30)
        encoder_motor_M5.set_power(30)
        time.sleep(1)
        encoder_motor_M2.set_power(30)
        encoder_motor_M3.set_power(30)
        encoder_motor_M4.set_power(-30)
        encoder_motor_M5.set_power(-30)

    time.sleep(1)
    stop_wheels()
    stop_bl()

def stop_feed():
    global Move
    power_expand_board.set_power("DC3", 0)
    power_expand_board.set_power("DC1", 0)
    power_expand_board.set_power("DC2", 0)
    time.sleep(100)

def automaticstage():
    global Move
    autofeed()
    autowheels()
    auto_bl()
    stop_feed()
    stop_wheels()

def stop_wheels():
    global Move
    encoder_motor_M2.set_power(0)
    encoder_motor_M3.set_power(0)
    encoder_motor_M4.set_power(0)
    encoder_motor_M5.set_power(0)
    time.sleep(100)

def auto_bl():
    global Move
    power_expand_board.stop("BL1")
    power_expand_board.stop("BL2")

def autofeed():
    global Move
    power_expand_board.set_power("DC3", -100)
    power_expand_board.set_power("DC1", 100)
    power_expand_board.set_power("DC2", 100)
    autowheels()
    auto_bl()
    time.sleep(2)
    stop_feed()

def stop_bl():
    global Move
    power_expand_board.set_power("BL1", 100)
    power_expand_board.set_power("BL2", -100)
    power_expand_board.set_power("BL2", 100)

def smartcamera():
    global Move
    smart_camera_1.open_light()
    smart_camera_1.set_mode("color")
    if smart_camera_1.detect_sign(2):
      # DO SOMETHING
      pass

    else:
      if smart_camera_1.detect_sign(1):
        encoder_motor_M2.set_power(-60)
        encoder_motor_M3.set_power(60)
        encoder_motor_M4.set_power(60)
        encoder_motor_M5.set_power(-60)

      else:
        # DO SOMETHING
        pass

while True:
    time.sleep(0.001)
    if power_manage_module.is_auto_mode():
      encoder_motor_M1.set_power(50)
      automaticstage()
      stop_wheels()

    else:
      feed__E0_B8_AB_E0_B8_99_E0_B9_89_E0_B8_B2()
      Move()
      Feed()
      BL()
      Block()
      Laser()
      feedbon()
