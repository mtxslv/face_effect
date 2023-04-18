from pathlib import Path

import cv2
import numpy as np
import mediapipe as mp

def process_files(input_path: Path, 
                  output_path: Path,
                  effects: list) -> None:
    
  all_files = list(input_path.iterdir())
  IMAGE_FILES = [x for x in all_files if x.suffix == '.jpg' or x.suffix == '.jpeg' or x.suffix == '.png']

  mp_face_detection = mp.solutions.face_detection  
  with mp_face_detection.FaceDetection(
      model_selection=1, min_detection_confidence=0.5) as face_detection:
    for idx, file in enumerate(IMAGE_FILES):
      print(file)
      image = cv2.imread(str(file))
      # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
      results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
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
        new_face = image
      
      if 'greyscale' in effects or 'Grayscale' in effects:
        new_face = cv2.cvtColor(new_face, cv2.COLOR_RGB2GRAY)

      file_name = 'processed_' + file.name
      cv2.imwrite( str(output_path/file_name), new_face)

def process_video(effects: list) -> None:
  mp_face_detection = mp.solutions.face_detection
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
        new_face = image
      
      if 'greyscale' in effects or 'Grayscale' in effects:
        new_face = cv2.cvtColor(new_face, cv2.COLOR_RGB2GRAY)
      else:
        new_face = cv2.cvtColor(new_face, cv2.COLOR_BGR2RGB)
      cv2.imshow('b l u r e d', cv2.flip(new_face,1))
      if cv2.waitKey(5) & 0xFF == 27:
        break
  cap.release()