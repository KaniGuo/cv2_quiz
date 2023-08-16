"""Write a Python script that reads an image from a file as grayscale,
and finds the four non-overlapping 5x5 patches with highest average
brightness. Take the patch centers as corners of a quadrilateral,
calculate its area in pixels, and draw the quadrilateral in red into
the image and save it in PNG format. Use the opencv-python package for
image handling. Write test cases.
It should be possible to run the script from the __main__ section or
from command line."""


import cv2
import numpy as np
import os

def highest_brightness(image, num = 4, size = 5):
    # calculate with gray value
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = gray_image.shape
    # calculate the coordinate of the center of every 5*5 patches and save them in patch_list
    patch_list = []
    for n in range(num):
        print(f"Finding patch {n+1}...")
        patch_max = 0
        for i in range(size//2, width - size//2):
            for j in range (size//2, height - size//2):
                patch = gray_image[i-size//2:i+size//2+1, j-size//2:j+size//2+1]
                patch_avg = np.mean(patch)

                if patch_avg > patch_max:
                    patch_max = patch_avg
                    patch_coor = (i,j)
        patch_list.append(patch_coor)
        # set the gray value of selected patches as 0 to avoid overlapping 
        i,j = patch_coor
        gray_image[i-size//2:i+size//2+1, j-size//2:j+size//2+1] = 0
    print("The center of highest brightness patch:", patch_list)
    points = np.array(patch_list)
    center = np.mean(points, axis=0)
    # Arrange the points in clockwise order to draw a convex polygon
    sorted_points = sorted(points, key=lambda point: np.arctan2(point[1] - center[1], point[0] - center[0]))
    return sorted_points
        

def quadrilateral_area(sorted_points):
    area = cv2.contourArea(np.array(sorted_points, dtype=np.int32))
    print("Area of quadrilateral:", abs(area))
    return area

def draw_quadrilateral(image, sorted_points, output_path = "image with quadrilateral.png"):
    # cv2.fillConvexPoly(image, np.array(sorted_points), color=(0,0,255))
    cv2.polylines(image, [np.array(sorted_points)], color=(0,0,255), isClosed=True, thickness=2)
    cv2.imshow("Image with quadrilateral:",image)
    cv2.waitKey(0)
    cv2.imwrite(output_path, image)
    print("Save \"image with quadrilateral.png\" successfully!")

def make_image():
    width, height = 400, 400  # 图像的宽度和高度
    black_image = np.zeros((height, width, 3), dtype=np.uint8)  # 创建一个黑色图像

    # 设置四个白色像素点的坐标
    white_pixels = [(100, 100), (200, 100), (100, 200), (200, 200)]

    # 在图像上绘制四个白色像素点
    for pixel in white_pixels:
        black_image[pixel[1], pixel[0]] = [255, 255, 255]  # 设置像素为白色

    # 显示图像
    # cv2.imshow('Image', black_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return black_image


def main(path):
    # import image
    image = cv2.imread(path)
    sorted_points = highest_brightness(image)
    quadrilateral_area(sorted_points)
    draw_quadrilateral(image, sorted_points)

if __name__ == "__main__":
    input_path = input("please input the path of image:")
    if os.path.exists(input_path) and os.path.isfile(input_path):
        main(input_path)
    else:
        print("No image!")
    
