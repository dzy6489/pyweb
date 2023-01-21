import requests
import base64
import cv2 as cv
'''
人体关键点识别
'''

request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_analysis"
# 二进制方式打开图片文件
f = open('111.jpg', 'rb')
img = base64.b64encode(f.read())

params = {"image":img}
access_token = '24.49fba9bdc48e206feae6047a0b2231c1.2592000.1676682217.282335-29799651'
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print (response.json())


filename='111.jpg'

img=cv.imread(filename)

point_size = 1
point_color = (0, 0, 255)  # BGR
thickness = 5

# 画点
point = (95, 451)  # 点的坐标。画点实际上就是画半径很小的实心圆。
cv.circle(img, point, point_size, point_color, thickness)


cv.imshow('Main Window',img)

cv.waitKey() #任意键退出

cv.destroyAllWindows()

