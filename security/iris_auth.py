import cv2
import numpy as np


# ============================================================
# 1. IRIS DETECTION
# ============================================================

def detect_iris(image):

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    gray = cv2.medianBlur(
        gray,
        5
    )

    circles = cv2.HoughCircles(

        gray,

        cv2.HOUGH_GRADIENT,

        dp=1,

        minDist=20,

        param1=50,

        param2=30,

        minRadius=10,

        maxRadius=100
    )

    if circles is None:
        return None

    circles = circles[0]

    return circles[0]


# ============================================================
# 2. GABOR FEATURE EXTRACTION
# ============================================================

def extract_gabor_features(
    iris_image
):

    features = []

    for theta in np.arange(
        0,
        np.pi,
        np.pi / 4
    ):

        kernel = cv2.getGaborKernel(

            (21, 21),

            sigma=4,

            theta=theta,

            lambd=10,

            gamma=0.5,

            psi=0,

            ktype=cv2.CV_32F
        )

        filtered = cv2.filter2D(
            iris_image,
            cv2.CV_8UC3,
            kernel
        )

        features.append(
            filtered
        )

    return features


# ============================================================
# 3. HAMMING DISTANCE
# ============================================================

def hamming_distance(
    template1,
    template2
):

    template1 = np.array(
        template1
    )

    template2 = np.array(
        template2
    )

    return np.mean(
        template1 != template2
    )