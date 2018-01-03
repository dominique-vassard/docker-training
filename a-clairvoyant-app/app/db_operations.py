# from app.irma_api import app

# print(app.config)
# from app.irma_api import app


def init_db(db):
    sql = """
        CREATE TABLE IF NOT EXISTS predictions(
            sign VARCHAR(15) NOT NULL,
            future VARCHAR(255) NOT NULL,
            INDEX sign_idx(sign)
            )
    """
    db.execute(sql)
    return True


def initial_feed(db):
    db.execute("TRUNCATE TABLE predictions")

    sql = """
        INSERT INTO predictions(sign, future) VALUES
        ("aries","Are those horns?"),
        ("taurus","You will be stubborn!"),
        ("gemini","Invest one, gain two!"),
        ("cancer","Go on a tropical island!"),
        ("leo","You will gain a beautiful collar"),
        ("virgo","Don't be so prude!"),
        ("libra","You will be in equal mood."),
        ("scorpio","You should contact Sting."),
        ("sagittarius","Steal the rich to give to the poor!"),
        ("capricorn","Your future is a chimera!"),
        ("aquarius","Your glass is full of water."),
        ("pisces","Obviously, you're not a dolphin!")
    """

    db.execute(sql)
    return True


def read_future(sign, db):
    """Read future form database.


    Arguments:
        sign (str): Astrological sign for which predict future.

    Returns:
        (str): The future for the given astrological sign
    """
    res = "no future"
    sql = """
        SELECT future
        FROM predictions
        WHERE sign = %s"""
    params = [sign]

    q_results = db.execute(sql, params)
    results = [row["future"] for row in q_results]

    if results:
        res = results[0]

    return res
