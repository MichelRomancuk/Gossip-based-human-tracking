import face_recognition
from picamera2 import Picamera2, Preview
import time
import socket



# Get the face encodings for each face in each image file
# Since there could be more than one face in each image, it returns a list of encodings.
# But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
def face_rec():
    while True:
        try:
            # Take picture 
            picam2.capture_file("tmp.jpg")
            tmp_image = face_recognition.load_image_file("tmp.jpg")
            tmp_encoding = face_recognition.face_encodings(tmp_image)[0]

        except IndexError:
            continue
        # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
        try:
            results = face_recognition.compare_faces(known_faces, tmp_encoding)
            # Check for known faces; Add aditional faces with elif blocks. 
            if results[0]:
                local_gossip = "Michel" + ";" + socket.gethostname() + ";" + "0"
                if check_new(local_gossip):
                    write_local_gossip(local_gossip)
            elif results[1]:
                local_gossip = "Natalia" + ";" + socket.gethostname() + ";" + "0"
                if check_new(local_gossip):
                    write_local_gossip(local_gossip)
            time.sleep(1)
        except UnboundLocalError:
            continue

def write_local_gossip(local_gossip):
    global i
    with open('local_gossip.txt', 'r') as file:
        content = file.read().strip()
        file.close()
    parts = content.split(';')
    i = int(parts[2])+1
    parts[2] = str(i)
    new_parts = local_gossip.split(';')
    with open('local_gossip.txt', 'w') as file:
        output = new_parts[0] + ';' + new_parts[1] + ';' + parts[2]
        file.write(output)
        file.truncate()

def check_new(local_gossip):
    with open('local_gossip.txt', 'r') as file:
        old = file.read().strip()
        file.close()
    old_parts = old.split(';')
    local_parts = local_gossip.split(';')
    print(old_parts)
    if old_parts[0] == local_parts[0] and old_parts[1] == local_parts[1]:
        return False
    else:
        return True


if __name__ == "__main__":
    print("Starting")
    i = 0
    # Set up camera
    picam2 = Picamera2()
    picam2.start()
    time.sleep(2)

    # Load the jpg files into numpy arrays
    Michel_image = face_recognition.load_image_file("Michel.jpg")
    Michel_encoding = face_recognition.face_encodings(Michel_image)[0]
    Natalia_image = face_recognition.load_image_file("Natalia.jpg")
    Natalia_encoding = face_recognition.face_encodings(Natalia_image)[0]
    
    # Array for face recognition:
    known_faces = [
        Michel_encoding,
        Natalia_encoding
    ]
    
    # Start face_rec
    face_rec()
    
    
