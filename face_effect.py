import cv2
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# For static images:
IMAGE_FILES = []
with mp_face_detection.FaceDetection(
    model_selection=1, min_detection_confidence=0.5) as face_detection:
  for idx, file in enumerate(IMAGE_FILES):
    image = cv2.imread(file)
    # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
    results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Draw face detections of each face.
    if not results.detections:
      continue
    annotated_image = image.copy()
    for detection in results.detections:
      print('Nose tip:')
      print(mp_face_detection.get_key_point(
          detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))
      mp_drawing.draw_detection(annotated_image, detection)
    cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)

# For webcam input:

# my things
billie = 0
cap = cv2.VideoCapture(0)
with mp_face_detection.FaceDetection(
    model_selection=1, min_detection_confidence=0.5) as face_detection:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_detection.process(image)
    
    # my things
    try:
      # first extract the bounding box coordinates (xmin,ymin,width,height)
      # understand what these measures are:
      # https://github.com/google/mediapipe/blob/master/docs/solutions/face_detection.md#detections
      relative_bounding_box = {
        'xmin': results.detections[0].location_data.relative_bounding_box.xmin,
        'ymin': results.detections[0].location_data.relative_bounding_box.ymin,
        'width': results.detections[0].location_data.relative_bounding_box.width,
        'height': results.detections[0].location_data.relative_bounding_box.height
      }
      bounding_box_corners = {
        'xmin': int(relative_bounding_box['xmin']*image.shape[1]),
        'ymin': int(relative_bounding_box['ymin']*image.shape[0]),
        'width': int(relative_bounding_box['width']*image.shape[1]),
        'height': int(relative_bounding_box['height']*image.shape[0])
      }

      extracted_face_square = image[
        bounding_box_corners['ymin']:bounding_box_corners['ymin']+bounding_box_corners['height'],
        bounding_box_corners['xmin']:bounding_box_corners['xmin']+bounding_box_corners['width']        
      ]
      blured_face = cv2.GaussianBlur(extracted_face_square,(45,45),sigmaX=100.0,sigmaY=2.0)
      new_face = image.copy()
      new_face[
        bounding_box_corners['ymin']:bounding_box_corners['ymin']+bounding_box_corners['height'],
        bounding_box_corners['xmin']:bounding_box_corners['xmin']+bounding_box_corners['width']
      ] = blured_face  
    except:
      print('whatevr')
      pass

    # Draw the face detection annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.detections:
      for detection in results.detections:
        mp_drawing.draw_detection(image, detection)
    # Flip the image horizontally for a selfie-view display.
    fliped_img = cv2.flip(image, 1)
    fliped_g_img = cv2.cvtColor(fliped_img, cv2.COLOR_BGR2GRAY)
    new_face_g = cv2.cvtColor(new_face, cv2.COLOR_RGB2GRAY)
    #cv2.imshow('MediaPipe Face Detection', fliped_g_img)
    #cv2.imshow('Extracted Face', extracted_face_square)
    #cv2.imshow('Blured Face', blured_face)
    cv2.imshow('b l u r e d', new_face_g)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
