import time
import RPi.GPIO as GPIO

class stepMotor:
	__total_steps = None
	__deg_step = None
	__delay = None
	__position = None
	__pins = None

	__index = 0
	__full_step = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]


	def __init__(self, total_steps, pins, delay=0.02):
		self.__total_steps = total_steps
		self.__delay = delay
		self.__position = 0
		self.__pins = pins
		self.__deg_step = 360/total_steps

		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(pins[0], GPIO.OUT); GPIO.output(pins[0], 1)
		GPIO.setup(pins[1], GPIO.OUT); GPIO.output(pins[1], 0)
		GPIO.setup(pins[2], GPIO.OUT); GPIO.output(pins[2], 0)
		GPIO.setup(pins[3], GPIO.OUT); GPIO.output(pins[3], 0)
		time.sleep(0.01)
		self.off()

	# Control de coils and GPIOs
	def __coils(self, d):
		if (d > 0 and self.__index == 3): self.__index = -1
		if (d < 0 and self.__index == 0): self.__index = 4
		self.__index += d
		self.__position += d

		GPIO.output(self.__pins[0], self.__full_step[self.__index][0])
		GPIO.output(self.__pins[1], self.__full_step[self.__index][1])
		GPIO.output(self.__pins[2], self.__full_step[self.__index][2])
		GPIO.output(self.__pins[3], self.__full_step[self.__index][3])
		time.sleep(self.__delay)


	# Move relative steps
	def move_relative(self, steps):
		if (steps > 0):
			for i in range(0, steps): self.__coils(1)
		else:
			for i in range(steps, 0): self.__coils(-1)

	# Move to absolute position
	def move_absolute(self, position):
		x = self.__position - position
		
		if (x < 0):
			for i in range(x, 0): self.__coils(1)
		else:
			for i in range(0, x): self.__coils(-1)

	# Move to relative angle
	def angle_relative(self, degs):
		steps = round(degs/self.__deg_step)
		if (steps > 0):
			for i in range(0, steps): self.__coils(1)
		else:
			for i in range(steps, 0): self.__coils(-1)
	
	# Move to absolute angle
	def angle_absolute(self, deg):
		steps = round(deg/self.__deg_step)
		x = self.__position - steps
		
		if (x < 0):
			for i in range(x, 0): self.__coils(1)
		else:
			for i in range(0, x): self.__coils(-1)

	# Get current position in steps
	def get_steps(self):
		return self.__position
	
	# Get current position in angle
	def get_angle(self):
		return self.__position*self.__deg_step

	# Turn all pins OFF
	def off(self):
		GPIO.output(self.__pins[0], 0)
		GPIO.output(self.__pins[1], 0)
		GPIO.output(self.__pins[2], 0)
		GPIO.output(self.__pins[3], 0)
