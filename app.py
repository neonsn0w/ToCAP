import os

from flask import Flask, render_template, request
from pathlib import Path
from dotenv import load_dotenv

from cookie_checker import check_instagram_cookies
app = Flask(__name__)

load_dotenv()

COOKIES_FOLDER_PATH = os.getenv("COOKIES_FOLDER_PATH")

@app.route('/', methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        cookies = request.form.get("cookies_textbox")

        result = check_instagram_cookies(cookies)

        if result["status"] == "VALID":
            file = Path(COOKIES_FOLDER_PATH + result["username"] + ".txt")
            if not file.exists():
                with open(file, "w") as f:
                    f.write(cookies)
                    f.flush()
            else:
                result = {
                    "status": "DUPLICATE",
                    "message": "Valid but already added"
                }

    return render_template("index.html", result = result)

    return render_template('index.html', processed = processed)

if __name__ == '__main__':
    app.run()
