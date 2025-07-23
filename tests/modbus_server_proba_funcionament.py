from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep

# Local IP address of the PC (the one configured on the Ethernet adapter)
server = ModbusServer("84.88.129.100", 502, no_block=True)
print("MODBUS server active on 84.88.129.100:502")
server.start()

try:
    while True:
        # Write value 10 to register 0 (for example, X)
        server.data_bank.set_input_registers(0, [10])
        sleep(0.5)
except Exception as e:
    print(f"Server error: {e}")
    server.stop()
