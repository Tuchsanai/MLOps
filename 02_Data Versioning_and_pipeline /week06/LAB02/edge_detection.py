import cv2
import os

input_folder = "./img"
output_folder = "./processed_img"
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    img = cv2.imread(os.path.join(input_folder, filename), cv2.IMREAD_GRAYSCALE)
    edges = cv2.Canny(img, 100, 200)
    cv2.imwrite(os.path.join(output_folder, filename), edges)