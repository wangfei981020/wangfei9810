# 在 Flask 中，定义视图函数非常简单。我们通常使用 @app.route() 装饰器来绑定特定的 URL 路径与函数。下面是一个简单的示例：

from flask import Flask
from flask import render_template
from flask import jsonify

app = Flask(__name__)

@app.route('/about')
def about():
    return render_template('about.html')

# 返回 json 格式
@app.route('/api/data')
def data():
    return jsonify({"message": "Hello, JSON!"})

# 处理请求参数
@app.route('/user/<username>')
def profile(username):
    return f"Hello, {username}!"

@app.route('/')
def home():
    return "Hello, Flask!"

# 视图函数的错误处理
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

if __name__ == '__main__':
    app.run(debug=True)

