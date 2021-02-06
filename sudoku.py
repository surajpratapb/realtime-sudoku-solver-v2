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
box = 28 + 2 * margin
grid_size = 9 * box


# saving video output
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
flag = 0
out = cv2.VideoWriter('solution_output.avi', fourcc, 30.0, (1080, 620))


while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    # Changing the color picture to gray
    gray = cv2.GaussianBlur(gray, (7, 7), 0)            # applying GaussianBlur
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 9, 2)       # inverting color scale

# finding contours from the picture

    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    # removing redundant pixels
    contour_grid = None
    maxArea = 0

    for c in contours:
        area = cv2.contourArea(c)           # returns the number of nonzero pixels
        if area > 25000:
            peri = cv2.arcLength(c, True)
            polygon = cv2.approxPolyDP(c, 0.01 * peri, True)
            if area > maxArea and len(polygon) == 4:
                contour_grid = polygon
                maxArea = area

# processing for image transform
    if contour_grid is not None:
        cv2.drawContours(frame, [contour_grid], 0, (0, 255, 0), 2)
        points = np.vstack(contour_grid).squeeze()
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
        grid = cv2.warpPerspective(frame, M, (grid_size, grid_size))
        grid = cv2.cvtColor(grid, cv2.COLOR_BGR2GRAY)
        grid = cv2.adaptiveThreshold(
            grid, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 7, 3)
        result = " "
        cv2.imshow("grid", grid)            # shows output screen
        if flag == 0:

            grid_txt = []
            for y in range(9):
                line = ""
                for x in range(9):
                    y2min = y * box + margin
                    y2max = (y + 1) * box - margin
                    x2min = x * box + margin
                    x2max = (x + 1) * box - margin
                    cv2.imwrite("mat" + str(y) + str(x) + ".png",
                                grid[y2min:y2max, x2min:x2max])
                    img = grid[y2min:y2max, x2min:x2max]
                    x = img.reshape(1, 28, 28, 1)
                    if x.sum() > 10000:
                        prediction = classifier.predict_classes(x)
                        line += "{:d}".format(prediction[0])
                    else:
                        line += "{:d}".format(0)
                grid_txt.append(line)
            print(grid_txt)

            # passing the predicted sudoku vales to the sudoku solver function
            result = sol.sudoku(grid_txt)
        print("Results:", result)

        if result is not None:
            flag = 1

            # creating a array of 9x9 and filling it with zeros
            background = np.zeros(
                shape=(grid_size, grid_size, 3), dtype=np.float32)
            for y in range(len(result)):
                for x in range(len(result[y])):
                    if grid_txt[y][x] == "0":
                        cv2.putText(background, "{:d}".format(result[y][x]),((
                                        x ) * box + margin + 3, (y + 1) * box - margin - 3),cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 0.9, (0, 0, 255), 1)

            # rendering the output over the sudoku
            M = cv2.getPerspectiveTransform(pts2, pts1)
            h, w, c = frame.shape
            backgroundP = cv2.warpPerspective(background, M, (w, h))
            img2gray = cv2.cvtColor(backgroundP, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
            mask = mask.astype('uint8')
            mask_inv = cv2.bitwise_not(mask)
            img1_bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
            img2_fg = cv2.bitwise_and(backgroundP, backgroundP, mask=mask).astype('uint8')
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
