import cv2
from zipfile import ZipFile
import os
import uuid

def detector(image):
    image = cv2.imread(image)
    final=list()
    smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_smile.xml')
    smiles  = smile_cascade.detectMultiScale(image, scaleFactor = 1.8, minNeighbors = 20)
    if len(smiles)>=1:
        return True
    else:
        return False
 
def extract_frames(input_path, output_directory, frame_rate=1):
    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        print(f"Error: Could not open video file '{input_path}'")
        return
    
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_interval = fps // frame_rate
    os.makedirs(output_directory, exist_ok=True)

    frame_count = 0
    frame_number = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            output_path = os.path.join(output_directory, f"frame_{frame_number:04d}.png")
            cv2.imwrite(output_path, frame)
            frame_number += 1

        frame_count += 1
    cap.release() 
 

def generate_zip(vid):
    code=str(uuid.uuid4())
    extract_frames(vid,f'frames_{code}')
    zipObj = ZipFile(f'output_{code}.zip', 'w')
    for image in os.listdir(f'frames_{code}'):
        if detector(image=fr'frames_{code}\{image}'):
            zipObj.write(fr'frames_{code}\{image}')
    zipObj.close()
    os.remove('input.mp4')
    return code

#generate_zip('frames')