from flask import Flask
import app.irma as irma


app = Flask(__name__)


@app.route("/irma/<sign>")
def see_future(sign:str):
    return irma.see_future(sign)
