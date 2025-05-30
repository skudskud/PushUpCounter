# import cv2
# import numpy as np
# import PoseModule as pm

# def setup_camera(file_path=None):
#     """Initializes the video capture object."""
#     # If a file_path is provided, open the file. Otherwise, open the default camera.
#     if file_path is not None:
#         return cv2.VideoCapture(file_path)
#     else:
#         return cv2.VideoCapture(0)


# def update_feedback_and_count(elbow, shoulder, hip, direction, count, form):
#     """Determines the feedback message and updates the count based on the angles."""
#     feedback = "Fix Form"
#     if elbow > 160 and shoulder > 40 and hip > 160:
#         form = 1
#     if form == 1:
#         if elbow <= 90 and hip > 160:
#             feedback = "Up"
#             if direction == 0:
#                 count += 0.5
#                 direction = 1
#         elif elbow > 160 and shoulder > 40 and hip > 160:
#             feedback = "Down"
#             if direction == 1:
#                 count += 0.5
#                 direction = 0
#         else:
#             feedback = "Fix Form"
#     return feedback, count, direction, form

# def draw_ui(img, per, bar, count, feedback, form):
#     """Draws the UI elements on the image."""
#     if form == 1:
#         cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
#         cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
#         cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

#     cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
#     cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
    
#     cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
#     cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

# # Update your main function to include the path to your MP4 file
# def main():
#     # Provide the path to your MP4 file here
#     mp4_file_path = '/Users/aryanvij/Downloads/The Perfect Push Up _ Do it right!.mp4'
#     cap = setup_camera(mp4_file_path)
#     detector = pm.poseDetector()
#     count = 0
#     direction = 0
#     form = 0

#     while cap.isOpened():
#         ret, img = cap.read()
#         if not ret:
#             break  # If no frames are returned, stop the loop
#         img = detector.findPose(img, False)
#         lmList = detector.findPosition(img, False)

#         if len(lmList) != 0:
#             elbow = detector.findAngle(img, 11, 13, 15)
#             shoulder = detector.findAngle(img, 13, 11, 23)
#             hip = detector.findAngle(img, 11, 23, 25)
#             per = np.interp(elbow, (90, 160), (0, 100))
#             bar = np.interp(elbow, (90, 160), (380, 50))
#             feedback, count, direction, form = update_feedback_and_count(elbow, shoulder, hip, direction, count, form)
#             draw_ui(img, per, bar, count, feedback, form)
#             print(count)
        
#         cv2.imshow('Pushup Counter', img)
#         if cv2.waitKey(10) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()





import cv2
import numpy as np
import PoseModule as pm

def setup_camera():
    """Initializes the video capture object."""
    return cv2.VideoCapture(0)

def get_video_dimensions(cap):
    """Returns the dimensions of the video frame."""
    width = cap.get(3)  # float `width`
    height = cap.get(4)  # float `height`
    return width, height

def update_feedback_and_count(elbow, shoulder, hip, direction, count, form):
    """Determines the feedback message and updates the count based on the angles."""
    feedback = "Fix Form"
    if elbow > 160 and shoulder > 40 and hip > 160:
        form = 1
    if form == 1:
        if elbow <= 90 and hip > 160:
            feedback = "Up"
            if direction == 0:
                count += 0.5
                direction = 1
        elif elbow > 160 and shoulder > 40 and hip > 160:
            feedback = "Down"
            if direction == 1:
                count += 0.5
                direction = 0
        else:
            feedback = "Fix Form"
    return feedback, count, direction, form

def draw_ui(img, per, bar, count, feedback, form):
    """Draws the UI elements on the image."""
    if form == 1:
        cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
        cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
    
    cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
    cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

def main():
    cap = setup_camera()
    detector = pm.poseDetector()
    count = 0
    direction = 0
    form = 0

    while cap.isOpened():
        ret, img = cap.read()
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)

        if len(lmList) != 0:
            elbow = detector.findAngle(img, 11, 13, 15)
            shoulder = detector.findAngle(img, 13, 11, 23)
            hip = detector.findAngle(img, 11, 23, 25)
            per = np.interp(elbow, (90, 160), (0, 100))
            bar = np.interp(elbow, (90, 160), (380, 50))
            feedback, count, direction, form = update_feedback_and_count(elbow, shoulder, hip, direction, count, form)
            draw_ui(img, per, bar, count, feedback, form)
            print(count)
        
        cv2.imshow('Pushup Counter', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm



cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
direction = 0
form = 0
feedback = "Fix Form"


while cap.isOpened():
    ret, img = cap.read() #640 x 480
    #Determine dimensions of video - Help with creation of box in Line 43
    width  = cap.get(3)  # float `width`
    height = cap.get(4)  # float `height`
    # print(width, height)
    
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) != 0:
        elbow = detector.findAngle(img, 11, 13, 15)
        shoulder = detector.findAngle(img, 13, 11, 23)
        hip = detector.findAngle(img, 11, 23,25)
        
        #Percentage of success of pushup
        per = np.interp(elbow, (90, 160), (0, 100))
        
        #Bar to show Pushup progress
        bar = np.interp(elbow, (90, 160), (380, 50))

        #Check to ensure right form before starting the program
        if elbow > 160 and shoulder > 40 and hip > 160:
            form = 1
    
        #Check for full range of motion for the pushup
        if form == 1:
            if per == 0:
                if elbow <= 90 and hip > 160:
                    feedback = "Up"
                    if direction == 0:
                        count += 0.5
                        direction = 1
                else:
                    feedback = "Fix Form"
                    
            if per == 100:
                if elbow > 160 and shoulder > 40 and hip > 160:
                    feedback = "Down"
                    if direction == 1:
                        count += 0.5
                        direction = 0
                else:
                    feedback = "Fix Form"
                        # form = 0
                
                    
    
        print(count)
        
        #Draw Bar
        if form == 1:
            cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
            cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                        (255, 0, 0), 2)


        #Pushup counter
        cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 5)
        
        #Feedback 
        cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, feedback, (500, 40 ), cv2.FONT_HERSHEY_PLAIN, 2,
                    (0, 255, 0), 2)

        
    cv2.imshow('Pushup counter', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()