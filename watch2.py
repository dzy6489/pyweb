from watchdog.observers import Observer
from watchdog.events import *
import requests
import base64
import cv2 as cv

# 处理器
class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        if event.is_directory:
            print("directory moved from {0} to {1}".format(event.src_path, event.dest_path))
        else:
            print("file moved from {0} to {1}".format(event.src_path, event.dest_path))

    def on_created(self, event):
        if event.is_directory:
            print("directory created:{0}".format(event.src_path))
        else:
            print("file created:{0}".format(event.src_path))
            request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_analysis"
            # 二进制方式打开图片文件
            filename = 'upload/'+event.src_path.split("\\")[1]
            f = open(filename, 'rb')
            img = base64.b64encode(f.read())

            params = {"image": img}
            access_token = '24.49fba9bdc48e206feae6047a0b2231c1.2592000.1676682217.282335-29799651'
            request_url = request_url + "?access_token=" + access_token
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            response = requests.post(request_url, data=params, headers=headers)
            if response:
                print(response.json())
            nose_x = int(response.json()['person_info'][0]['body_parts']['nose']['x'])
            nose_y = int(response.json()['person_info'][0]['body_parts']['nose']['y'])
            right_knee_x = int(response.json()['person_info'][0]['body_parts']['right_knee']['x'])
            right_knee_y = int(response.json()['person_info'][0]['body_parts']['right_knee']['y'])

            img = cv.imread(filename)

            point_size = 1
            point_color = (0, 0, 255)  # BGR
            thickness = 5

            # 画点
            point1 = (nose_x, nose_y)  # 点的坐标。画点实际上就是画半径很小的实心圆。
            point2 = (right_knee_x,right_knee_y)
            cv.circle(img, point1, point_size, point_color, thickness)
            cv.line(img, point1,point2, point_size, point_color, thickness)

            cv.imshow('Main Window', img)

            cv.waitKey()  # 任意键退出

            cv.destroyAllWindows()

    def on_deleted(self, event):
        if event.is_directory:
            print("directory deleted:{0}".format(event.src_path))
        else:
            print("file deleted:{0}".format(event.src_path))

    def on_modified(self, event):
        if event.is_directory:
            print("directory modified:{0}".format(event.src_path))
        else:
            print("file modified:{0}".format(event.src_path))


if __name__ == '__main__':
    observer = Observer()
    # 处理器初始化时候这里可以传些参进去
    event_handler = FileEventHandler()
    # 监控的文件夹
    observer.schedule(event_handler, r"./upload", True)
    observer.start()
    observer.join()