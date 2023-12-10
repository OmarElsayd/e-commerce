from random import choices
from string import ascii_uppercase, digits


def gen_order_confirmation(len_=30) -> str:
    """

    :param len_: 30 fixed unless changed
    :return: Confirmation Number
    """
    return "".join(
        choices(
            ascii_uppercase + digits,
            k=len_
        )
    )
