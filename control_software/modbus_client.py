from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient('192.168.100.9')
client.write_coil(0, False)
result = client.read_coils(1,1)
print(result.bits[0])
client.close()