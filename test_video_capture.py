# references: https://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/

# import the necessary packages
from imutils.video import WebcamVideoStream
import imutils
import cv2
import time
import sys

import threading

from ffmpegvideostream import FFmpegVideoStream

THIRD_FLOOR_LEFT_CAMERA = 'rtsp://admin:admin@123@10.10.30.125:554'
THIRD_FLOOR_RIGHT_CAMERA = 'rtsp://admin:admin123@10.10.30.126:554'
NINTH_FLOOR_LEFT_CAMERA = 'rtsp://admin:admin123@10.10.30.122:554'
NINTH_FLOOR_RIGHT_CAMERA = 'rtsp://admin:admin123@10.10.30.123:554'
 
def display_video(camera, vs):
    #cv2.namedWindow(camera, flags=cv2.WINDOW_FREERATIO)
    while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        start = time.time()
        frame = vs.read()
        read_cost = (time.time() - start) * 1000
        
        cv2.imshow(camera, frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    cv2.destroyAllWindows()

def capture_without_threading(camera):
    # grab a pointer to the video stream and initialize the FPS counter
    stream = cv2.VideoCapture(camera)
 
    while True:
        # grab the frame from the stream and resize it to have a maximum
        # width of 400 pixels
        start = time.time()
        (grabbed, frame) = stream.read()
        read_cost = (time.time() - start) * 1000
        
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

        start = time.time()
        for i in range(100):
            imutils.resize(frame, width=400)
        handle_cost = (time.time() - start) * 1000
        print("read: {:.2f}ms, handle: {:.2f}ms".format(read_cost, handle_cost))
     
     
    # do a bit of cleanup
    stream.release()
    cv2.destroyAllWindows()

def capture_without_threading_without_workload(camera):
    # grab a pointer to the video stream and initialize the FPS counter
    stream = cv2.VideoCapture(camera)
 
    while True:
        # grab the frame from the stream and resize it to have a maximum
        # width of 400 pixels
        start = time.time()
        #(grabbed, frame) = stream.read()
        grabbed = stream.grab()
        read_cost = (time.time() - start) * 1000
        (grabbed, frame) = stream.retrieve()
        print("read: {:.2f}ms".format(read_cost))
     
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
     
    # do a bit of cleanup
    stream.release()
    cv2.destroyAllWindows()

def capture_with_threading(camera):
    vs = WebcamVideoStream(camera).start()
    threading.Thread(target=display_video, args=(camera, vs)).start()     
    while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        start = time.time()
        frame = vs.read()
        read_cost = (time.time() - start) * 1000
        
        start = time.time()
        for i in range(100):
            imutils.resize(frame, width=400)
        handle_cost = (time.time() - start) * 1000
        print("read: {:.2f}ms, handle: {:.2f}ms".format(read_cost, handle_cost))
     
    # do a bit of cleanup
    vs.stop()

def capture_with_threading_without_workload(camera):
    vs = WebcamVideoStream(camera).start()
     
    while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        start = time.time()
        frame = vs.read()
        read_cost = (time.time() - start) * 1000
        print("read: {:.2f}ms".format(read_cost))
     
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
     
    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()

WIDTH = 1920
HEIGHT = 1080
def capture_with_threading_ffmpeg(camera, display=True):
    vs = FFmpegVideoStream(camera, WIDTH, HEIGHT).start()
    if display:
        threading.Thread(target=display_video, args=(camera, vs)).start()     
    while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        start = time.time()
        frame = vs.read()
        read_cost = (time.time() - start) * 1000
        
        start = time.time()
        for i in range(100):
            imutils.resize(frame, width=400)
        handle_cost = (time.time() - start) * 1000
        print("read: {:.2f}ms, handle: {:.2f}ms".format(read_cost, handle_cost))
     
    # do a bit of cleanup
    vs.stop()

def capture_with_threading_without_workload_ffmpeg(camera):
    vs = FFmpegVideoStream(camera, WIDTH, HEIGHT).start()
     
    while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        start = time.time()
        frame = vs.read()
        read_cost = (time.time() - start) * 1000
        print("read: {:.2f}ms".format(read_cost))
     
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
     
    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        camera_id = int(sys.argv[1])
        if camera_id == 1:
            capture_with_threading_ffmpeg(THIRD_FLOOR_LEFT_CAMERA, False)
        elif camera_id == 2:
            capture_with_threading_ffmpeg(THIRD_FLOOR_RIGHT_CAMERA)
        elif camera_id == 3:
            capture_with_threading_ffmpeg(NINTH_FLOOR_LEFT_CAMERA, False)
        else:
            capture_with_threading_ffmpeg(NINTH_FLOOR_RIGHT_CAMERA, False)
            

#capture_without_threading(THIRD_FLOOR_RIGHT_CAMERA)
#capture_without_threading_without_workload(THIRD_FLOOR_RIGHT_CAMERA)
#capture_with_threading(THIRD_FLOOR_LEFT_CAMERA)
#capture_with_threading(THIRD_FLOOR_RIGHT_CAMERA)
#capture_with_threading(NINTH_FLOOR_LEFT_CAMERA)
#capture_with_threading(NINTH_FLOOR_RIGHT_CAMERA)
#capture_with_threading_without_workload(THIRD_FLOOR_RIGHT_CAMERA)
