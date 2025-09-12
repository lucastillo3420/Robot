# Robot Móvil Autónomo con VSLAM - Trabajo de Fin de Grado

![Imagen del robot](https://github.com/lucastillo3420/Robot/blob/main/Robot.jpg?raw=true ) 

Este repositorio contiene el software, la configuración y la documentación desarrollados para el **Trabajo de Fin de Grado**:

> **Diseño e Implementación de un Robot Móvil Autónomo con VSLAM basado en Cámara RGB-D**

El proyecto incluye el diseño, construcción y programación de una plataforma robótica de bajo coste capaz de **mapear y navegar de forma autónoma en interiores**, utilizando **ROS 2**, **RTAB-Map** y **Nav2**.

---

##  Características Principales

-  **Plataforma robótica completa:** robot de 4 ruedas con tracción diferencial (*skid-steer*).
-  **Control de bajo nivel:** driver ROS 2 propio que gestiona cinemática, odometría y comunicación con motores.
-  **Mapeo visual-inercial (VSLAM):** integración de cámara RGB-D e IMU mediante **RTAB-Map**.
-  **Navegación autónoma:** pila de navegación **Nav2** para localización, planificación y evasión de obstáculos.
-  **Arquitectura modular:** paquetes ROS 2 bien estructurados y mantenibles.

---

##  Componentes Hardware

- **Chasis:** goBILDA Recon 4WD  
- **Motores:** 4x GoBILDA 5203 con encoder (537.7 PPR)  
- **Controladoras:** 2x RoboClaw 2x7A  
- **Procesador:** Raspberry Pi 5 (8GB)  
- **Sensor principal:** Cámara RGB-D Luxonis OAK-D Lite  
- **IMU:** WitMotion WT901C  
- **Batería:** LiPo 4S 3700 mAh + reguladores  

---

##  Arquitectura de Software

Sistema basado en **Ubuntu 24.04 LTS** y **ROS 2 Jazzy Jalisco**.

### Paquetes clave:
- `robot_driver` → driver propio de bajo nivel (cinemática, odometría, motores).
  - `robot_driver_node.py`: nodo central, suscribe `/cmd_vel` y publica `/odom/wheel`.
  - **Clases internas**:
    - `RoboClawInterface`: comunicación con controladoras.
    - `Kinematics`: cinemática directa e inversa.
    - `RobotOdometry`: estimación de pose (x, y, θ).
- `depthai_ros_driver`: driver oficial de la cámara OAK-D Lite.
- `witmotion_ros`: driver para la IMU.

---

##  Instalación

### Prerrequisitos
- Ubuntu 24.04 LTS  
- ROS 2 Jazzy Jalisco  
- Git
- RTAB-Map
- Nav2

### Clonar el repositorio
```bash
cd ~/ros2_ws/src
git clone --recurse-submodules https://github.com/lucastillo3420/Robot.git
cd ~/ros2_ws
colcon build
source install/setup.bash
````

---

##  Uso del Sistema

El sistema puede funcionar en **dos modos principales**: **Mapeo** y **Navegación Autónoma**.

---

### 🔹 1. Mapeo del Entorno

Permite crear un mapa nuevo con RTAB-Map.

**Terminal 1 – Sistema de mapeo (cámara + RTAB-Map):**

```bash
ros2 launch depthai_ros_driver rtabmap.MapaVisual.py
```

**Terminal 2 – Driver del robot:**

```bash
ros2 run robot_driver robot_driver_node
```

**Terminal 3 – Control manual:**

```bash
# Opción A: Joystick virtual
ros2 run teleop_twist_qt teleop_twist_qt

# Opción B: Teclado
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Conduce lentamente el robot por el entorno, cubriendo todas las áreas.
Para guardar el mapa, cierra primero RTAB-Map con `Ctrl+C`.

---

### 🔹 2. Navegación Autónoma

Usa un mapa previamente creado para navegar con Nav2.

**Terminal 1 – Localización con RTAB-Map:**

```bash
ros2 launch depthai_ros_driver rtabmap.launchNavegacion.py
```

**Terminal 2 – Navegación con Nav2:**

```bash
ros2 launch robot_driver navegacion.launch.py
```

En **RViz**:

1. Espera a que cargue el mapa.
2. Usa **2D Pose Estimate** para indicar la posición inicial del robot.
3. Usa **Nav2 Goal** para enviar un destino.

El robot planificará y navegará de forma autónoma evitando obstáculos.

---






```
