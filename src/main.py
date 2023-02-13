import cv2
import cv2.aruco as aruco
import numpy as np
from parametros import P0, P1, P2, P3

from video import VideoReader


def MyDetectMarkers(f: np.ndarray) -> np.ndarray:
    corner = []
    corners_, ids_, _ = arucoDetecter.detectMarkers(f)
    if ids_ is None:
        return np.array(corner, dtype="float32")

    ids_ = ids_.reshape(-1)
    if ids_[0] == 0:
        corner = corners_[0].reshape(-1, 2)
    return np.array(corner, dtype="float32")


def createM(ps: np.ndarray, xs: np.ndarray) -> np.ndarray:
    # if ps.shape != (-1, 3, 4) or xs.shape != (-1, 3):
    #     raise Exception
    l = np.shape[0] * 3
    M = np.zeros((l, 6))


v0, v1 = VideoReader("../data/videos/camera-00.mp4"), VideoReader("../data/videos/camera-01.mp4")
v2, v3 = VideoReader("../data/videos/camera-02.mp4"), VideoReader("../data/videos/camera-03.mp4")

dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
arucoDetecter = aruco.ArucoDetector(dictionary)

for f0, f1, f2, f3 in zip(v0, v1, v2, v3):
    # RETIRAR DEPOIS
    f0_ = cv2.resize(f0, (644, 364))
    f1_ = cv2.resize(f1, (644, 364))
    f2_ = cv2.resize(f2, (644, 364))
    f3_ = cv2.resize(f3, (644, 364))
    f01 = cv2.hconcat([f0_, f1_])
    f23 = cv2.hconcat([f2_, f3_])
    frame = cv2.vconcat([f01, f23])
    corners, ids, _ = arucoDetecter.detectMarkers(frame)
    frame = aruco.drawDetectedMarkers(frame, corners, ids)
    #######################################################

    corner0 = MyDetectMarkers(f0)
    corner1 = MyDetectMarkers(f1)
    corner2 = MyDetectMarkers(f2)
    corner3 = MyDetectMarkers(f3)

    print(f"corner0:\n {corner0}")
    print(f"corner1:\n {corner1}")
    print(f"corner2:\n {corner2}")
    print(f"corner3:\n {corner3}")
    print(f"###############################")

    cv2.imshow("Video", frame)
    if cv2.waitKey(5) == ord('q'):
        break

cv2.destroyAllWindows()
