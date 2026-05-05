import smbus2
from config import PCF_ADDRESS

bus = smbus2.SMBus(1)

def read_adc(channel):
    bus.write_byte(PCF_ADDRESS, 0x40 | channel)
    bus.read_byte(PCF_ADDRESS)  # dummy read
    return bus.read_byte(PCF_ADDRESS)

