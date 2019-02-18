import cv2

cap = cv2.VideoCapture('newface.mp4')
# 영상의 의미지를 연속적으로 캡쳐할 수 있게 하는 class
vidcap = cv2.VideoCapture('newface.mp4')
 
count = 0
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print('length : ', length)
fps = cap.get(cv2.CAP_PROP_FPS)
print('fps : ', fps)

while(vidcap.isOpened()):
    ret, image = vidcap.read()
 
    if(int(vidcap.get(1)) % 23 == 0):
        #print('Saved frame number : ' + str(int(vidcap.get(1))))
        cv2.imwrite("frame%d.jpg" % count, image)
        #print('Saved frame%d.jpg' % count)
        count += 1

 
vidcap.release()

