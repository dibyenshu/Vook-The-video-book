from havenondemand.hodclient import *
from havenondemand.hodresponseparser import *
import re
import cv2
import numpy as np
import math

###############################
print("Transcribing audio")
###############################
#GET TEXT
loc = ""
fh = open("C:/Users/DM/Documents/vook/info.txt", "r")
loc = fh.readlines()
fh.close()
hodClient = HODClient("51996ed0-fdeb-4b6f-b6e2-d097465f6cd3")
parser = HODResponseParser()
hodApp = ""
loc[0] = loc[0][:-1]
style = loc[2][:-1]
result = ""

# callback function
def asyncRequestCompleted(response, **context):
	jobID = parser.parse_jobid(response)
	if jobID is None:
		errorObj = parser.get_last_error()
		for err in errorObj.errors:
			print ("Error code: %d \nReason: %s \nDetails: %s\n" % (err.error,err.reason, err.detail))
	else:
		hodClient.get_job_status(jobID, requestCompleted, **context)

def requestCompleted(response, **context):
        global result
        payloadObj = parser.parse_payload(response)
        if payloadObj is None:
                errorObj = parser.get_last_error()
                resp = ""
                for err in errorObj.errors:
                        if err.error == ErrorCode.QUEUED:
                                # wait for some time then call GetJobStatus or GetJobResult again with the same jobID from err.jobID
                                print ("job is queued. Retry in 2 secs. jobID: " + err.jobID)
                                time.sleep(2)
                                hodClient.get_job_status(err.jobID, requestCompleted, **context)
                                return
                        elif err.error == ErrorCode.IN_PROGRESS:
                                # wait for some time then call GetJobStatus or GetJobResult again with the same jobID from err.jobID
                                print ("task is in progress. Retry in 10 secs. jobID: " + err.jobID)
                                time.sleep(10)
                                hodClient.get_job_status(err.jobID, requestCompleted, **context)
                                return
                        else:
                                resp += "Error code: %d \nReason: %s \nDetails: %s\njobID: %s\n" % (err.error,err.reason, err.detail, err.jobID)
                print (resp)
        else:
                app = context["hodapp"]
                resp = ""
                if app == HODApps.RECOGNIZE_SPEECH:
                        documents = payloadObj["document"]
                        for doc in documents:
                                resp += doc["content"] + "\n"
                        result = resp
                        #paramArr = {}
                        #print ("Reconized text:\n" + resp)
                        #paramArr["text"] = resp
                        return



hodApp = HODApps.RECOGNIZE_SPEECH
paramArr = {}
loc_vid = []
loc_vid.append(loc[0])
paramArr["file"] = loc_vid
#paramArr["url"] = "https://www.havenondemand.com/sample-content/videos/hpnext.mp4"

context = {}
context["hodapp"] = hodApp

hodClient.post_request(paramArr, hodApp, async=True, callback=asyncRequestCompleted, **context)

result = re.sub('<.*?> ', '', result)
#print(result)

fo = open("C:/Users/DM/Documents/vook/output.txt", "w")
fo.write(result);
fo.close()


########################
print("Fetching frames")
########################
class Cartoonizer:
    """Cartoonizer effect
        A class that applies a cartoon effect to an image.
        The class uses a bilateral filter and adaptive thresholding to create
        a cartoon effect.
    """
    def __init__(self):
        pass

    def render(self, img_rgb):
        img_rgb = cv2.resize(img_rgb, (1366,768))
        numDownSamples = 2       # number of downscaling steps
        numBilateralFilters = 50  # number of bilateral filtering steps

        # -- STEP 1 --
        # downsample image using Gaussian pyramid
        img_color = img_rgb
        for _ in range(numDownSamples):
            img_color = cv2.pyrDown(img_color)
        #cv2.imshow("downcolor",img_color)
        #cv2.waitKey(0)
        # repeatedly apply small bilateral filter instead of applying
        # one large filter
        for _ in range(numBilateralFilters):
            img_color = cv2.bilateralFilter(img_color, 9, 9, 7)
        #cv2.imshow("bilateral filter",img_color)
        #cv2.waitKey(0)
        # upsample image to original size
        for _ in range(numDownSamples):
            img_color = cv2.pyrUp(img_color)
        #cv2.imshow("upscaling",img_color)
        #cv2.waitKey(0)
        # -- STEPS 2 and 3 --
        # convert to grayscale and apply median blur
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
        img_blur = cv2.medianBlur(img_gray, 3)
        #cv2.imshow("grayscale+median blur",img_color)
        #cv2.waitKey(0)
        # -- STEP 4 --
        # detect and enhance edges
        img_edge = cv2.adaptiveThreshold(img_blur, 255,
                                         cv2.ADAPTIVE_THRESH_MEAN_C,
                                         cv2.THRESH_BINARY, 9, 2)
        #cv2.imshow("edge",img_edge)
        #cv2.waitKey(0)

        # -- STEP 5 --
        # convert back to color so that it can be bit-ANDed with color image
        (x,y,z) = img_color.shape
        img_edge = cv2.resize(img_edge,(y,x)) 
        img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
        #cv2.imwrite("edge.png",img_edge)
        #cv2.imshow("step 5", img_edge)
        #cv2.waitKey(0)
        #img_edge = cv2.resize(img_edge,(i for i in img_color.shape[:2]))
        #print img_edge.shape, img_color.shape
        return cv2.bitwise_and(img_color, img_edge)
tmp_canvas = Cartoonizer()
#GET FRAMES

cap =cv2.VideoCapture(loc[0])

frame_dis = 40
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
string = ""
string = str(math.ceil(length/frame_dis))
fo = open("C:/Users/DM/Documents/vook/frame_count.txt", "w")
fo.write(string);
fo.close()

counter = 0
frame_counter = 0
while True:
    ret, frame = cap.read()    
    if frame_counter%frame_dis == 0:
        if style == 'Normal':    
                cv2.imwrite("C:/Users/DM/Documents/vook/frames/"+ str(counter) + ".jpg",frame)
                counter += 1
        else:                  
                res = tmp_canvas.render(frame)
                cv2.imwrite("C:/Users/DM/Documents/vook/frames/"+ str(counter) + ".jpg", res)
                counter += 1
    frame_counter += 1
    if frame_counter == length:
        break

fh = open("C:/Users/DM/Documents/vook/status.txt", "w")
fh.write("1")
fh.close()
