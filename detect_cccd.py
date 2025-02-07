from ultralytics import YOLO
from inference_sdk import InferenceHTTPClient
from ocr import Orc
import cv2

model = YOLO("best_cccd.pt")
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="rek0guyPgQJRNt5CF2vD"
)


class DetectCCCD():
    def __init__(self, file_path_front, file_path_back):
        self.file_path_front = file_path_front
        self.file_path_back = file_path_back

    async def detect_cccd_front(self):
        return self.__detect(self.file_path_front)
        # img = cv2.imread(self.file_path_front)
        # results = CLIENT.infer(self.file_path_front, model_id="bv10_15_2024/10")
        # data ={}
        # current_place = ""
        # for pred in results["predictions"]:
        #     class_name = pred["class"]
        #     pred["x"] = pred["x"] - (pred["width"] / 2)
        #     pred["y"] = pred["y"] - (pred["height"] / 2)
        #     x1 = pred["x"]
        #     y1 = pred["y"]
        #     x2 = x1 + pred["width"]
        #     y2 = y1 + pred["height"]
        #     cropped = img[int(y1):int(y2), int(x1):int(x2)]
        #     text = Orc(cropped).image_to_string()
        #     if(class_name == "current_place"):
        #         if(current_place == ""):
        #             current_place = text
        #         else:
        #             text = f"{current_place}, {text}"
        #     if(self.__convert_key(class_name) is not ""):
        #         data[self.__convert_key(class_name)] = text
        # print("detect_cccd_front DONE")
        # # return results
        # return data
        
    
    async def detect_cccd_back(self):
        return self.__detect(self.file_path_back)
        # img = cv2.imread(self.file_path_back)
        # results = CLIENT.infer(self.file_path_back, model_id="bv10_15_2024/10")
        # for pred in results["predictions"]:
        #     pred["x"] = pred["x"] - (pred["width"] / 2)
        #     pred["y"] = pred["y"] - (pred["height"] / 2)
        #     x1 = pred["x"]
        #     y1 = pred["y"]
        #     x2 = x1 + pred["width"]
        #     y2 = y1 + pred["height"]
        #     # cropped = img[int(y1):int(y2), int(x1):int(x2)]
        #     # text = Orc(cropped).image_to_string()
        #     # pred["text"] = text
        # print("detect_cccd_back DONE")
        # return results
    
    # def detect_cccd_front(self):
    #     return self.__detect()

    def __detect(self, img_path):
        # Read image from which text needs to be extracted
        img = cv2.imread(img_path)
        results = model(img_path)
        data = {}
        for result in results:
            current_place = ""
            for box in result.boxes:  # Lặp qua từng bounding box
                cls_id = int(box.cls[0])  # ID của lớp
                class_name = model.names[cls_id] 
                confidence = float(box.conf[0])  # Độ tin cậy
                x1, y1, x2, y2 = map(float, box.xyxy[0])  # Tọa độ bounding box (xmin, ymin, xmax, ymax)
                # print(f"Class Name: {class_name} Class ID: {cls_id}, Confidence: {confidence}, BBox: ({x1}, {y1}, {x2}, {y2})")
                # data["x"] = x1
                # data["y"] = y1
                # data["width"] = x2 - x1
                # data["height"] = y2 - y1
                # data["class"] = class_name
                # data["class_id"] = cls_id
                # data["confidence"] = confidence
                cropped = img[int(y1):int(y2), int(x1):int(x2)]
                text = Orc(cropped).image_to_string()

                print(f"{class_name}: {text}")
                if(class_name == "current_place"):
                    if(current_place == ""):
                        current_place = text
                    else:
                        temp = sorted([text, current_place], key=len)
                        text = ", ".join(temp)
                if(self.__convert_key(class_name) != ""):
                    data[self.__convert_key(class_name)] = text
        return data
    def __convert_key(self, class_name):
        switcher ={
            "dob": "birthDate",
            "origin_place": "originPlace",
            "name": "fullName",
            "id": "idCardNo",
            "expire_date": "expiryDate",
            "nationality": "nationality",
            "current_place": "residencePlace",
            "gender": "gender",
            "gender": "gender",
        }
        return switcher.get(class_name, "")

