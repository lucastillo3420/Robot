# Robot Móvil Autónomo con VSLAM - Trabajo de Fin de Grado

![Imagen del robot en funcionamiento](https://github.com/lucastillo3420/Robot/blob/main/docs/robot_completo.jpg?raw=true) 

Este repositorio contiene todo el software, la configuración y la documentación desarrollados para el Trabajo de Fin de Grado: "Diseño e Implementación de un Robot Móvil Autónomo con VSLAM basado en Cámara RGB-D".

El proyecto abarca el diseño completo, la construcción y la programación de una plataforma robótica de bajo coste capaz de realizar mapeo y navegación autónoma en entornos de interior utilizando ROS 2, RTAB-Map y Nav2.

---

## Características Principales

- **Plataforma Robótica Completa:** Diseño y construcción de un robot de 4 ruedas con tracción diferencial (*skid-steer*).
- **Control de Bajo Nivel:** Un driver de ROS 2 personalizado que gestiona la cinemática, la odometría de ruedas y la comunicación con las controladoras de motores.
- **Mapeo Visual-Inercial (VSLAM):** Utiliza **RTAB-Map** para fusionar los datos de una cámara RGB-D y una IMU, generando mapas 2D consistentes y métricamente precisos.
- **Navegación Autónoma:** Integra la pila de navegación **Nav2** para la localización, planificación de rutas y evasión de obstáculos en mapas previamente generados.
- **Arquitectura Modular:** El sistema está dividido en paquetes de ROS 2 con responsabilidades claras, siguiendo las mejores prácticas del ecosistema.

---

## Componentes Hardware

La plataforma ha sido construida utilizando los siguientes componentes principales:
- **Chasis:** goBILDA Recon de 4 ruedas motrices.
- **Motores:** 4x Motores planetarios GoBILDA 5203 Series con encoder integrado (537.7 PPR).
- **Controladoras de Motor:** 2x RoboClaw 2x7A.
- **Unidad de Procesamiento Principal:** Raspberry Pi 5 (8GB).
- **Sensor de Percepción Principal:** Cámara inteligente RGB-D Luxonis OAK-D Lite.
- **Sensor Inercial:** IMU WitMotion WT901C.
- **Alimentación:** Batería LiPo 4S 3700mAh y placas de regulación de voltaje.

---

## Arquitectura del Software

El sistema opera sobre **Ubuntu 24.04 LTS** y **ROS 2 Jazzy Jalisco**. La arquitectura se compone de los siguientes paquetes y nodos clave:

- **`robot_driver`:** Paquete personalizado que contiene:
  - `robot_driver_node`: Se comunica con las controladoras RoboClaw, aplica la cinemática y publica la odometría de las ruedas (`/odom/wheel`).
  - Clases de abstracción para la cinemática, la odometría y la interfaz de hardware.

- **`depthai_ros_driver`:** Driver oficial para la cámara OAK-D Lite.
- **`witmotion_ros`:** Driver para la IMU WitMotion.
- **`rtabmap_ros`:** Utilizado para la odometría visual y el SLAM.
- **`robot_localization` (EKF):** Utilizado para la fusión de la odometría de ruedas y la IMU, proporcionando una odometría base robusta.
- **`nav2`:** Pila de navegación completa para la localización (AMCL), planificación y control.

---

## Instalación y Puesta en Marcha

### 1. Prerrequisitos
- Un ordenador con Ubuntu 24.04 LTS.
- ROS 2 Jazzy Jalisco instalado.
- Git instalado.

### 2. Clonar el Repositorio
Navega a tu workspace de ROS 2 y clona este repositorio.

```bash
cd ~/ros2_ws/src
git clone --recurse-submodules https://github.com/lucastillo3420/Robot.git
