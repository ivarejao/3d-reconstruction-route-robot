import cv2
import cv2.aruco as aruco
from video import VideoReader
from parametros import P0, P1, P2, P3

v0, v1 = VideoReader("../data/videos/camera-00.mp4"), VideoReader("../data/videos/camera-01.mp4")
v2, v3 = VideoReader("../data/videos/camera-02.mp4"), VideoReader("../data/videos/camera-03.mp4")

dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
arucoDetecter = aruco.ArucoDetector(dictionary)

for f0, f1, f2, f3 in zip(v0, v1, v2, v3):
    # RETIRAR DEPOIS
    f0 = cv2.resize(f0, (644, 364))
    f1 = cv2.resize(f1, (644, 364))
    f2 = cv2.resize(f2, (644, 364))
    f3 = cv2.resize(f3, (644, 364))
    f01 = cv2.hconcat([f0, f1])
    f23 = cv2.hconcat([f2, f3])
    frame = cv2.vconcat([f01, f23])
    corners, ids, _ = arucoDetecter.detectMarkers(frame)
    frame = aruco.drawDetectedMarkers(frame, corners, ids)
    #######################################################

    cv2.imshow("Video", frame)

    if cv2.waitKey(5) == ord('q'):
        break

cv2.destroyAllWindows()