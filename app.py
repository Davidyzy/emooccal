from flask import Flask,render_template
import request
app = Flask(__name__)
import face_detect
import requests
import json
import os
import cv2
import time


#azure cloud
subscription_key = "3dbd88257b0248d0a7cbbaf782b98a64"
assert subscription_key
headers = {'Content-Type': 'application/octet-stream',
           'Ocp-Apim-Subscription-Key': subscription_key}

face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'emotion',
}


#get camera and capture
cap = cv2.VideoCapture(0)
t=0
while(t<5):
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    cv2.imshow('frame', rgb)
    out1 = cv2.imwrite('image/'+str(t)+'.jpg', frame)
    t+=1
    time.sleep(3)


cap.release()
cv2.destroyAllWindows()


#analyze emotion expression
def analyze_image(img_name):
    image_path = os.path.join('image/' + img_name)
    image_data = open(image_path, 'rb')

    response = requests.post(face_api_url, params=params,
                         headers=headers, data=image_data)
    response_json = response.json()

    #print(response_json)
    emotion_dic = response_json[0]['faceAttributes']['emotion']
    dominant_emotion = max(emotion_dic, key=lambda x: emotion_dic[x])

    return dominant_emotion if emotion_dic[dominant_emotion] > 0.5 else 'complicated'


image_num = len(os.listdir('/Users/apple/Desktop/cs sample/calhack/image/'))
for pic in range(1, image_num-1):
    print(analyze_image(str(pic)+'.jpg')+str(pic*30))


#flask back end
@app.route('/show', methods=['GET'])
def show():
    emotion = request.args.get(analyze_image())
    timepoint = request.args.get('age')

    return render_template("show.html",
                           emotion=emotion,
                           timepoint=timepoint)


if __name__ =="__main__":
    app.run(debug=True,port=8080)