# En este modulo vamos a implementar las cinematicas del robot 

import math

class Kinematics:
    def __init__(self, wheel_radius, wheel_base, axle_distance):
        self.wheel_radius=wheel_radius
        self.wheel_base=wheel_base
        self.axle_distance=axle_distance

    def inverse_kinematics(self, v, omega):
        """Cinemática inversa: convierte velocidad lineal y angular en velocidades de ruedas en rad/s."""

        omega1 = (v - omega*(self.wheel_base/2.0)) / self.wheel_radius  # Rueda delantera derecha
        omega2 = (v + omega*(self.wheel_base/2.0)) / self.wheel_radius  # Rueda delantera izquierda
        omega3 = (v - omega*(self.wheel_base/2.0)) / self.wheel_radius # Rueda trasera derecha
        omega4 = (v + omega*(self.wheel_base/2.0)) / self.wheel_radius  # Rueda trasera izquierda
        return omega1, omega2, omega3, omega4
    
    def direct_kinematics(self , omega1, omega2, omega3, omega4):
        """Cinemática directa: convierte velocidades de ruedas en velocidad lineal y angular."""
        v_real = (self.wheel_radius* (omega1 + omega2 + omega3 + omega4)) / 4
        omega_real = (self.wheel_radius * (-omega1 + omega2 -omega3 + omega4)) / (2 * self.wheel_base )
        return v_real, omega_real
        