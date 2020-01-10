import time
import multiprocessing as mp
import cv2

import time
import imutils

import gc

def image_put(q, user, pwd, ip):
    cap = cv2.VideoCapture("rtsp://%s:%s@%s" % (user, pwd, ip))
    preload = True
    while True:
            
        start = time.time()
        (grabbed, frame) = cap.read()
        read_cost = (time.time() - start) * 1000
        #if read_cost < 40:
        #    continue       

        """ 
        start = time.time() 
        q.put(frame)
        q.get() if q.qsize() > 1 else None
        put_cost = (time.time() - start) * 1000
        """
        start = time.time() 
        q.append(frame)
        if len(q) >= 50:
            del q[:]
            gc.collect()
        put_cost = (time.time() - start) * 1000

        print("read: {:.2f}ms, put: {:.2f}ms".format(read_cost, put_cost))


def image_get(q, window_name):
    cv2.namedWindow(window_name, flags=cv2.WINDOW_FREERATIO)
    while True:
        if len(q) != 0:
            start = time.time()
            frame = q.pop()
            #frame = q.get()
            get_cost = (time.time() - start) * 1000
            start = time.time()
            cv2.imshow(window_name, frame)
            cv2.waitKey(1)
            show_cost = (time.time() - start) * 1000
            
            start = time.time()
            for i in range(0):
                imutils.resize(frame, width=400)
            handle_cost = (time.time() - start) * 1000
            print("get: {:.2f}ms, show: {:.2f}ms, handle: {:.2f}ms".format(get_cost, show_cost, handle_cost))


def run_single_camera():
    user_name, user_pwd, camera_ip = "admin", "admin123", "10.10.30.126:554"

    #mp.set_start_method(method='spawn')  # init
    #queue = mp.Queue(maxsize=2)
    with mp.Manager() as manager:
        queue = manager.list()
        processes = [mp.Process(target=image_put, args=(queue, user_name, user_pwd, camera_ip)),
                     mp.Process(target=image_get, args=(queue, camera_ip))]

        [process.start() for process in processes]
        [process.join() for process in processes]


def run_multi_camera():
    user_name, user_pwd = "admin", "admin123"
    camera_ip_l = [
        "10.10.30.126:554",
#        "10.10.30.122:554",
        "10.10.30.123:554",
    ]

    #mp.set_start_method(method='spawn')  # init
    with mp.Manager() as manager:
        queues = [manager.list() for _ in camera_ip_l]

        processes = []
        for queue, camera_ip in zip(queues, camera_ip_l):
            processes.append(mp.Process(target=image_put, args=(queue, user_name, user_pwd, camera_ip)))
            processes.append(mp.Process(target=image_get, args=(queue, camera_ip)))

        for process in processes:
            process.daemon = True
            process.start()
        for process in processes:
            process.join()

def run():
    run_single_camera()  # quick, with 2 threads
    #run_multi_camera() # with 1 + n threads

if __name__ == '__main__':
    run()
