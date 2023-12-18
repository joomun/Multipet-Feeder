import cv2
import threading
import numpy as np
import time
import serial

# Set up the serial connection to the Arduino
ser = serial.Serial('/dev/ttyUSB0', 19200)

# Load the Haar cascade for cat detection
cat_cascade = cv2.CascadeClassifier('/home/joomun/opencv/data/haarcascades/haarcascade_frontalcatface_extended.xml')


# Initialize the camera
camera = cv2.VideoCapture(0)

# Define a flag for indicating if a frame has been captured
frame_captured = False

# Define a lock for accessing the captured frame
lock = threading.Lock()

# Define a flag for indicating if the program should quit
quit_program = False

# Define a function to quit the program
def quit():
    global quit_program
    quit_program = True

if 0xFF == ord('q'):
    quit_program = True

def capture_frame():
    global frame_captured
    global lock
    
    while not quit_program:
        # Capture frame-by-frame
        ret, frame = camera.read()

        # Acquire the lock to access the captured frame
        lock.acquire()
        # Set the captured frame and release the lock
        frame_captured = frame
        lock.release()

def process_frame():
    global frame_captured
    global lock
    global quit_program
    last_detection_time = time.time() - 60 # Set last detection time to 2 hours ago

    while not quit_program:
        # Wait until a frame has been captured
        while not isinstance(frame_captured, np.ndarray):
            if quit_program:
                break

        if quit_program:
            break
        
        # Acquire the lock to access the captured frame
        lock.acquire()
        # Make a copy of the captured frame and release the lock
        frame = frame_captured.copy()
        frame_captured = False
        lock.release()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Get the current time
        current_time = time.time()

        # Only detect a cat if it's been at least 2 hours since the last detection
        if (current_time - last_detection_time) >= 2:
            # Detect cats in the frame
            cats = cat_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            # Draw a rectangle around each cat
            for (x, y, w, h) in cats:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                ser.write(b'cat') # Send a signal to pin 8 on the Arduino board to set it high
                print("Cat found")
                last_detection_time = current_time
        
        
        # Display the frame
        cv2.imshow("Cat Detection", frame)

        # Check if the 'q' key has been pressed
        if cv2.waitKey(60) & 0xFF == ord('q'):
            quit_program = True

    # Release the camera and close the window
    camera.release()
    cv2.destroyAllWindows()

# Create and start the threads
capture_thread = threading.Thread(target=capture_frame)
process_thread = threading.Thread(target=process_frame)
capture_thread.start()
process_thread.start()

# Wait for the threads to finish
capture_thread.join()
process_thread.join()

ser.close()

