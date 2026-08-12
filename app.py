import streamlit as st
from deepface import DeepFace
import cv2
import pandas as pd
import os
from datetime import datetime
from PIL import Image
import tempfile

st.set_page_config(page_title="AI Face Analysis", layout="wide")

# ---------------------- CSS ----------------------

st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp{
    background: radial-gradient(circle at top,#0f172a,#020617);
    color:white;
}

/* GRID BACKGROUND */
.stApp::before{
    content:"";
    position:fixed;
    top:0;
    left:0;
    width:100%;
    height:100%;
    background-image:
        linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px);
    background-size:60px 60px;
    pointer-events:none;
}

/* NAVB
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:10px 20px;
    border-bottom:1px solid rgba(255,255,255,0.1);
}

.logo{
    font-size:22px;
    font-weight:bold;
}

.logo span{
    color:#00F5D4;
}

/* HERO */
.hero{
    text-align:center;
    padding-top:80px;
}

.title{
    font-size:72px;
    font-weight:800;
}

.highlight{
    color:#00F5D4;
    text-shadow:0px 0px 20px #00F5D4;
}

.subtitle{
    color:#94a3b8;
    font-size:20px;
    margin-top:15px;
}

/* BUTTONS */AR */
.navbar{
.btn{
    display:inline-block;
    padding:12px 30px;
    margin:20px 10px;
    border-radius:10px;
    font-weight:bold;
    border:1px solid #00F5D4;
}

.btn-primary{
    background:#00F5D4;
    color:black;
}

.btn-outline{
    color:#00F5D4;
}

/* STATS */
.stats{
    display:flex;
    justify-content:center;
    gap:120px;
    margin-top:60px;
}

.stat{
    text-align:center;
}

.stat-number{
    font-size:36px;
    font-weight:bold;
    color:#00F5D4;
}

.card{
    background:rgba(255,255,255,0.05);
    border-radius:15px;
    padding:30px;
    text-align:center;
    border:1px solid rgba(255,255,255,0.08);
}

.card:hover{
    box-shadow:0 0 20px rgba(0,255,200,0.5);
}

.metric{
    background:#111827;
    padding:20px;
    border-radius:12px;
    text-align:center;
}

.name{
    font-size:50px;
    font-weight:bold;
    color:#00F5D4;
    text-align:center;
    text-shadow:0px 0px 20px #00F5D4;
}

</style>
""", unsafe_allow_html=True)


# ---------------------- HERO ----------------------
st.markdown("""
<div class="hero">

<div class="title">
AI <span class="highlight">Face Analysis</span>
</div>

<div class="subtitle">
Intelligent AI-powered face detection & recognition for real-time
security, surveillance, and identity verification.
</div>

</div>
""", unsafe_allow_html=True)


# ---------------------- STATS ----------------------

st.markdown("""
<style>
.metric-container {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    margin-top: 20px;
}

.metric-card {
    background: #111827;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    flex: 1;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
    transition: 0.3s;
}

.metric-card:hover {
    transform: translateY(-5px);
}

.metric-value {
    font-size: 32px;
    font-weight: bold;
    color: #00FFA3;
}

.metric-label {
    font-size: 14px;
    color: #9CA3AF;
    margin-top: 5px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="metric-container">
    <div class="metric-card">
        <div class="metric-value">99.7%</div>
        <div class="metric-label">Accuracy</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">&lt;50ms</div>
        <div class="metric-label">Latency</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">24/7</div>
        <div class="metric-label">Monitoring</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()


# ---------------------- SIDEBAR ----------------------
menu = st.sidebar.radio(
"Navigation",
["Home","Register Face","Upload Image","Live Camera","Attendance Log"]
)


# ---------------------- ATTENDANCE ----------------------
def mark_attendance(name):

    now = datetime.now()

    row = {
        "Name":name,
        "Date":now.strftime("%Y-%m-%d"),
        "Time":now.strftime("%H:%M:%S")
    }

    try:
        df = pd.read_csv("attendance.csv")
        df = pd.concat([df,pd.DataFrame([row])])
    except:
        df = pd.DataFrame([row])

    df.to_csv("attendance.csv",index=False)


# ---------------------- HOME ----------------------
if menu == "Home":

    col1,col2,col3 = st.columns(3)

    col1.markdown("""
    <div class="card">
    <h3>📷 Face Recognition</h3>
    Identify people using AI
    </div>
    """, unsafe_allow_html=True)

    col2.markdown("""
    <div class="card">
    <h3>🎥 Live Monitoring</h3>
    Real-time camera detection
    </div>
    """, unsafe_allow_html=True)

    col3.markdown("""
    <div class="card">
    <h3>📊 Attendance System</h3>
    Automatic attendance logging
    </div>
    """, unsafe_allow_html=True)


# ---------------------- REGISTER ----------------------
elif menu == "Register Face":

    st.header("Register New Face")

    if "name_confirmed" not in st.session_state:
        st.session_state.name_confirmed = False

    if "camera_on" not in st.session_state:
        st.session_state.camera_on = False

    # ---------- NAME INPUT ----------
    name_input = st.text_input("Enter Name")

    if not st.session_state.name_confirmed:

        if st.button("✔ Confirm Name"):

            if name_input == "":
                st.warning("Please enter a name.")
            else:
                st.session_state.name_confirmed = True
                st.session_state.person_name = name_input

    # ---------- AFTER NAME CONFIRMED ----------
    if st.session_state.name_confirmed:

        name = st.session_state.person_name

        st.success(f"Registering: {name}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("📷 Open Camera"):
                st.session_state.camera_on = True

        with col2:
            if st.button("❌ Close Camera"):
                st.session_state.camera_on = False

        # ---------- CAMERA ----------
        if st.session_state.camera_on:

            col1, col2, col3 = st.columns([1,2,1])

            with col2:
                image_file = st.camera_input("Capture Face")

            if image_file is not None:

                image = Image.open(image_file)

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("💾 Save Photo"):

                        path = f"database/{name}"
                        os.makedirs(path, exist_ok=True)

                        count = len(os.listdir(path))

                        file_path = f"{path}/{name}_{count+1}.jpg"

                        image.save(file_path)

                        st.success("Face saved successfully!")

                with col2:
                    if st.button("🔄 Retry"):

                        st.session_state.camera_on = False
                        st.rerun()

# ---------------------- IMAGE RECOGNITION ----------------------
elif menu == "Upload Image":

    st.header("Upload Image Recognition")

    uploaded = st.file_uploader("Upload Image",type=["jpg","png","jpeg"])

    if uploaded:

        image = Image.open(uploaded)

        st.image(image,width=350)

        with tempfile.NamedTemporaryFile(delete=False,suffix=".jpg") as temp:
            image.save(temp.name)

        analysis = DeepFace.analyze(
            img_path=temp.name,
            actions=['age','gender','emotion'],
            enforce_detection=False
        )

        result = DeepFace.find(
            img_path=temp.name,
            db_path="database",
            enforce_detection=False
        )

        age = analysis[0]["age"]
        gender = analysis[0]["dominant_gender"]
        emotion = analysis[0]["dominant_emotion"]

        if len(result[0])>0:

            identity = result[0]["identity"][0]
            name = identity.split("\\")[-2]

            mark_attendance(name)

        else:
            name = "Unknown"

        st.markdown(f'<div class="name">{name}</div>',unsafe_allow_html=True)

        col1,col2,col3 = st.columns(3)

        col1.markdown(f'<div class="metric">Age<br>{age}</div>',unsafe_allow_html=True)
        col2.markdown(f'<div class="metric">Gender<br>{gender}</div>',unsafe_allow_html=True)
        col3.markdown(f'<div class="metric">Emotion<br>{emotion}</div>',unsafe_allow_html=True)


# ---------------------- LIVE CAMERA ----------------------
elif menu == "Live Camera":

    import time

    st.header("Live Face Recognition")

    if "camera_running" not in st.session_state:
        st.session_state.camera_running = False

    if "frame_count" not in st.session_state:
        st.session_state.frame_count = 0

    if "last_name" not in st.session_state:
        st.session_state.last_name = ""

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        if st.button("▶ Start Camera"):
            st.session_state.camera_running = True

    with col_btn2:
        if st.button("⏹ Stop Camera"):
            st.session_state.camera_running = False

    col1, col2 = st.columns([2,1])

    FRAME_WINDOW = col1.image([])
    info_panel = col2.empty()

    if st.session_state.camera_running:

        camera = cv2.VideoCapture(0)

        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        name = "Scanning..."
        age = ""
        gender = ""
        emotion = ""
        status = "Not Marked"

        while st.session_state.camera_running:

            ret, frame = camera.read()

            if not ret:
                break

            st.session_state.frame_count += 1

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray,1.3,5)

            # 🔥 Run AI every 30 frames (LESS LAG)
            if st.session_state.frame_count % 30 == 0:

                try:
                    # 🔥 Resize frame for faster processing
                    small_frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)

                    analysis = DeepFace.analyze(
                        small_frame,
                        actions=['age','gender','emotion'],
                        enforce_detection=False
                    )

                    age = analysis[0]['age']
                    gender = analysis[0]['dominant_gender']
                    emotion = analysis[0]['dominant_emotion']

                    recognition = DeepFace.find(
                        img_path=small_frame,
                        db_path="database",
                        enforce_detection=False
                    )

                    if len(recognition[0]) > 0:

                        identity = recognition[0]['identity'][0]
                        name = identity.split("\\")[-2]

                        if name != st.session_state.last_name:

                            mark_attendance(name)
                            status = "Marked"
                            st.session_state.last_name = name

                    else:
                        name = "Unknown"

                except:
                    name = "Unknown"

            for (x,y,w,h) in faces:

                if name == "Unknown":
                    color = (0,0,255)
                else:
                    color = (0,255,0)

                cv2.rectangle(frame,(x,y),(x+w,y+h),color,3)

                cv2.putText(
                    frame,
                    name,
                    (x,y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    color,
                    2
                )

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            FRAME_WINDOW.image(frame)

            info_panel.markdown(f"""
            ### 🧠 AI Detection Panel

            **Detected Person:** {name}

            **Age:** {age}

            **Gender:** {gender}

            **Emotion:** {emotion}

            **Attendance Status:** {status}
            """)

            # 🔥 Small delay to reduce CPU usage (IMPORTANT)
            time.sleep(0.03)

        camera.release()


# ---------------------- ATTENDANCE ----------------------
elif menu == "Attendance Log":

    st.header("Attendance Log")

    try:

        df = pd.read_csv("attendance.csv")

        # Search filter
        search = st.text_input("🔍 Search Person")

        if search:
            df = df[df["Name"].str.contains(search, case=False)]

        # Latest attendance on top
        df = df.sort_values(by=["Date","Time"], ascending=False)

        # Display table
        st.dataframe(df, use_container_width=True)

    except:

        st.warning("No attendance recorded yet")