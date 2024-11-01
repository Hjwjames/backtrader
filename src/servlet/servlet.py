from flask import Flask, jsonify
from flask import request

app = Flask(__name__)

# 定义一个简单的路由
@app.route('/')
def home():
    return "欢迎来到 Flask 示例应用！"

# 定义一个 RESTful API 路由
@app.route('/api/data', methods=['GET'])
def get_data():
    # 返回一些示例数据
    data = {'name': 'Flask', 'type': 'Web Framework'}
    return jsonify(data)  # 将字典转换为 JSON 格式并返回

# 处理 POST 请求
@app.route('/api/data', methods=['POST'])
def create_data():
    new_data = request.get_json()  # 获取 JSON 请求体
    return jsonify(new_data), 201  # 返回新数据和 HTTP 201 状态码

if __name__ == '__main__':
    app.run(debug=True)  # 开启调试模式，便于开发时检查错误

