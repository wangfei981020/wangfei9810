from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '欢迎来到Flask应用首页！'


@app.route('/about')
def about():
    return '这是关于页面'

@app.route('/contact')
def contact():
    return '这是联系页面'

#路由中的参数
# 有时，我们希望路由能够接收动态参数。例如，设想我们有一个用户资料页面，根据用户ID来展示不同用户的信息。

# 我们可以定义如下路由：
@app.route('/user/<int:user_id>')
def user_profile(user_id):
    return f'用户ID：{user_id}'

# 多种参数类型
# Flask允许多种参数类型定义。除了<int:>，还可以使用：

# <float:>：匹配浮点数
# <path:>：匹配斜杠（/）的路径
# <string:>：匹配任何字符串（默认情况）
# 例如，以下路由定义了一个接受字符串的路径：

@app.route('/file/<path:filename>')
def show_file(filename):
    return f'你访问的文件是：{filename}'



if __name__ == '__main__':
    app.run(debug=True)