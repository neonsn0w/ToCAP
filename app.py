import os
import re

from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pathlib import Path
from dotenv import load_dotenv

from cookie_checker import check_instagram_cookies
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024  # Limit to 64 KB
limiter = Limiter(get_remote_address, app=app)
csrf = CSRFProtect(app)

load_dotenv()

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
COOKIES_FOLDER_PATH = os.getenv("COOKIES_FOLDER_PATH")

base_dir = Path(COOKIES_FOLDER_PATH).resolve()

@app.route('/', methods=["GET", "POST"])
@limiter.limit("20 per minute")
def index():
    result = None

    if request.method == "POST":
        cookies = request.form.get("cookies_textbox")

        result = check_instagram_cookies(cookies)

        if result["status"] == "VALID":
            safe_username = re.sub(r'[^a-zA-Z0-9._-]', '', result["username"])
            file = (base_dir / f"{safe_username}.txt").resolve()
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

if __name__ == '__main__':
    app.run()
