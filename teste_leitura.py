import cv2
import numpy as np
from scipy.spatial import distance
from scipy.optimize import linear_sum_assignment
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.stats import norm
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
from glob import glob

# Define bubble size and space
bubble_size = 30
bubble_space = 5

arquivos = glob(r'OMR-Scanner-7/test/*.jpg')
# Load the scanned multiple choice bubble sheet image
img = cv2.imread('OMR-Scanner-7/test/501-24-_jpg.rf.a4b3e2c0bbeff6c7bfd0d7ffb0fa1a16.jpg')

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply binary threshold
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

# Detect contours
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Initialize lists for circles and squares
circles = []
squares = []

# Iterate over the contours and check for circle or square shapes
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    
    if (h > w * 1.2 and h > w * 0.8):
        if (w > bubble_size and h > bubble_size):
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            squares.append([x, y, w, h])
        elif (w < bubble_size and h < bubble_size):
            cv2.circle(img, (x + w // 2, y + h // 2), min(w, h) // 2, (0, 0, 255), 2)
            circles.append([x, y, w, h])

# Detect multiple choice options by detecting lines in the bubble sheet
lines = cv2.HoughLines(thresh, 1, np.pi / 180, 100, 0, 0)

# Define the list of bubble coordinates
bubble_coordinates = []

# Iterate over the lines and draw them on the image
for rho, theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))

    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # For each line, iterate over the circles and check if the circle center is near the line
    for center in circles:
        cx, cy, _, _ = center
        dis = abs(cx * a + cy * b - rho) / np.sqrt(a * a + b * b)
        
        if dis < bubble_size / 2:
            cv2.circle(img, (cx, cy), int(bubble_size / 2), (255, 0, 0), 2)
            bubble_coordinates.append([cx, cy])

# Save the detected circles and lines image
cv2.imwrite('detected_circles_and_lines.jpg', img)

# Sort the detected bubble coordinates based on the vertical distance from the top of the bubble sheet
sorted_bubble_coordinates = sorted(bubble_coordinates, key=lambda x: x[1])

# Initialize a dictionary to store the sorted multiple choice options
sorted_multiple_choice_options = {}

# Define the vertical space between bubbles
vertical_space = bubble_size + bubble_space

# Iterate over the sorted bubble coordinates and group them into multiple choice options based on their vertical position
for i, bubble in enumerate(sorted_bubble_coordinates):
    row = i // 5
    column = i % 5
    key = f'option_{row + 1}'
    
    if key not in sorted_multiple_choice_options:
        sorted_multiple_choice_options[key] = []
    
    sorted_multiple_choice_options[key].append(bubble)

# Display the detected multiple choice options
print(sorted_multiple_choice_options)

# Load the image of the multiple choice options answer key
answer_key_img = cv2.imread('OMR-Scanner-7/test/501-24-_jpg.rf.a4b3e2c0bbeff6c7bfd0d7ffb0fa1a16.jpg')

# Convert the image to grayscale
answer_key_gray = cv2.cvtColor(answer_key_img, cv2.COLOR_BGR2GRAY)

# Apply binary threshold
_, answer_key_thresh = cv2.threshold(answer_key_gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

# Detect contours in the answer key image
answer_key_contours, _ = cv2.findContours(answer_key_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Define the list of answer key bubble coordinates
answer_key_bubble_coordinates = []

# Iterate over the answer key contours and check for circle shapes
for cnt in answer_key_contours:
    x, y, w, h = cv2.boundingRect(cnt)
    
    if (w > bubble_size and h > bubble_size):
        cv2.rectangle(answer_key_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        answer_key_bubble_coordinates.append([x, y, w, h])

# Save the detected answer key circles image
cv2.imwrite('detected_answer_key_circles.jpg', answer_key_img)

# Compare the detected bubble coordinates with the answer key bubble coordinates and determine the correct answers
correct_answers = {}

for key, coordinates in sorted_multiple_choice_options.items():
    correct_answer = None
    
    for bubble in coordinates:
        cx, cy = bubble
        
        for bubble_key, bubble_coordinates in enumerate(answer_key_bubble_coordinates):
            x, y, w, h = bubble_coordinates
            
            if cx > x and cx < x + w and cy > y and cy < y + h:
                correct_answer = bubble_key + 1
                break
        
        if correct_answer is not None:
            correct_answers[key] = correct_answer
            break

# Display the correct answers
print(correct_answers)