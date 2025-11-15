# Hand Tracking LED Control with STM32

A real-time hand tracking system built using **OpenCV** and **MediaPipe**, which sends commands over **UART** to an STM32 microcontroller to control LEDs.  
This project demonstrates how computer vision can interact with embedded hardware in a simple and effective way.

---

## ✨ Features
- Real-time hand tracking using MediaPipe  
- Detects fingertip position and checks box intersections  
- Sends `'R'`, `'B'`, `'Y'` commands to STM32 through UART (115200 baud)  
- STM32 toggles LEDs on PC2, PC3, and PA10  
- Stable communication at **3 Hz**  
- Clean and lightweight Python + STM32 implementation  

---

## 🖥️ PC / Python Side

The computer vision application is implemented in `main.py`.

### Technologies used:
- Python 3.x  
- OpenCV  
- MediaPipe  
- PySerial  

### How it works:
- The camera detects your hand and tracks your index fingertip.
- When your finger enters a colored box, the script sends a UART character:
  - **Blue Box → `'B'`**
  - **Yellow Box → `'Y'`**
  - **Red Box → `'R'`**

---

## 🔧 STM32 Side (Firmware)

The STM32 code listens for UART characters using interrupt mode:

- `'R'` toggles **PC3**  
- `'B'` toggles **PC2**  
- `'Y'` toggles **PA10**  

This logic is implemented inside:

