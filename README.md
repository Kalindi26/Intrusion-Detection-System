# 🚨 Intrusion Detection System

**A real-time intrusion detection system that restricts unauthorized people from entering a marked restricted area using computer vision.**

---

## 📝 Description

This project detects human intrusion into a predefined **restricted zone** (highlighted in yellow) using object detection. If a person enters this zone, they are marked as an **Intruder**, and alerts are triggered (buzzer and email). People outside this zone are considered **Authorized**. The restricted zone is marked visually and can be adjusted as per the application's needs. The system supports both **live webcam feeds** and **uploaded video files** through a simple Streamlit interface.

---

## 🎯 Features

- 📹 **Live Webcam** and **Uploaded Video** support  
- 🧠 **MobileNet SSD** object detection for real-time person detection  
- 🟨 **Customizable restricted area** (highlighted in yellow)  
- 🚨 **Intrusion alerts**:
  - 🔊 Buzzer sound (via Pygame)
  - 📧 Email notifications
- 🎛️ Clean and user-friendly **Streamlit interface**

---

## 💡 How It Works

A specific region in the video frame is designated as a **restricted area**, visually marked with a yellow bounding box. When a person enters this area, they are identified as an **Intruder**, and the system plays a buzzer sound and sends an email alert. Individuals outside the zone are marked as **Authorized**. The restricted area can be adjusted as per user needs, making the system suitable for many real-life scenarios.

---

## 🔍 Applications

This system has several real-world use cases, including:

- 🏠 **Home Security**: Monitor entrances or garages, and detect trespassers entering private property.
- 🚗 **Vehicle Theft Prevention**: Integrate with CCTV and motorized gates to detect unauthorized access near parked vehicles.
- 🏢 **Office Surveillance**: Secure sensitive areas like server rooms, labs, or confidential zones.
- 🏫 **Campus Safety**: Restrict access to faculty-only areas or storage rooms.
- 🏭 **Industrial Use**: Prevent entry into hazardous zones like machinery or chemical storage areas.
- 🏛️ **Public Places**: Secure monuments, museums, or exhibitions where access is restricted.

> This system can be further enhanced by integrating with IoT-based locking mechanisms, automatic gates, or smart sirens.

---

## 📦 Setup Instructions

To get the Intrusion Detection System up and running on your machine, follow these steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/intrusion-detection-system.git
   cd intrusion-detection-system
````

2. **Install Required Libraries**
   Install all necessary Python packages using:

   ```bash
   pip install -r requirements.txt
   ```

3. **Download MobileNet SSD Model Files**
   Download the following files and place them in the root project directory:

   * [`MobileNetSSD_deploy.prototxt.txt`](https://github.com/chuanqi305/MobileNet-SSD/blob/master/MobileNetSSD_deploy.prototxt)
   * [`MobileNetSSD_deploy.caffemodel`](https://github.com/chuanqi305/MobileNet-SSD/blob/master/MobileNetSSD_deploy.caffemodel)

4. **Add a Buzzer Sound File**
   Download or use an existing `.mp3` buzzer sound file (like `buzzer-or-wrong-answer-20582.mp3`) and place it in the root directory. This will be played when an intrusion is detected.

5. **Set Up Email Alerts**
   For email notifications, create a `.streamlit/secrets.toml` file with the following format:

   ```toml
   sender_email = "your_email@gmail.com"
   sender_password = "your_app_password"
   receiver_email = "receiver_email@example.com"
   ```

   > ⚠️ If using Gmail, make sure to enable 2-Step Verification and create an **App Password** for enhanced security.

6. **Run the System**
   Start the Streamlit application using:

   ```bash
   streamlit run app.py
   ```

   From the sidebar, select your video source (Webcam or Uploaded Video), then check the "Start System" box to begin detection.

---

## 📁 File Structure

```
intrusion-detection-system/
│
├── app.py
├── requirements.txt                
├── MobileNetSSD_deploy.caffemodel  
├── MobileNetSSD_deploy.prototxt.txt 
├── buzzer-or-wrong-answer-20582.mp3 
├── README.md                       
└── .streamlit/
    └── secrets.toml                
```

---



## 📸 Demo Preview

## 📸 Demo Preview

![Intrusion Output](https://github.com/Kalindi26/Intrusion-Detection-System/blob/main/demo_img.png?raw=true)





---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🤝 Acknowledgments

* [MobileNet SSD](https://github.com/chuanqi305/MobileNet-SSD)
* [Streamlit](https://streamlit.io/)
* [OpenCV](https://opencv.org/)

```


