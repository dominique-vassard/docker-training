import app.db_operations as db_ops


def check_sign(sign:str):
    """Check if given astrological sign is valid.
    Sanitizes the result.

    Arguments:
        sign (str): THe astrological sign to check.

    Returns:
        (str): A valid lowercased astrological sign

    Raises:
        (Exception): if astrologicalk sign in not valid
    """
    valid_signs = [
        "aries",
        "taurus",
        "gemini",
        "cancer",
        "leo",
        "virgo",
        "libra",
        "scorpio",
        "sagittarius",
        "capricorn",
        "aquarius",
        "pisces"
    ]

    cur_sign = sign.lower()
    if cur_sign in valid_signs:
        return cur_sign
    else:
        raise Exception("This sign does not exists")


def see_future(sign:str, db):
    """Clairvoyant function.

    Give me your sign, I'll tell your future.

    Arguments:
        sign (str): A valid astrological sign
    """
    cur_sign = check_sign(sign)
    res = """
    {}, your future is:
    {}
    """

    return res.format(cur_sign.capitalize(),
                      db_ops.read_future(cur_sign, db).capitalize())
