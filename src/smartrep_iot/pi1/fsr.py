import smbus2
import time

from config import PCF_ADDRESS, EQUIPMENT, CHANNEL

bus = smbus2.SMBus(1)


def read_adc(channel):
    control = 0x40 | channel

    bus.write_byte(PCF_ADDRESS, control)
    bus.read_byte(PCF_ADDRESS)  # dummy
    value = bus.read_byte(PCF_ADDRESS)

    return value


def read_adc_stable(channel, samples=5):
    total = 0
    for _ in range(samples):
        total += read_adc(channel)
        time.sleep(0.002)
    return total / samples


def read_all_fsr():
    """
    Returns:
    {
        "dumbbell_left": value,
        "dumbbell_right": value,
        ...
    }
    """
    readings = {}

    for name, cfg in EQUIPMENT.items():
        channel = cfg[CHANNEL]
        readings[name] = read_adc_stable(channel)

    return readings


def any_active(readings):
    """
    TRUE if any equipment is being USED
    (i.e. pressure BELOW threshold → lifted)
    """
    for name, value in readings.items():
        threshold = EQUIPMENT[name]["threshold"]

        if value < threshold:
            return True

    return False


def all_idle(readings):
    """
    TRUE if ALL equipment are resting
    """
    for name, value in readings.items():
        threshold = EQUIPMENT[name]["threshold"]

        if value < threshold:
            return False

    return True