import os
from flask import Flask, request, jsonify
from detect_cccd import DetectCCCD
from compare_two_faces import CompareTwoFaces
import asyncio

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "<h1>Home</h1>"

# Đường dẫn lưu trữ tệp
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Giới hạn kích thước tệp tối đa (ví dụ: 24MB)
app.config['MAX_CONTENT_LENGTH'] = 24 * 1024 * 1024

# Tạo thư mục lưu trữ nếu không tồn tại
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/extract-document', methods=['POST'])
async def extract_document():
    images = __get_images(request)
    if images is None:
        return jsonify({"error": "something error files"}), 400
    front, back = images
    model = DetectCCCD(front, back)
    results = await asyncio.gather(model.detect_cccd_front(), model.detect_cccd_back())
    detect_front = results[0]
    detect_back = results[1]
    return jsonify({"message":  "successfully", "object": detect_front}), 20

@app.route("/")
def hello_world():
  """Example Hello World route."""
  name = os.environ.get("NAME", "World")
  return f"Hello {name}!"

@app.route('/check_faces', methods=['POST'])
def api_check_faces():
    files = request.files
    file1_path = None 
    file2_path = None
    compare = None
    if 'file_1' in files:
        file1 = files['file_1']
        file1_path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(file1_path)
    if 'file_2' in files:
        file2 = files['file_2']
        file2_path = os.path.join(app.config['UPLOAD_FOLDER'], file2.filename)
        file2.save(file2_path)
    if file1_path is None or file2_path is None:
        return jsonify({"error": "Files error"}), 400
    
    else:
        compare = CompareTwoFaces(file1_path, file2_path).compare()
    
    return jsonify({"compare": compare}), 200

async def check_faces(front, face):
    compare = CompareTwoFaces(front, face).compare()
    return {"compare": compare}

def __get_images(request):
    files = request.files
    front = None 
    back = None
    if 'frontImage' in files:
        file1 = files['frontImage']
        front = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(front)
    if 'backImage' in files:
        file2 = files['backImage']
        back = os.path.join(app.config['UPLOAD_FOLDER'], file2.filename)
        file2.save(back)
    if front is None or back is None:
        return None
    return [front, back]

if __name__ == "__main__":
    # app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
    app.run()
