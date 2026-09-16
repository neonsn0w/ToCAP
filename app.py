from flask import Flask, render_template, request

from cookie_checker import check_instagram_cookies
app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        cookies = request.form.get("cookies_textbox")

        mlep = check_instagram_cookies(cookies)

    return render_template("index.html", result = mlep)



    return render_template('index.html', processed = processed)

if __name__ == '__main__':
    app.run()
