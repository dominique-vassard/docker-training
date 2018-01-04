import click
from flask import Flask

from app.utils.database import IrmaDb
import app.irma as irma
import app.db_operations as db_ops


app = Flask(__name__)

# CONFIG
app.config["DB_HOST"] = "172.17.0.3"
app.config["DB_PORT"] = 3306
app.config["DB_USER"] = "irma"
app.config["DB_PASSWORD"] = "cr1StalB4ll"
app.config["DB_NAME"] = "irma"

db = IrmaDb(app.config["DB_HOST"], app.config["DB_PORT"],
            app.config["DB_USER"], app.config["DB_PASSWORD"],
            app.config["DB_NAME"])


# ROUTING
@app.route("/irma/<sign>")
def see_future(sign):
    return irma.see_future(sign, db)


# COMMAND
@app.cli.command()
def initdb():
    """Initialize the database."""
    db_ops.init_db(db)
    db_ops.initial_feed(db)
    click.echo('Database initialized')
