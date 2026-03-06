Ayan's Smart Parking System

A **Smart Car Parking System** built using **Arduino, IR sensors, Servo motors, and a Python GUI** that monitors parking slot availability in **real-time**.

This project automatically controls **entry and exit gates** and displays **live parking slot status** on a **modern animated desktop interface**.

---

#  Features

✅ Real-time parking slot monitoring
✅ Automatic entry gate control
✅ Automatic exit gate control
✅ Live GUI with animations
✅ Slot availability statistics
✅ Occupancy rate calculation
✅ Emergency alert system
✅ Serial communication between Arduino and Python GUI

---

#  How the System Works

1. **IR Sensors detect vehicles** in parking slots.
2. Arduino reads sensor data and **counts available slots**.
3. Arduino sends the data through **Serial Communication (USB)**.
4. The **Python GUI reads the serial data** and updates the interface.
5. When a car arrives at the **entry gate**:

   * If slots are available → gate opens.
   * If parking is full → entry remains closed.
6. When a car reaches the **exit gate**, the gate opens automatically.

---

#  Hardware Components

| Component    | Quantity |
| ------------ | -------- |
| Arduino Uno  | 1        |
| IR Sensors   | 6        |
| Servo Motors | 2        |
| Jumper Wires | Several  |
| Breadboard   | 1        |
| USB Cable    | 1        |
| Laptop / PC  | 1        |

---

# 🔌 Circuit Diagram / Connections

## Parking Slot Sensors

| Slot             | Arduino Pin |
| ---------------- | ----------- |
| Slot 1 IR Sensor | D4          |
| Slot 2 IR Sensor | D5          |
| Slot 3 IR Sensor | D6          |
| Slot 4 IR Sensor | D7          |

Each IR sensor detects if a **car is parked in the slot**.

Logic:

HIGH → Slot Empty
LOW → Car Present

---

## Gate Sensors

| Gate Sensor          | Arduino Pin |
| -------------------- | ----------- |
| Entry Gate IR Sensor | D2          |
| Exit Gate IR Sensor  | D3          |

These sensors detect when a **vehicle reaches the gate**.

---

## Servo Motor Connections

| Servo            | Arduino Pin |
| ---------------- | ----------- |
| Entry Gate Servo | D8          |
| Exit Gate Servo  | D9          |

Servo operation:

0° → Gate Closed
90° → Gate Open

---

## IR Sensor Wiring

Each IR sensor has **3 pins**:

| IR Pin | Connection          |
| ------ | ------------------- |
| VCC    | 5V                  |
| GND    | GND                 |
| OUT    | Arduino Digital Pin |

Example:

```
IR Sensor → Arduino
VCC → 5V
GND → GND
OUT → D4 / D5 / D6 / D7
```

---

## Servo Motor Wiring

| Servo Wire      | Connection            |
| --------------- | --------------------- |
| Red             | 5V                    |
| Brown / Black   | GND                   |
| Orange / Yellow | Arduino Pin (D8 / D9) |

---

# 🧾 Arduino Code Overview

The Arduino performs three main tasks:

### 1️⃣ Read Parking Sensors

```
const int slotSensors[] = {4,5,6,7};
```

These sensors determine if parking slots are **occupied or free**.

---

### 2️⃣ Calculate Available Slots

```
if (state == HIGH)
availableSlots++;
```

HIGH means **no car in the slot**.

---

### 3️⃣ Send Data to Computer

Arduino sends data through Serial:

```
SLOTS:3
```

The Python GUI reads this value and updates the interface.

---

### 4️⃣ Gate Automation

**Entry Gate**

```
if (entrySensor == LOW && availableSlots > 0)
```

Gate opens only if:

* A car is detected
* Parking space is available

---

**Exit Gate**

```
if (exitSensor == LOW)
```

Exit gate always opens when a car approaches.

---

# 🖥 Python GUI

The GUI is built using:

* **Tkinter**
* **PySerial**
* **Pygame**

It displays:

* Parking slot status
* Total slots
* Available slots
* Occupied slots
* Occupancy rate

It also includes:

🎨 Animated parking slots
📊 Real-time statistics
🕐 Live clock
🔌 Serial connection indicator
🚨 Emergency alert button

---

# 📡 Serial Communication

The GUI receives data using:

```
SERIAL_PORT = 'COM6'
BAUD_RATE = 9600
```

Make sure the **COM port matches your Arduino port**.

Example output from Arduino:

```
SLOTS:4
SLOTS:3
SLOTS:2
```

---

# 📂 Project Structure

```
smart-parking-system
│
├── arduino
│   └── parking_system.ino
│
├── gui
│   └── parking_gui.py
│
├── assets
│   └── alert.mp3
│
└── README.md
```

---

# ▶ How to Run the Project

## Step 1 — Upload Arduino Code

1. Open **Arduino IDE**
2. Upload `parking_system.ino`
3. Connect Arduino via USB

---

## Step 2 — Install Python Libraries

Install required libraries:

```
pip install pyserial pygame
```

---

## Step 3 — Run GUI

```
python parking_gui.py
```

The dashboard will open showing **live parking data**.

---

# 🧪 Testing Without Hardware

You can simulate parking slots using the **SIMULATE** button in the GUI.

This randomly generates parking data for testing.

---

# 📊 System Example

| Slot   | Status    |
| ------ | --------- |
| Slot 1 | Occupied  |
| Slot 2 | Available |
| Slot 3 | Occupied  |
| Slot 4 | Available |

Available Slots → **2**

---

# 🚀 Future Improvements

Possible upgrades:

* Web-based dashboard
* Mobile app integration
* Camera-based vehicle detection
* Automatic number plate recognition
* Cloud database logging
* IoT integration

---

# 👨‍💻 Author

**Ayan Ahmad**

Software Engineering Student
Smart Systems & Embedded Projects

