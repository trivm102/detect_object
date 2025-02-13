from PIL import Image
import pytesseract
import cv2

class Orc():
    def __init__(self, img):
        self.img = img
    
    def image_to_string(self):
        # name =random.randint(1, 1000000)
        # cv2.imwrite(f"{name}.jpg", self.img)
        text = pytesseract.image_to_string(self.img, lang="vie", config=self.__custom_config)
        if text is None:
            text = self.__preprocessing()
        return text.strip()
    
    def __preprocessing(self):
        # Đọc ảnh
        copied_image = self.img.copy()
        image = cv2.cvtColor(copied_image, cv2.COLOR_BGR2GRAY)
        # Tiền xử lý ảnh
        image = cv2.GaussianBlur(image, (5, 5), 0)  # Giảm nhiễu
        _, image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Ngưỡng hóa
        image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)  # Phóng to

        # Nhận diện văn bản
        text = pytesseract.image_to_string(image, lang="vie", config=self.__custom_config)
        return text
    
    __custom_config = r'--oem 3 --psm 6'
    # Tối ưu cấu hình của pytesseract
    # --oem: Chế độ OCR Engine:
    # 0: Chỉ Legacy OCR.
    # 1: Chỉ LSTM OCR.
    # 3: Kết hợp cả hai.
    # --psm: Chế độ phân tích trang (Page Segmentation Mode):
    # 6: Tìm một khối văn bản duy nhất.
    # 11: Nhận diện văn bản dạng đơn dòng.