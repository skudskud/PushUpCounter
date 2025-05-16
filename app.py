import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
import av
import cv2
import PoseModule as pm
import numpy as np # For np.interp
import math # For angle calculations if not fully covered by PoseModule

# RTCConfiguration for STUN/TURN servers
RTC_CONFIGURATION = RTCConfiguration({
    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
})

class VideoProcessor(VideoTransformerBase):
    def __init__(self):
        self.detector = pm.poseDetector()
        # Initialize variables for push-up logic directly in the processor
        # These will be reset for each new VideoProcessor instance (e.g., if the component re-mounts)
        # For persistent count across full app reloads/sessions, Streamlit session_state is better (see main())
        self.count = 0 
        self.direction = 0 # 0 for down, 1 for up
        self.form = 0 # 0 for incorrect, 1 for correct
        self.feedback = "Fix Form"

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        img = self.detector.findPose(img, draw=True)
        lmList = self.detector.findPosition(img, draw=False)

        if len(lmList) != 0:
            # Key landmarks for push-up
            # Left side: Shoulder 11, Elbow 13, Wrist 15, Hip 23
            # Right side: Shoulder 12, Elbow 14, Wrist 16, Hip 24
            # We'll use left side for this example, assuming user faces roughly sideways or camera can see left
            
            # Calculate angles (drawing them on the image is handled by findAngle)
            elbow_angle = self.detector.findAngle(img, 11, 13, 15) # Left Elbow
            shoulder_angle = self.detector.findAngle(img, 13, 11, 23) # Left Shoulder
            hip_angle = self.detector.findAngle(img, 11, 23, 25) # Left Hip (using 25 for knee to infer hip line)
            
            # Interpolate percentage for bar (elbow angle)
            # Assuming 90 degrees is down and 160 is up for full rep
            per = np.interp(elbow_angle, (90, 160), (100, 0)) # Inverted for bar: 100% when down, 0% when up
            bar = np.interp(elbow_angle, (90, 160), (380, 50)) # Bar position on screen

            # --- Push-up Logic Adapted --- 
            if elbow_angle > 160 and shoulder_angle > 40 and hip_angle > 160:
                self.form = 1 # Good starting form
            
            if self.form == 1:
                if per == 100: # Elbow bent (down position)
                    if elbow_angle <= 90 and hip_angle > 160: # Validate angles for down position
                        self.feedback = "Up"
                        if self.direction == 0:
                            self.count += 0.5
                            self.direction = 1 # Moving up now
                    else:
                        self.feedback = "Fix Form - Full Range"
                        # self.form = 0 # Optionally reset form if full range not met
                elif per == 0: # Elbow straight (up position)
                    if elbow_angle > 160 and shoulder_angle > 40 and hip_angle > 160:
                        self.feedback = "Down"
                        if self.direction == 1:
                            self.count += 0.5
                            self.direction = 0 # Moving down now
                    else:
                        self.feedback = "Fix Form - Full Extension"
                        # self.form = 0 # Optionally reset form if full extension not met
            else:
                self.feedback = "Fix Form - Starting Position"

            # --- UI Elements Drawn on Image --- 
            # Draw Bar
            if self.form == 1:
                cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
                cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

            # Push-up Counter
            cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(int(self.count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
            
            # Feedback Text
            cv2.rectangle(img, (110, 380), (550, 480), (255, 255, 255), cv2.FILLED) # Adjusted position
            cv2.putText(img, self.feedback, (115, 450), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

def main():
    st.title("💪 Push-Up Counter")
    st.write("Welcome to the real-time push-up tracker!")

    # Initialize session state variables if they don't exist
    if 'pushup_count' not in st.session_state:
        st.session_state.pushup_count = 0
    if 'feedback_message' not in st.session_state:
        st.session_state.feedback_message = "Fix Form"
    # Note: direction and form are more tightly coupled with VideoProcessor instance for now.
    # We can lift them to session_state if needed for more complex inter-component communication later.

    webrtc_ctx = webrtc_streamer(
        key="pushup-counter",
        video_transformer_factory=VideoProcessor, # This will create a new VideoProcessor instance
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

    # Display count and feedback from session state (updated by VideoProcessor)
    # This part is tricky because VideoProcessor runs in a separate thread/context with streamlit-webrtc.
    # Direct access to its self.count or self.feedback isn't straightforward for Streamlit UI update.
    # For now, the count and feedback are drawn ON the video frame by VideoProcessor.
    # To display them as separate Streamlit elements, we'd need a callback mechanism or use session_state more extensively.

    # Placeholder for Streamlit UI elements (if we move drawing out of VideoProcessor)
    # st.metric("Push-ups", st.session_state.pushup_count)
    # st.info(st.session_state.feedback_message)

if __name__ == "__main__":
    main() 