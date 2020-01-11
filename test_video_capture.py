# references: https://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/

# import the necessary packages
from imutils.video import WebcamVideoStream
import imutils
import cv2
import time
import datetime
import sys

import threading

from ffmpegvideostream import FFmpegVideoStream

THIRD_FLOOR_LEFT_CAMERA = 'rtsp://admin:admin@123@10.10.30.125:554'
THIRD_FLOOR_RIGHT_CAMERA = 'rtsp://admin:admin123@10.10.30.126:554'
NINTH_FLOOR_LEFT_CAMERA = 'rtsp://admin:admin123@10.10.30.122:554'
NINTH_FLOOR_RIGHT_CAMERA = 'rtsp://admin:admin123@10.10.30.123:554'
MYBDROOM_CAMERA = 'rtsp://192.168.0.34:8554/mybdroom'

IMAGE_PATH = '/home/guomao/data'

def save_image(image_path, prefix, image):
    image_file_name = image_path + '/' + prefix + '-' + datetime.datetime.now().strftime('%H-%M-%S-%f')[:-3] + '.png'
    cv2.imwrite(image_file_name, image)

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

def capture_with_threading(camera, display=True):
    vs = WebcamVideoStream(camera).start()
    if display:
        threading.Thread(target=display_video, args=(camera, vs)).start()
    frame_count = 0     
    while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        start = time.time()
        frame = vs.read()
        read_cost = (time.time() - start) * 1000
        frame_count += 1
        if frame_count >= 100 and frame_count < 200:
            save_image(IMAGE_PATH, 'cv2', frame)
        
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
def capture_with_threading_ffmpeg(camera, display=True, width=WIDTH, height=HEIGHT, rtsp_transport='tcp', in_frame_rate=25, out_frame_rate=25):
    vs = FFmpegVideoStream(camera, width, height, rtsp_transport, in_frame_rate, out_frame_rate).start()
    if display:
        threading.Thread(target=display_video, args=(camera, vs)).start()
    frame_count = 0     
    while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        start = time.time()
        frame = vs.read()
        read_cost = (time.time() - start) * 1000
        frame_count += 1
        if frame_count >= 100 and frame_count < 200:
            save_image(IMAGE_PATH, 'ffmpeg', frame)

        start = time.time()
        for i in range(30):
            imutils.resize(frame, width=400)
        handle_cost = (time.time() - start) * 1000
        #print("read: {:.2f}ms, handle: {:.2f}ms".format(read_cost, handle_cost))
     
    # do a bit of cleanup
    vs.stop()

def capture_with_threading_without_workload_ffmpeg(camera, width=WIDTH, height=HEIGHT):
    vs = FFmpegVideoStream(camera, width, height).start()
     
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
            capture_with_threading_ffmpeg(THIRD_FLOOR_LEFT_CAMERA, True)
        elif camera_id == 2:
            capture_with_threading_ffmpeg(THIRD_FLOOR_RIGHT_CAMERA, True)
        elif camera_id == 3:
            capture_with_threading_ffmpeg(NINTH_FLOOR_LEFT_CAMERA, True)
        elif camera_id == 4:
            capture_with_threading_ffmpeg(NINTH_FLOOR_RIGHT_CAMERA, True)
        elif camera_id == 5:
            capture_with_threading_ffmpeg(MYBDROOM_CAMERA, True, 720, 360, 'udp', 15, 15)
            

#capture_without_threading(THIRD_FLOOR_RIGHT_CAMERA)
#capture_without_threading_without_workload(THIRD_FLOOR_RIGHT_CAMERA)
#capture_with_threading(THIRD_FLOOR_LEFT_CAMERA)
#capture_with_threading(THIRD_FLOOR_RIGHT_CAMERA)
#capture_with_threading(NINTH_FLOOR_LEFT_CAMERA)
#capture_with_threading(NINTH_FLOOR_RIGHT_CAMERA)
#capture_with_threading_without_workload(THIRD_FLOOR_RIGHT_CAMERA)
