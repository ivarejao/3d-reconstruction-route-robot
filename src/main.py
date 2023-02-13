import cv2
import cv2.aruco as aruco
import numpy as np
from parametros import P0, P1, P2, P3

from video import VideoReader


def findCenterPixelAruco(f: np.ndarray) -> np.ndarray:
    corner_ = []
    corners_, ids_, _ = arucoDetecter.detectMarkers(f)
    if ids_ is None:
        return np.array(corner_, dtype="float32")

    ids_ = ids_.reshape(-1)
    if ids_[0] == 0:
        corner_ = corners_[0].reshape(-1, 2)
        xc = (corner_[0][0] + corner_[1][0] + corner_[2][0] + corner_[3][0]) / 4
        yc = (corner_[0][1] + corner_[1][1] + corner_[2][1] + corner_[3][1]) / 4
        corner_ = [xc, yc, 1]  # corner na verdade eh o centro
    return np.array(corner_, dtype="float32")


xp = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(xp[1:2, :])


def createM(ps_: np.ndarray, xs: np.ndarray) -> np.ndarray:
    npontos = xs.shape[0]
    if npontos < 2:
        return np.array([], dtype="float32")

    l, c = npontos * 3, 4 + npontos
    M = np.zeros((l, c))

    for p, x, j in zip(ps_, xs, range(0, npontos)):
        li, lo = 3*j, 3*j + 3
        ci, co = 4 + j, 4 + j + 1
        M[li:lo, 0:4] = p
        M[li:lo, ci:co] = -x.reshape(3, -1)
    return np.array([], dtype="float32")


v0, v1 = VideoReader("../data/videos/camera-00.mp4"), VideoReader("../data/videos/camera-01.mp4")
v2, v3 = VideoReader("../data/videos/camera-02.mp4"), VideoReader("../data/videos/camera-03.mp4")

dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
arucoDetecter = aruco.ArucoDetector(dictionary)
pdict = [P0, P1, P2, P3]

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

    centers = [findCenterPixelAruco(f0), findCenterPixelAruco(f1), findCenterPixelAruco(f2), findCenterPixelAruco(f3)]
    cs = []
    ps = []
    for i, center in enumerate(centers):
        if len(center) > 0:
            cs.append(center)
            ps.append(pdict[i])

    cs = np.array(cs, dtype="float32")
    ps = np.array(ps, dtype="float32")
    createM(ps, cs)

    cv2.imshow("Video", frame)
    if cv2.waitKey(5) == ord('q'):
        break

cv2.destroyAllWindows()
