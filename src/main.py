import cv2
import cv2.aruco as aruco
import matplotlib.pyplot as plt
import numpy as np
from argparse import ArgumentParser

from parametros import P0, P1, P2, P3
from video import VideoReader
import os

def parse_args():
    """
    Faz a leitura dos argumentos
    """
    parser = ArgumentParser()
    parser.add_argument("--data-path", help="O caminho onde se encontra os vídeos", required=True)
    args = parser.parse_args()
    return args

def presentImage(centers, *args):
    f0, f1, f2, f3 = args
    if len(centers[0]) > 0:
        f0 = cv2.circle(f0, centers[0][0:2].astype(int), 10, (255, 0, 0), -1)
    if len(centers[1]) > 0:
        f1 = cv2.circle(f1, centers[1][0:2].astype(int), 10, (255, 0, 0), -1)
    if len(centers[2]) > 0:
        f2 = cv2.circle(f2, centers[2][0:2].astype(int), 10, (255, 0, 0), -1)
    if len(centers[3]) > 0:
        f3 = cv2.circle(f3, centers[3][0:2].astype(int), 10, (255, 0, 0), -1)

    f0_ = cv2.resize(f0, (644, 364))
    f1_ = cv2.resize(f1, (644, 364))
    f2_ = cv2.resize(f2, (644, 364))
    f3_ = cv2.resize(f3, (644, 364))
    f01 = cv2.hconcat([f0_, f1_])
    f23 = cv2.hconcat([f2_, f3_])
    frame = cv2.vconcat([f01, f23])

    cv2.imshow("Video", frame)
    if cv2.waitKey(5) == ord('q'):
        return False

    return True


def findCenterPixelAruco(f: np.ndarray, arucoDetecter) -> np.ndarray:
    corner = []
    corners, ids, _ = arucoDetecter.detectMarkers(f)
    if ids is None:
        return np.array(corner, dtype="float32")

    ids = ids.reshape(-1)
    if ids[0] == 0:
        corner = corners[0].reshape(-1, 2)
        xc = (corner[0][0] + corner[1][0] + corner[2][0] + corner[3][0]) / 4
        yc = (corner[0][1] + corner[1][1] + corner[2][1] + corner[3][1]) / 4
        corner = [xc, yc, 1]  # corner na verdade eh o centro
    return np.array(corner, dtype="float32")


def createM(ps: np.ndarray, xs: np.ndarray) -> np.ndarray:
    npontos = xs.shape[0]
    if npontos < 2:
        return np.array([], dtype="float32")

    l, c = npontos * 3, 4 + npontos
    M = np.zeros((l, c))

    for p, x, j in zip(ps, xs, range(0, npontos)):
        li, lo = 3 * j, 3 * j + 3
        ci, co = 4 + j, 4 + j + 1
        M[li:lo, 0:4] = p
        M[li:lo, ci:co] = -x.reshape(3, -1)
    return np.array(M, dtype="float32")


def main():
    args = parse_args()
    DATA_PATH = args.data_path

    v0, v1 = VideoReader(os.path.join(DATA_PATH, "camera-00.mp4")), VideoReader(os.path.join(DATA_PATH, "camera-01.mp4"))
    v2, v3 = VideoReader(os.path.join(DATA_PATH, "camera-02.mp4")), VideoReader(os.path.join(DATA_PATH, "camera-03.mp4"))

    cv2.namedWindow('Video', cv2.WINDOW_AUTOSIZE | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_NORMAL)

    dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    arucoDetecter = aruco.ArucoDetector(dictionary)
    pdict = [P0, P1, P2, P3]
    arucoPositions = []

    for f0, f1, f2, f3 in zip(v0, v1, v2, v3):
        centers = [findCenterPixelAruco(f0, arucoDetecter), findCenterPixelAruco(f1, arucoDetecter),
                   findCenterPixelAruco(f2, arucoDetecter), findCenterPixelAruco(f3, arucoDetecter)
                   ]

        if not presentImage(centers, f0, f1, f2, f3):
            break

        cs = []
        ps = []
        for i, center in enumerate(centers):
            if len(center) > 0:
                cs.append(center)
                ps.append(pdict[i])

        cs = np.array(cs, dtype="float32")
        ps = np.array(ps, dtype="float32")
        m = createM(ps, cs)
        u, s, vh = np.linalg.svd(m)
        x, y, z, w = np.array(vh[-1, 0:4]).T  # aruco position
        arucoPositions.append(np.array([x / w, y / w, z / w]))

    cv2.destroyAllWindows()

    arucoPositions = np.array(arucoPositions)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(arucoPositions[:, 0], arucoPositions[:, 1], arucoPositions[:, 2])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(-2.0, 2.0)
    ax.set_ylim(-1.0, 1.0)
    ax.set_zlim(0, 1.0)
    plt.show()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
