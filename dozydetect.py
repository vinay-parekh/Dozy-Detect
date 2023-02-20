import cv2	# importing opencv for basic image processing functions 
import numpy as np	# for array related functions
import dlib # for deep learning based modules and face landmark detection
from imutils import face_utils	# face_utils for basic operations of conversion

cap = cv2.VideoCapture(0)	#initializing the camera and taking the instance

# initializing the face detector and landmark detector

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# status making for current state

sleep = 0
drowsy = 0
active = 0
status = " "
color = (0, 0, 0)

# the below function uses euclidean's formula to compute distance between two points
def compute(pointA, pointB):
	distance = np.linalg.norm(pointA - pointB)
	return(distance)

def blinked_eye(a, b, c, d, e, f):
	upper_distance = compute(b, d) + compute(c, e)
	lower_distance = compute(a, f)
	ratio = upper_distance / (2.0 * lower_distance)

	# checking if the eye is blinked
	if (ratio > 0.25):	# 0.25 is a standard ratio, which says that an eye is minimally open at this point and above 
		return 2
	elif (ratio > 0.21 and ratio < 0.25):
		return 1
	else:
		return 0

while True:
	_, image = cap.read()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	faces = detector(gray)

	# detected face in faces array

	for face in faces:
		x1 = face.left()
		y1 = face.top()
		x2 = face.right()
		y2 = face.bottom()

		face_frame = frame.copy()
		cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

		landmark = predictor(gray, face)
		landmark = face_utils.shape_to_np(landmark)

		# the numbers are actually landmarks which will show eye
		left_blink = blinked_eye(landmark[36], landmark[37], landmark[38], landmark[41], landmark[40], landmark[39])
		right_blink = blinked_eye(landmark[42], landmark[43], landmark[44], landmark[47], landmark[46], landmark[45])

		# display result for the eye blinks
		if ((left_blink == 0) or (right_blink == 0)):
			sleep += 1
			drowsy = 0
			active = 0
			if (sleep > 6):		# 6 is given to for stablizing state
				status = "SLEEPING!"
				color = (255, 0, 0)

		elif ((left_blink == 1) or (right_blink == 1)):
			sleep = 0
			active = 0
			drowsy += 1
			if (drowsy > 6):
				status = "DROWSY STATE!"
				color = (0, 0, 255)

		else:
			drowsy = 0
			sleep = 0
			active += 1
			if (active > 6):
				status = "ACTIVE STATE!"
				color = (0, 255, 0)

		cv2.putText(frame, status, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

		for n in range(0, 68):
			(x, y) = landmark[n]
			cv2. circle(face_frame, (x, y), 1, (255, 0, 0), -1)

	cv2.imshow("Frame", frame)
	cv2.imshow("Result of detector", face_frame)

	key = cv2.waitKey(1)
	if (key == 27):
		break

cap.release