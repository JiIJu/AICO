from periphery import I2C

# Open i2c-0 controller
i2c = I2C("/dev/i2c-1")

# Read byte at address 0x100 of EEPROM at 0x50
msgs = [I2C.Message([0x01, 0x00]), I2C.Message([0x00], read=True)]
i2c.transfer(0x60, msgs)
print("0x100: 0x{:02x}".format(msgs[1].data[0]))

i2c.close()