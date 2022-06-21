import cv2
import numpy as np
import logging
import math
import numpy as np
import requests

url = 'http://192.168.43.191:8000/PostDirection/'
frame_before_resize = cv2.imread('./selfDrivingCar/uploadedFiles/result.jpg')
frame_before_rotate = cv2.rotate(frame_before_resize,cv2.ROTATE_90_COUNTERCLOCKWISE)
frame = cv2.resize(frame_before_rotate, (1032, 581)) 
########### Detection Functions ###########


def detect_edges(frame):
    # filter for blue lane lines
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Green color
    # low_green = np.array([25, 52, 72])
    # high_green = np.array([102, 255, 255])
    # mask = cv2.inRange(hsv, low_green, high_green)
    # green = cv2.bitwise_and(frame, frame, mask=mask)

    lower_blue = np.array([60, 40, 40])
    upper_blue = np.array([150, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # detect edges
    edges = cv2.Canny(mask, 200, 400)

    return edges


def region_of_interest(edges):
    height, width = edges.shape
    mask = np.zeros_like(edges)

    # only focus bottom half of the screen
    polygon = np.array([[
        (0, height * 1 / 2),
        (width, height * 1 / 2),
        (width, height),
        (0, height),
    ]], np.int32)

    cv2.fillPoly(mask, polygon, 255)
    cropped_edges = cv2.bitwise_and(edges, mask)
    return cropped_edges


def detect_line_segments(cropped_edges):
    # tuning min_threshold, minLineLength, maxLineGap is a trial and error process by hand
    rho = 1  # distance precision in pixel, i.e. 1 pixel
    angle = np.pi / 180  # angular precision in radian, i.e. 1 degree
    min_threshold = 10  # minimal of votes
    line_segments = cv2.HoughLinesP(cropped_edges, rho, angle, min_threshold,
                                    np.array([]), minLineLength=80, maxLineGap=25)

    return line_segments


def average_slope_intercept(frame, line_segments):
    """
    This function combines line segments into one or two lane lines
    If all line slopes are < 0: then we only have detected left lane
    If all line slopes are > 0: then we only have detected right lane
    """
    lane_lines = []
    # lane_lines_final = [[],[]]
    if line_segments is None:
        logging.info('No line_segment segments detected')
        return lane_lines

    height, width, _ = frame.shape
    left_fit = []
    right_fit = []

    boundary = 1/3
    # left lane line segment should be on left 2/3 of the screen
    left_region_boundary = width * (1 - boundary)
    # right lane line segment should be on left 2/3 of the screen
    right_region_boundary = width * boundary

    for line_segment in line_segments:
        for x1, y1, x2, y2 in line_segment:
            if x1 == x2:
                logging.info(
                    'skipping vertical line segment (slope=inf): %s' % line_segment)
                continue
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]
            if slope < 0:
                if x1 < left_region_boundary and x2 < left_region_boundary:
                    left_fit.append((slope, intercept))
            else:
                if x1 > right_region_boundary and x2 > right_region_boundary:
                    right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    if len(left_fit) > 0:
        lane_lines.append(make_points(frame, left_fit_average))

    right_fit_average = np.average(right_fit, axis=0)
    if len(right_fit) > 0:
        lane_lines.append(make_points(frame, right_fit_average))

    # [[[316, 720, 484, 432]], [[1009, 720, 718, 432]]]
    logging.debug('lane lines: %s' % lane_lines)
    legnth = len(lane_lines)
    return lane_lines

def getSlope(lane_lines):
    slope2 = (lane_lines[1][0][3]-lane_lines[1][0][1]) / (lane_lines[1][0][2]-lane_lines[1][0][0])
    angle2=math.atan(slope2)
    slope1 = (lane_lines[0][0][3]-lane_lines[0][0][1]) / (lane_lines[0][0][2]-lane_lines[0][0][0])
    angle1=math.atan(slope1)
    angle1Deg = int(angle1 * 180.0 / math.pi) + 180
    angle2Deg = int(angle2 * 180.0 / math.pi) + 180
    print(angle2Deg,angle1Deg)
######### Displaying Functions ########


def display_lines(frame, lines, line_color=(0, 255, 0), line_width=2):
    line_image = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2),
                         line_color, line_width)
    line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    return line_image


def make_points(frame, line):
    height, width, _ = frame.shape
    slope, intercept = line
    y1 = height  # bottom of the frame
    y2 = int(y1 * 1 / 2)  # make points from middle of the frame down

    # bound the coordinates within the frame
    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    return [[x1, y1, x2, y2]]

def detect_lane(frame):
    logging.debug('detecting lane lines...')

    edges = detect_edges(frame)
    # cv2.imshow('edges', edges)

    cropped_edges = region_of_interest(edges)
    # cv2.imshow('edges cropped', cropped_edges)

    line_segments = detect_line_segments(cropped_edges)
    line_segment_image = display_lines(frame, line_segments)
    # cv2.imshow("line segments", line_segment_image)

    lane_lines = average_slope_intercept(frame, line_segments)
    lane_lines_image = display_lines(frame, lane_lines)
    # cv2.imshow("lane lines", lane_lines_image)
    cv2.waitKey(0) 
    
    return lane_lines, lane_lines_image
def getSlope(lane_lines):
    if len(lane_lines[0])==0:
        angle1Deg=0
        angle2Deg=0
        return(angle2Deg,angle1Deg)
    if len(lane_lines[0])<2:
        slope1 = (lane_lines[0][0][0][3]-lane_lines[0][0][0][1]) / (lane_lines[0][0][0][2]-lane_lines[0][0][0][0])
        angle1=math.atan(slope1)
        angle1Deg = int(angle1 * 180.0 / math.pi) + 180
        angle2Deg=0
        return(angle2Deg,angle1Deg)
    else:
        slope2 = (lane_lines[0][1][0][3]-lane_lines[0][1][0][1]) / (lane_lines[0][1][0][2]-lane_lines[0][1][0][0])
        angle2=math.atan(slope2)
        slope1 = (lane_lines[0][0][0][3]-lane_lines[0][0][0][1]) / (lane_lines[0][0][0][2]-lane_lines[0][0][0][0])
        angle1=math.atan(slope1)
        angle1Deg = int(angle1 * 180.0 / math.pi) + 180
        angle2Deg = int(angle2 * 180.0 / math.pi) + 180
        return(angle2Deg,angle1Deg)
lane_lines = detect_lane(frame)
def getDirection():
    lineRight,lineLeft=getSlope(lane_lines)
    if lineRight>180:
        lineRight=lineRight-180
    if lineLeft>180:
        lineLeft=lineLeft-180
    print(lineLeft,lineRight)
    if lineLeft==0 and lineRight==0:
       requests.post(url, data ={'direction':'s'} ) 
       print("s")
    if 60<=lineLeft<=130 and 60<=lineRight<=130:
       requests.post(url, data ={'direction':'f'} )
       print("f")
    elif 0<lineLeft<=60 or 0<lineRight<=60:
        requests.post(url, data ={'direction':'l'} )
        print("l")
    # elif 0<=lineLeft<=70 and 70<=lineRight<=110:
    #     print("L")
    elif 130<=lineLeft<=180 or 130<=lineRight<=180:
        requests.post(url, data ={'direction':'r'} )
        print("r")
    # elif 90<=lineLeft<=180 and 0<=lineRight<=70:
    #     print("R")
    else:
        print("out")
# getSlope(lane_lines)
# print(lane_lines)
getDirection()
# lane_lines_image = display_lines(frame, lane_lines)
# getSlope(lane_lines)