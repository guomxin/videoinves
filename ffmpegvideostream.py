from threading import Thread
import ffmpeg
import numpy as np

class FFmpegVideoStream:
    def __init__(self, src, width, height, name="FFmpegVideoStream"):
        # get the first frame from stream 
        self.frame = None
        self.width = width
        self.height = height
        self.process = (
            ffmpeg
             .input(src)
             .output('-', format='rawvideo', pix_fmt='rgb24')
             .run_async(pipe_stdout=True)
        )
        packet = self.process.stdout.read(self.height * self.width * 3)
        self.frame = (
            np
            .frombuffer(packet, np.uint8)
            .reshape([self.height, self.width, 3])
        )

        # initialize the thread name
        self.name = name
        
        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        while self.process.poll() is None:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return
    
            # otherwise, read the next frame from the stream
            try:
                packet = self.process.stdout.read(self.height * self.width * 3)
                self.frame = (
                    np
                    .frombuffer(packet, np.uint8)
                    .reshape([self.height, self.width, 3])
                )
            except:
                self.frame = None

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
