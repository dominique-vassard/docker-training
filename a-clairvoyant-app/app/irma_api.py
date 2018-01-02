from flask import Flask
import irma


app = Flask(__name__)


@app.route("/irma/<sign>")
def see_future(sign):
    return irma.see_future(sign)
