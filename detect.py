import cv2
import streamlit as st
import numpy as np
import pygame
import smtplib
import os
import tempfile
from email.message import EmailMessage
from datetime import datetime
from keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from keras.models import Model
from sklearn.cluster import KMeans

# ---------------------------- Streamlit UI Setup ----------------------------
st.set_page_config(page_title="Intrusion Detection System", layout="wide")
st.markdown("""
    <style>
    body {
        background-color: #f7f9fc;
    }
    .main {
        background-color: #eaf4ff;
        padding: 20px;
        border-radius: 10px;
    }
    </style>
    <div class="main">
        <h1 style='color: #003366;'>🚨 Intrusion Detection System</h1>
    </div>
""", unsafe_allow_html=True)

st.sidebar.title("Input Options")
feed_type = st.sidebar.radio("Choose Input Type:", ("Webcam", "Upload Video"))
start_detection = st.sidebar.checkbox("Start System")

# ---------------------------- Buzzer Setup ----------------------------
def play_buzzer():
    pygame.mixer.init()
    try:
        pygame.mixer.music.load("buzzer-or-wrong-answer-20582.mp3")
        pygame.mixer.music.play()
    except Exception as e:
        st.error(f"Buzzer Error: {e}")

# ---------------------------- Email Alert ----------------------------
def send_email_alert():
    SENDER_EMAIL = st.secrets["sender_email"]
    SENDER_PASSWORD = st.secrets["sender_password"]
    RECEIVER_EMAIL = st.secrets["receiver_email"]

    msg = EmailMessage()
    msg.set_content("Intrusion detected at your premises.")
    msg["Subject"] = "Intrusion Alert"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        st.success("Email Alert Sent!")
    except Exception as e:
        st.error(f"Email failed: {e}")

# ---------------------------- Load Detection Model ----------------------------
prototxt = "MobileNetSSD_deploy.prototxt.txt"
model_file = "MobileNetSSD_deploy.caffemodel"
if not os.path.isfile(prototxt) or not os.path.isfile(model_file):
    st.error("Model files not found. Make sure 'MobileNetSSD_deploy.prototxt' and 'MobileNetSSD_deploy.caffemodel' are present.")
    st.stop()

net = cv2.dnn.readNetFromCaffe(prototxt, model_file)
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

try:
    base_model = MobileNetV2(weights="imagenet", include_top=False, pooling="avg")
    feature_model = Model(inputs=base_model.input, outputs=base_model.output)
except Exception as e:
    st.error("Failed to load MobileNetV2 model. Please check your installation.")
    st.stop()

# ---------------------------- Detection Logic ----------------------------
def detect_intrusion_with_zone(frame):
    if len(frame.shape) == 2 or frame.shape[2] == 1:
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    h, w = frame.shape[:2]
    zone_width = int(0.60 * w)
    zone_top_left = (w - zone_width, 0)
    zone_bottom_right = (w, h)

    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()
    intrusion_detected = False

    cv2.rectangle(frame, zone_top_left, zone_bottom_right, (0, 255, 255), 2)

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            idx = int(detections[0, 0, i, 1])
            if CLASSES[idx] == "person":
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                center_x = int((startX + endX) / 2)
                center_y = int((startY + endY) / 2)

                in_zone = zone_top_left[0] <= center_x <= zone_bottom_right[0] and zone_top_left[1] <= center_y <= zone_bottom_right[1]
                if in_zone:
                    color = (0, 0, 255)
                    label = "Intruder"
                    intrusion_detected = True
                else:
                    color = (0, 255, 0)
                    label = "Authorized"

                cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
                cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    return frame, intrusion_detected

# ---------------------------- Video Feed ----------------------------
if start_detection:
    stframe = st.empty()
    alert_sent = False

    if feed_type == "Webcam":
        cap = cv2.VideoCapture(0)
    else:
        video_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])
        if video_file is not None:
            if 'temp_video_path' not in st.session_state:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tfile:
                    tfile.write(video_file.read())
                    st.session_state.temp_video_path = tfile.name
            cap = cv2.VideoCapture(st.session_state.temp_video_path)
        else:
            st.warning("Upload a video to start.")
            st.stop()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (640, 480))
        result_frame, intrusion = detect_intrusion_with_zone(frame)

        if intrusion and not alert_sent:
            play_buzzer()
            send_email_alert()
            alert_sent = True
            cv2.putText(result_frame, "Intrusion Detected!", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        stframe.image(result_frame, channels="BGR")

    cap.release()
    if "temp_video_path" in st.session_state:
        try:
            os.remove(st.session_state["temp_video_path"])
        except Exception:
            st.warning("Could not delete temp file. It may still be in use.")
        del st.session_state["temp_video_path"]
