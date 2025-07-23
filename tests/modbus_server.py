from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep

# IP local del PC (la que configuraste en el adaptador Ethernet)
server = ModbusServer("84.88.129.100", 502, no_block=True)
print("🟢 Servidor MODBUS activo en 84.88.129.100:502")
server.start()

try:
    while True:
        # Escribir valor 10 en el registro 0 (por ejemplo, X)
        server.data_bank.set_input_registers(0,[10])
        sleep(0.5)
except Exception as e:
    print(f"🛑 Error en el servidor: {e}")
    server.stop()

