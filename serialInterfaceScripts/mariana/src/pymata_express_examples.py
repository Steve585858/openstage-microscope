
#https://htmlpreview.github.io/?https://github.com/MrYsLab/pymata-express/blob/master/html/pymata_express/index.html#pymata_express.pymata_express.PymataExpress.set_pin_mode_servo
#https://github.com/MrYsLab/pymata-express
import asyncio
import sys, time

from pymata_express import pymata_express
from pymata_express_base import PEBase

from PyQt5.QtCore import QThread

class ConcurrentTasks(PEBase):

    def __init__(self, board, ctrl={'break': False}):
        super().__init__(board)

        # digital pins
        self.white_led = 11
        self.blue_led = 12
        self.green_led = 8

        # analog pin
        self.potentiometer = 5

        self.ctrl = ctrl

    async def potentiometer_change_callback(self, data):
        """
        Call back to receive potentiometer changes.
        Scale the reported value between 0 and ~127 to
        control the green led.
        :param data: [pin, current reported value, pin_mode, timestamp]
        """
        
        scaled_value = data[1] // 4
        await self.board.analog_write(self.green_led, scaled_value)

    async def blink_white(self):  
        await self.board.set_pin_mode_digital_output(self.white_led)
        await self.blink_led(self.white_led, 1)
        return 'white'
    
    async def blink_blue(self):  
        await self.board.set_pin_mode_digital_output(self.blue_led)
        await self.blink_led(self.blue_led, .5)
        return 'blue'
    
    def callback(self, context):
        print("Task result:%s"%context.result())
            
    async def blink(self):
        self.task1 = asyncio.ensure_future(self.blink_white())
        self.task2 = asyncio.ensure_future(self.blink_blue())

        self.task1.add_done_callback(self.callback)
        self.task2.add_done_callback(self.callback)

        await asyncio.gather(self.task1, self.task2)

    def close_blink(self):
        self.task1.close()
        self.task2.close()

    async def async_init_and_run(self):
        await self.board.set_pin_mode_digital_output(self.white_led)
        await self.board.set_pin_mode_digital_output(self.blue_led)
        await self.board.set_pin_mode_pwm(self.green_led)
        await self.board.set_pin_mode_analog_input(self.potentiometer, self.potentiometer_change_callback)
        # start a 5 second period for you to manipulate the 5
        print('You have 5 seconds to manipulate the pin input.')

        await asyncio.sleep(5)
        value, time_stamp = await self.board.analog_read(self.potentiometer)
        print(f'Print polling the pin: value = {value} ')

        await self.board.disable_analog_reporting(self.potentiometer)

        print('Reporting is disabled. You have another 5 seconds '
              'to manipulate the pin to see that reporting has ceased')
        value, time_stamp = await self.board.analog_read(self.potentiometer)
        await asyncio.sleep(5)

        print(f'Print polling the pin: value = {value} ')

        await self.board.enable_analog_reporting(self.potentiometer, callback=self.potentiometer_change_callback)

        print('Reporting is now re-enabled. You have 5 seconds to '
              'manipulate the pin until the program exits')

        await asyncio.sleep(5)
        value, time_stamp = await self.board.analog_read(self.potentiometer)
        print(f'Print polling the pin: value = {value} ')

        # Create the 2 additional tasks
        white_led_task = asyncio.create_task(self.blink_led(self.white_led, 1))
        blue_led_task = asyncio.create_task(self.blink_led(self.blue_led, .5))
        # start the 2 tasks
        await white_led_task
        await blue_led_task

    async def blink_led(self, pin, sleep):
        toggle = 0
        while True:
            await self.board.digital_pin_write(pin, toggle)
            await asyncio.sleep(sleep)
            toggle ^= 1
            if self.ctrl['break']:
                await self.board.digital_pin_write(pin, 0)
                break 



class LED(QThread):

    def __init__(self, board, ctrl={'break': False}):
        super().__init__()
        self.board = board
        self.ctrl = ctrl

        # digital pins
        self.white_led = 11
        self.blue_led = 12
        self.green_led = 8


    async def blink_white(self):  
        await self.board.set_pin_mode_digital_output(self.white_led)
        await self.blink_led(self.white_led, 1)
        return 'white'
    
    async def blink_blue(self):  
        await self.board.set_pin_mode_digital_output(self.blue_led)
        await self.blink_led(self.blue_led, .5)
        return 'blue'
    
    def callback(self, context):
        print("Task result:%s"%context.result())
            
    async def run(self):
        self.task1 = asyncio.ensure_future(self.blink_white())
        self.task2 = asyncio.ensure_future(self.blink_blue())

        self.task1.add_done_callback(self.callback)
        self.task2.add_done_callback(self.callback)

        await asyncio.gather(self.task1, self.task2)

    def close_blink(self):
        self.task1.close()
        self.task2.close()

    
    async def blink_led(self, pin, sleep):
        toggle = 0
        while True:
            await self.board.digital_pin_write(pin, toggle)
            await asyncio.sleep(sleep)
            toggle ^= 1
            if self.ctrl['break']:
                print('break because flag raised')
                break 

