# Code made in Pycharm by Igor Varejao
import cv2


class VideoReader():

    def __init__(self, path: str):
        self.video = cv2.VideoCapture(path)
        self.video_path = path
        if not self.video.isOpened():
            raise FileNotFoundError(f"Error opening video : {path}")

    def __iter__(self):
        while self.video.isOpened():
            ret, frame = self.video.read()
            if ret:
                yield frame
            else:
                break


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
