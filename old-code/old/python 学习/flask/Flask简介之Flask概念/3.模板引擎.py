from flask import Flask, render_template

app = Flask(__name__)

@app.route('/welcome/<name>')
def welcome(name):
    return render_template('welcome.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)