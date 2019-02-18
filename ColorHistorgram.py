import cv2
import numpy as np 
from matplotlib import pyplot as plt
from matplotlib import colors as mcolors

#이미지 불러오기
path = 'frame0.jpg'
img_color = cv2.imread(path)

cv2.namedWindow('Show Image')
cv2.imshow('Show Image', img_color)

cv2.waitKey(0)

img_rgb = cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB)

#이미지 분활
gray_img = cv2.cvtColor(img_color,cv2.COLOR_BGR2GRAY) 
gray_blur = cv2.GaussianBlur(gray_img, (7, 7), 0) 
adapt_thresh_im = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 20) 
max_thresh, thresh_im = cv2.threshold(gray_img, 100, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU) 
thresh = cv2.bitwise_or(adapt_thresh_im, thresh_im) 
kernel = np.ones((3,3),np.uint8) 
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2) 
sure_bg = cv2.dilate(thresh,kernel,iterations=2) 
img_color[sure_bg == 0] = [0,0,0] 
cv2.imwrite('Dframe0.jpg',img_color) 

#HSV로 변환
img = cv2.imread('frame0.jpg') 
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 
print(img_hsv.shape) 
h, s, v = cv2.split(img_hsv) 
cv2.imshow("hsv image", v) 
cv2.waitKey(0)

#히스토그램 평활화
hist, bins = np.histogram(v.flatten(), 256,[0,256])

cdf = hist.cumsum()

# cdf의 값이 0인 경우는 mask처리를 하여 계산에서 제외
# mask처리가 되면 Numpy 계산에서 제외가 됨
# 아래는 cdf array에서 값이 0인 부분을 mask처리함
cdf_m = np.ma.masked_equal(cdf,0)

#History Equalization 공식
cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())

# Mask처리를 했던 부분을 다시 0으로 변환
cdf = np.ma.filled(cdf_m,0).astype('uint8')
equalization_v = cdf[v]
plt.subplot(121),plt.imshow(v),plt.title('Original')
plt.subplot(122),plt.imshow(equalization_v),plt.title('Equalization')
plt.show()

#HSV로 합치기
equalization_hsv = cv2.merge([h, s, equalization_v])
cv2.imshow('IMAGE',equalization_hsv)
cv2.waitKey(0)

#RGB로 변환
equalization_rgb=mcolors.rgb_to_hsv(equalization_hsv)
cv2.imshow('IMAGE',equalization_rgb)
cv2.waitKey(0)
