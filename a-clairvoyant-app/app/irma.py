import os
import csv
import argparse


ROOT = os.path.dirname(__file__) + "/"


def check_sign(sign):
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


def read_future(sign):
    """Read future form external source.


    Arguments:
        sign (str): Astrological sign for which predict future.

    Returns:
        (str): The future for the given astrological sign
    """
    res = "no future"
    with open(ROOT + "data/future.csv", "rb") as f:
        reader = csv.DictReader(f)
        future = filter(lambda x: x["sign"] == sign, reader)
        if future:
            res = future[0]["future"]

    return res


def see_future(sign):
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

    print(res.format(cur_sign.capitalize(),
                     read_future(cur_sign).capitalize()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="I can see your future.")
    parser.add_argument("sign", type=str, help="Your astrological sign.")
    args = parser.parse_args()

    see_future(args.sign)
