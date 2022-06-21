import cv2
frame_before_resize = cv2.imread('E:/SelfDrivingCar/Server/selfDrivingCar/uploadedFiles/result.jpg')
frame_before_rotate = cv2.rotate(frame_before_resize,cv2.ROTATE_90_COUNTERCLOCKWISE)
frame = cv2.resize(frame_before_rotate, (1032, 581))
cv2.imshow('image',frame)
cv2.waitKey(0)
