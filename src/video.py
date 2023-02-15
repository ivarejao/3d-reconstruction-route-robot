# Code made in Pycharm by Igor Varejao
import cv2

class VideoReader():

    def __init__(self, path: str):
        self.video = cv2.VideoCapture(path)
        if (not self.video.isOpened()):
            raise FileNotFoundError(f"Error opening video : {path}")
        self.video_path = path
        width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.size = (height, width)
        self.fps = self.video.get(cv2.CAP_PROP_FPS)

    def __len__(self):
        return self.video.get(cv2.CAP_PROP_FRAME_COUNT)

    def __iter__(self):
        while self.video.isOpened():
            ret, frame = self.video.read()
            yield frame if ret else None

    def __getitem__(self, item: int):
        """
        Get the itemth frame from video
        """
        count = 0
        while self.video.isOpened():
            ret, frame = self.video.read()
            if count == item:
                if ret:
                    return frame
                else:
                    raise IndexError(f"Video index {item} is out bounding for {self.video_path}")
            count += 1

    def close(self):
        self.video.release()