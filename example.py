import time
from stepMotor import stepMotor

# Init motor 'm1' with 2048 steps connected to pins (6, 13, 19, 26) with 4ms of delay between steps
m1 = stepMotor(2048, (6, 13, 19, 26), 0.004)

# Move 90 degres
m1.angle_relative(90)

time.sleep(1)

# Move -45 degress
m1.angle_relative(-45)

# Turn off all the coils (to save power and !heat)
m1.off()
