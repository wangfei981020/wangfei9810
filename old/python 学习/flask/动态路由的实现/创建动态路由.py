from flask import Flask, jsonify

app= Flask(__name__)

# 定义一个动态路由
@app.route('/user/<username>')
def show_user_profile(username):
    # 返回用户信息
    return jsonify({"message": f"Welcome, {username}!"})

# 动态路由的类型
# Flask 支持多种类型的动态路由参数。我们可以指定参数类型，例如整数、浮点数等。例如：
@app.route('/post/<int:post_id>')
def show_post(post_id):
    return jsonify({"post_id": post_id})

# 处理多个动态参数
# 我们还可以在一个路由中同时处理多个动态参数，例如：
@app.route('/message/<username>/<int:post_id>')
def show_message(username,post_id):
    return jsonify({"user": username, "post_id": post_id})

if __name__ == '__main__':
    app.run(debug=True)