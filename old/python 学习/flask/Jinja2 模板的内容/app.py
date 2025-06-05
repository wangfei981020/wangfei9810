# 创建基本的Flask应用
# 在app.py文件中，我们首先需要创建一个简单的Flask应用，并设置路由，以便在浏览器中访问它。代码如下

from flask import Flask,render_template

app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('hello.html', name='Allen')

# 循环语句
# Jinja2还支持循环，我们可以使用for语句来遍历一组数据。例如，假设我们有一个列表要渲染：

# 在app.py中，我们可以修改索引函数如下：
@app.route('/')
def index():
    items = ['Flask','Django','FastAPI']
    return render_template('hello.html',name='World',items=items)


if __name__ == '__main__':
    app.run(debug=True)