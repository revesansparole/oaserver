from time import sleep


def main(a):
    """Emulate some time consuming task.

    Args:
        a: (float) any number

    Returns:
        (float) return parameter a
    """
    sleep(a / 10)
    return a
