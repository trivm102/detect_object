# import face_recognition

# class CompareTwoFaces():
#     def __init__(self, image1, image2):
#         self.image1 = image1
#         self.image2 = image2
    
#     def compare(self):
#         result = self.__checkFaces()
#         print("compare DONE")
#         return result
    
#     def __checkFaces(self):
#         # Load ảnh
#         image1 = face_recognition.load_image_file(self.image1)
#         image2 = face_recognition.load_image_file(self.image2)
#         # Xác định khuôn mặt trong từng ảnh
#         face1_encodings = face_recognition.face_encodings(image1)
#         face2_encodings = face_recognition.face_encodings(image2)
#         # Kiểm tra nếu có khuôn mặt trong cả hai ảnh
#         if len(face1_encodings) > 0 and len(face2_encodings) > 0:
#             # Lấy encoding khuôn mặt đầu tiên trong mỗi ảnh
#             face1_encoding = face1_encodings[0]
#             face2_encoding = face2_encodings[0]

#             # So sánh hai encoding
#             results = face_recognition.compare_faces([face1_encoding], face2_encoding)
#             distance = face_recognition.face_distance([face1_encoding], face2_encoding)
#             distance_score = round(distance[0], 2)
#             cosine_similarity = round((1 - distance[0]) * 100)
#             if results[0]:
#                 print(f"Hai khuôn mặt giống nhau (khoảng cách: {distance[0]:.2f})")
#                 return {"message": f"Hai khuôn mặt giống nhau {cosine_similarity}%",
#                             "result": True,
#                             "distance": distance_score,
#                             "similarity": cosine_similarity}

#             else:
#                 print(f"Hai khuôn mặt khác nhau (khoảng cách: {distance[0]:.2f})")
#                 return {"message": f"Hai khuôn mặt giống nhau {cosine_similarity}%",
#                             "result": False,
#                             "distance": distance_score,
#                             "similarity": cosine_similarity}
#         else:
#             print("Không phát hiện được khuôn mặt trong một hoặc cả hai ảnh!")
#             return {"message": "Không phát hiện được khuôn mặt trong một hoặc cả hai ảnh!",
#                             "result": False}




