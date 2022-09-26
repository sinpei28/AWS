from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/helloWorld")
def helloWorld():
    return render_template('hello.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)