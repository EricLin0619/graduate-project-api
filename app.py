import base64
from flask import Flask, jsonify, request
import urllib.request
import urllib.error
import time
import json
import pymongo
import certifi

app=Flask(__name__)
client = pymongo.MongoClient("mongodb+srv://Eric:zx50312zx@training.9vikg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db = client.cosme #選擇操作cosme資料庫

### 首頁，測試用
@app.route("/",methods=["GET","POST"])
def index():
    return jsonify({"success":True,"message":"It's face++ api."})

### 取得 face_analysis 的資料
@app.route("/face_analysis",methods=["GET","POST"])
def face_analysis():
    ### get imgfile represented in base64 
    analysis_result={}
    data = request.values["data"]
    imgData = base64.b64decode(data)
    #print(type(imgData))

    http_url = 'https://api-cn.faceplusplus.com/facepp/v1/facialfeatures'
    key = "0nzG98sy92I9MJeW_RwrSlxkTNiylvdJ"
    secret = "tckC6RMYCSTD1DNRvnYsoe4XpLr4F_dN"
    filepath = "https://i0.wp.com/post.medicalnewstoday.com/wp-content/uploads/sites/3/2020/03/GettyImages-1092658864_hero-1024x575.jpg?w=1155&h=1528"

    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
    data.append(key)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
    data.append(secret)
    data.append('--%s' % boundary)
    
    data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file')
    data.append('Content-Type: %s\r\n' % 'application/octet-stream')
    data.append(imgData)

    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_landmark')
    data.append('1')
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_attributes')
    data.append(
        "gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,skinstatus")
    data.append('--%s--\r\n' % boundary)

    for i, d in enumerate(data):
        if isinstance(d, str):
            data[i] = d.encode('utf-8')

    http_body = b'\r\n'.join(data)

    # build http request
    req = urllib.request.Request(url=http_url, data=http_body)

    # header
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)

    try:
        # post data to server
        resp = urllib.request.urlopen(req, timeout=5)
        # get response
        qrcont = resp.read()
        # if you want to load as json, you should decode first,
        # for example: json.loads(qrount.decode('utf-8'))
        #print(type(json.loads(qrcont.decode('utf-8'))))
        qrcont = json.loads(qrcont.decode('utf-8'))
        analysis_result["nose_type"] = qrcont["result"]["nose"]["nose_type"]
        analysis_result["face_type"] = qrcont['result']['face']["face_type"]
        analysis_result["jaw_type"] =  qrcont['result']['jaw']["jaw_type"]
        analysis_result["eyebrow_type"] = qrcont['result']['eyebrow']["eyebrow_type"]
        analysis_result["eye_type"] = qrcont['result']['eyes']["eyes_type"]
        return jsonify(analysis_result)
        
    except urllib.error.HTTPError as e:
        print(e.read().decode('utf-8'))

### 取得 face_detect 的資料
@app.route("/face_detect",methods=["GET","POST"])
def face_detect():
    ### get imgfile represented in base64 
    data = request.values["data"]
    imgData = base64.b64decode(data)
    #print(type(imgData))

    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    key = "0nzG98sy92I9MJeW_RwrSlxkTNiylvdJ"
    secret = "tckC6RMYCSTD1DNRvnYsoe4XpLr4F_dN"
    filepath = "https://i0.wp.com/post.medicalnewstoday.com/wp-content/uploads/sites/3/2020/03/GettyImages-1092658864_hero-1024x575.jpg?w=1155&h=1528"

    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
    data.append(key)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
    data.append(secret)
    data.append('--%s' % boundary)
    
    data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file')
    data.append('Content-Type: %s\r\n' % 'application/octet-stream')
    data.append(imgData)

    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_landmark')
    data.append('1')
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_attributes')
    data.append(
        "gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,skinstatus")
    data.append('--%s--\r\n' % boundary)

    for i, d in enumerate(data):
        if isinstance(d, str):
            data[i] = d.encode('utf-8')

    http_body = b'\r\n'.join(data)

    # build http request
    req = urllib.request.Request(url=http_url, data=http_body)

    # header
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)

    try:
        # post data to server
        resp = urllib.request.urlopen(req, timeout=5)
        # get response
        qrcont = resp.read()
        # if you want to load as json, you should decode first,
        # for example: json.loads(qrount.decode('utf-8'))
        print(type(json.loads(qrcont.decode('utf-8'))))
        return jsonify(json.loads(qrcont.decode('utf-8')))
        
    except urllib.error.HTTPError as e:
        print(e.read().decode('utf-8'))


############################################################# 化妝品資料
### 資料處理function
def get_data(cosmetics_name):
    ### convert byte to base64
    def byteString_to_byte(data):
        data=data.encode(encoding="ascii")
        result2 = data.decode('unicode-escape').encode('ISO-8859-1')
        base64Data = base64.b64encode(result2)
        return base64Data
    collection = db[cosmetics_name]
    result = collection.find()
    data = []
    frontSentence = "data:image/png;base64,"
    for x in result:
        del x["_id"]
        x["image"] = frontSentence+str(byteString_to_byte(x["image"][2:-1]))[2:-1]
        data.append(x)
    return jsonify(data)

### 取得唇膏資料
@app.route("/get-lipstick")
def get_lipstick():
    return get_data("lipstick")

### 取得腮紅資料
@app.route("/get-blush")
def get_blush():
    return get_data("blush")

### 取得唇蜜資料
@app.route("/get-lipgloss")
def get_lip_gloss():
    return get_data("lip_gloss")

### 取得眼影資料
@app.route("/get-eyeshadow")
def get_eye_shadow():
    return get_data("eye_shadow")


if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)