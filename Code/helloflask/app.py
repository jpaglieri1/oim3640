from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, Babson! Let's build some web applications!"

@app.route("/hello/<name>")
def hello(name):
    if name is None:
        name = "World"
    name = name.capitalize()



    html = f"<h1 style='color: red;'>Hello, {name}!<h1> <p1>Welcome to Flask development.</p>"
    return html

@app.route('/helllo/<name>')
def greet(name):
    return render_template('hello.html',name=name)

if __name__ == "__main__":
    app.run(debug=True)