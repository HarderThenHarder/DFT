import cv2
import numpy as np
import tkinter.filedialog as filedialog
import tkinter as tk
import sys
import math

root = tk.Tk()
root.withdraw()

file_name = filedialog.askopenfilename()
if file_name is '':
    sys.exit(0)

im = cv2.imread(file_name, 0)
h, w = im.shape

cv2.namedWindow("Result & Magnitude")
cv2.createTrackbar("start_pos", "Result & Magnitude", 0, int(min(w, h) / 2), lambda x: None)
cv2.createTrackbar("end_pos", "Result & Magnitude", int(min(w, h) / 4), int(min(w, h) / 2), lambda x: None)


def select_circle_range(r, value, mask, center):
    for row in range(mask.shape[0]):
        for column in range(mask.shape[1]):
            if math.sqrt((row - center[0]) ** 2 + (column - center[1]) ** 2) < r:
                mask[row][column] = value
    return mask

while True:
    dft = cv2.dft(np.float32(im), flags=cv2.DFT_COMPLEX_OUTPUT)

    dft_shift=np.fft.fftshift(dft)
    magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))

    rows,cols = im.shape

    start_pos = cv2.getTrackbarPos("start_pos", "Result & Magnitude")
    end_pos = cv2.getTrackbarPos("end_pos", "Result & Magnitude",)

    if start_pos > end_pos:
        start_pos = end_pos

    center = (int(rows / 2), int(cols / 2))

    mask = np.zeros((rows, cols, 2), np.uint8)
    mask[center[0] - end_pos : center[0] + end_pos, center[1] - end_pos : center[1] + end_pos] = 1
    mask[center[0] - start_pos : center[0] + start_pos, center[1] - start_pos : center[1] + start_pos] = 0
    # mask = select_circle_range(end_pos, 1, mask, center)
    # mask = select_circle_range(start_pos, 0, mask, center)

    fshift = dft_shift * mask
    f_ishift = np.fft.ifftshift(fshift)

    mask = np.zeros((rows, cols), np.uint8)
    mask[center[0] - end_pos : center[0] + end_pos, center[1] - end_pos : center[1] + end_pos] = 1
    mask[center[0] - start_pos : center[0] + start_pos, center[1] - start_pos : center[1] + start_pos] = 0
    # mask = select_circle_range(end_pos, 1, mask, center)
    # mask = select_circle_range(start_pos, 0, mask, center)
    magnitude_spectrum = magnitude_spectrum * mask
    magnitude_spectrum_for_visualize = cv2.normalize(magnitude_spectrum, None, 0, 1, cv2.NORM_MINMAX)

    img_back = cv2.idft(f_ishift)
    img_back = cv2.magnitude(img_back[:,:,0],img_back[:,:,1])

    img_back_for_visualize = cv2.normalize(img_back, None, 0, 1, cv2.NORM_MINMAX)

    cv2.imshow("Result & Magnitude", np.hstack((img_back_for_visualize, magnitude_spectrum_for_visualize)))
    if cv2.waitKey(1) == ord('q'):
        break
    elif cv2.getWindowProperty("Result & Magnitude", cv2.WND_PROP_AUTOSIZE) < 1:
        break