import smbus

# Adresse des Sensors (0x0D oder 0x1E je nachdem, was du siehst)
address = 0x0D

# Bus-Objekt
bus = smbus.SMBus(1)

# WHO_AM_I-Register (0x0F)
who_am_i = bus.read_byte_data(address, 0x0F)

print(f"WHO_AM_I: {hex(who_am_i)}")
