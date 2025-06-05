from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def home():
    # 定义一个字典，包含用户信息
    user_info = {
        'name': 'Alice',
        'age': 28,
        # 'hobby': 'painting'
        'hobbies': ['painting', 'reading', 'gaming'] 
    }
    return render_template('index.html',user=user_info)

if __name__ == '__main__':
    app.run(debug=True)

