import os
import csv
import argparse


ROOT = os.path.dirname(__file__) + "/"


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


def read_future(sign:str):
    """Read future form external source.


    Arguments:
        sign (str): Astrological sign for which predict future.

    Returns:
        (str): The future for the given astrological sign
    """
    res = "no future"
    with open(ROOT + "data/future.csv", "r") as f:
        reader = csv.DictReader(f)
        future = list(filter(lambda x: x["sign"] == sign, reader))
        if future:
            res = future[0]["future"]

    return res


def see_future(sign:str):
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
                      read_future(cur_sign).capitalize())
