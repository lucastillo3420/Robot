"""Módulo robot_roboclaw:
Este módulo manejará la comunicación con las controladoras RoboClaw.
Archivo: robot_roboclaw/robot_roboclaw/roboclaw_interface.py"""

from roboclaw_3 import Roboclaw

class RoboClawInterface:
    
    def __init__(self, port_delantero, port_trasero, buadrate ):
        # Configuración de RoboClaw
        self.address=0x80 
        self.rc_delantero = Roboclaw(port_delantero, buadrate )  # Controladora para motores delanteros
        self.rc_trasero = Roboclaw(port_trasero, buadrate)    # Controladora para motores traseros
        if not self.rc_delantero.Open() or not self.rc_trasero.Open():
            raise Exception("Error: No se pudo abrir la conexión con las controladoras Roboclaw.")
        

        self.ERROR_MESSAGES = {
            0x0000: "Normal",
            0x0001: "Advertencia: Sobrecorriente Motor 1",
            0x0002: "Advertencia: Sobrecorriente Motor 2",
            0x0004: "Error: Desconexión de Emergencia",
            0x0008: "Error: Fallo de Temperatura",
            0x0010: "Error: Fallo de Temperatura 2",
            0x0020: "Error: Batería Principal Baja",
            0x0040: "Error: Batería Lógica Baja",
            0x0080: "Error: Fallo Lógico",
            0x0100: "Error: Fallo del Driver Motor 1",
            0x0200: "Error: Fallo del Driver Motor 2",
            0x0400: "Advertencia: Límite de Velocidad Motor 1",
            0x0800: "Advertencia: Límite de Velocidad Motor 2" 
        }
            
    def set_wheel_speed(self, front_left, front_right, rear_left, rear_right):
        # Enviar las velocidades a los motores
            self.rc_delantero.SpeedM1(self.address, front_left)
            self.rc_delantero.SpeedM2(self.address, front_right)
            self.rc_trasero.SpeedM1(self.address, rear_left)
            self.rc_trasero.SpeedM2(self.address, rear_right)

    def read_encoders_speed(self):
         # Leer encoders y calcular velocidades reales en rad/s
        status_d1, enc_d1, dir_d1 = self.rc_delantero.ReadSpeedM1(self.address)
        status_d2, enc_d2, dir_d2 = self.rc_delantero.ReadSpeedM2(self.address)
        status_t1, enc_t1, dir_t1 = self.rc_trasero.ReadSpeedM1(self.address)
        status_t2, enc_t2, dir_t2 = self.rc_trasero.ReadSpeedM2(self.address)
        return enc_d1, enc_d2, enc_t1, enc_t2
    
    def read_encoders_position(self):
        """Lee posición absoluta de encoders (pulsos)."""
        status_d1, enc_d1, dir_d1 = self.rc_delantero.ReadEncM1(self.address)
        status_d2, enc_d2, dir_d2 = self.rc_delantero.ReadEncM2(self.address)
        status_t1, enc_t1, dir_t1 = self.rc_trasero.ReadEncM1(self.address)
        status_t2, enc_t2, dir_t2 = self.rc_trasero.ReadEncM2(self.address)
        return enc_d1, enc_d2, enc_t1, enc_t2

    def reset_encoders(self):
        """Resetea los encoders."""
        self.rc_delantero.ResetEncoders(self.address)
        self.rc_trasero.ResetEncoders(self.address)
        print("Encoders reseteados a 0.")
    
    def ReadVoltage(self):
        # Leer el voltaje de la batería principal
        voltage_max=16.8 #voltage maximo de la bateria
        voltage_min=13.2
        voltage = self.rc_delantero.ReadMainBatteryVoltage(self.address)
        if voltage[0]:  # Si la lectura fue exitosa
                voltage_value=voltage[1]/10.0 # Convertir a voltios
                battery_porcentage=((voltage_value-voltage_min)/(voltage_max-voltage_min))*100
                return voltage_value, battery_porcentage  
        else:
            raise Exception("Error al leer el voltaje de la batería principal")
            return None
    
    def check_status(self):
        """
        Lee la corriente y el estado de error de ambas controladoras
        y lo imprime en la consola de forma legible.
        """
        # --- Controladora Delantera ---
        status_c_d, current_d1, current_d2 = self.rc_delantero.ReadCurrents(self.address)
        status_e_d, error_d = self.rc_delantero.ReadError(self.address)
        
        print("\n--- Diagnóstico Roboclaw ---")
        print("Controladora Delantera:")
        if status_c_d:
            print(f"  Corriente Ruedas (Izq/Der): {current_d1 / 100.0:.2f} A / {current_d2 / 100.0:.2f} A")
        else:
            print("  No se pudo leer la corriente.")
        if status_e_d:
            error_msg = self.ERROR_MESSAGES.get(error_d, f"Código desconocido: {hex(error_d)}")
            print(f"  Estado de Error: {error_msg}")
           
        else:
            print("  No se pudo leer el estado de error.")

        # --- Controladora Trasera ---
        status_c_t, current_t1, current_t2 = self.rc_trasero.ReadCurrents(self.address)
        status_e_t, error_t = self.rc_trasero.ReadError(self.address)
        print(f"error crudo: ({hex(error_t)})")
        
        print("Controladora Trasera:")
        if status_c_t:
            print(f"  Corriente Ruedas (Izq/Der): {current_t1 / 100.0:.2f} A / {current_t2 / 100.0:.2f} A")
        else:
            print("  No se pudo leer la corriente.")
        if status_e_t:
            error_msg = self.ERROR_MESSAGES.get(error_t, f"Código desconocido: {hex(error_t)}")
            print(f"  Estado de Error: {error_msg}")
           
        else:
            print("  No se pudo leer el estado de error.")
        print("----------------------------")

