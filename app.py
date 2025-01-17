from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('upload.html')


@app.route("/button-pressed", methods=['POST'])
def button_pressed():
    print("pressed the button")


if __name__ == "__main__":
    app.run(debug=True)
