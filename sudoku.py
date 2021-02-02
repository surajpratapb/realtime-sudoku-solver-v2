import cv2
import numpy as np
import operator
from keras.models import load_model
from keras.models import model_from_json
import sudoku_solver as sol

# importing digit recognition model
classifier = load_model("./digit_model.h5")

# setting margin and grid size
margin = 4
case = 28 + 2 * margin
grid_size = 9 * case

# saving video output
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
flag = 0
out = cv2.VideoWriter('output.avi', fourcc, 30.0, (1080, 620))

# Changing the color picture to gray
# applying GaussianBlur
# inverting color scale
while True:

    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 9, 2)

    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)     # removing redundant pixels
    contour_grid_s = None
    maxArea = 0

    for c in contours:
        area = cv2.contourArea(c)           # returns the number of nonzero pixels
        if area > 25000:
            peri = cv2.arcLength(c, True)
            polygon = cv2.approxPolyDP(c, 0.01 * peri, True)
            if area > maxArea and len(polygon) == 4:
                contour_grid_s = polygon
                maxArea = area
    # processing for image transform
    if contour_grid_s is not None:
        cv2.drawContours(frame, [contour_grid_s], 0, (0, 255, 0), 2)
        points = np.vstack(contour_grid_s).squeeze()
        points = sorted(points, key=operator.itemgetter(1))
        if points[0][0] < points[1][0]:
            if points[3][0] < points[2][0]:
                pts1 = np.float32([points[0], points[1], points[3], points[2]])
            else:
                pts1 = np.float32([points[0], points[1], points[2], points[3]])
        else:
            if points[3][0] < points[2][0]:
                pts1 = np.float32([points[1], points[0], points[3], points[2]])
            else:
                pts1 = np.float32([points[1], points[0], points[2], points[3]])
        pts2 = np.float32([[0, 0], [grid_size, 0], [0, grid_size], [
                          grid_size, grid_size]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        grid_s = cv2.warpPerspective(frame, M, (grid_size, grid_size))
        grid_s = cv2.cvtColor(grid_s, cv2.COLOR_BGR2GRAY)
        grid_s = cv2.adaptiveThreshold(
            grid_s, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 7, 3)

        cv2.imshow("grid_s", grid_s)    # shows output screen
        if flag == 0:

            grid_s_txt = []
            for y in range(9):
                ligne = ""
                for x in range(9):
                    y2min = y * case + margin
                    y2max = (y + 1) * case - margin
                    x2min = x * case + margin
                    x2max = (x + 1) * case - margin
                    cv2.imwrite("mat" + str(y) + str(x) + ".png",
                                grid_s[y2min:y2max, x2min:x2max]) # writes the sudoku boxes into folder
                    img = grid_s[y2min:y2max, x2min:x2max]
                    x = img.reshape(1, 28, 28, 1)
                    if x.sum() > 10000:
                        prediction = classifier.predict_classes(x)
                        ligne += "{:d}".format(prediction[0])  # running digit recognition model on the pictures
                    else:
                        ligne += "{:d}".format(0)
                grid_s_txt.append(ligne)
            print(grid_s_txt)

            # passing the predicted sudoku vales to the sudoku solver function
            result = sol.sudoku(grid_s_txt)
        print("Result:", result)

        if result is not None:
            flag = 1
            bckgrnd = np.zeros(
                shape=(grid_size, grid_size, 3), dtype=np.float32)
            for y in range(len(result)):
                for x in range(len(result[y])):
                    if grid_s_txt[y][x] == "0":
                        cv2.putText(bckgrnd, "{:d}".format(result[y][x]), ((
                            x) * case + margin + 3, (y + 1) * case - margin - 3), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 0.9, (0, 0, 255), 1)

            # rendering the output over the sudoku
            M = cv2.getPerspectiveTransform(pts2, pts1)
            h, w, c = frame.shape
            bckgrndP = cv2.warpPerspective(bckgrnd, M, (w, h))
            img2gray = cv2.cvtColor(bckgrndP, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
            mask = mask.astype('uint8')
            mask_inv = cv2.bitwise_not(mask)
            img1_bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
            img2_fg = cv2.bitwise_and(bckgrndP, bckgrndP, mask=mask).astype('uint8')
            dst = cv2.add(img1_bg, img2_fg)
            dst = cv2.resize(dst, (1080, 620))
            cv2.imshow("frame", dst)
            out.write(dst)

        else:
            frame = cv2.resize(frame, (1080, 620))
            cv2.imshow("frame", frame)
            out.write(frame)

    else:
        flag = 0
        frame = cv2.resize(frame, (1080, 620))
        cv2.imshow("frame", frame)
        out.write(frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break


out.release()
cap.release()
cv2.destroyAllWindows()
