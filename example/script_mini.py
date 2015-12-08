from time import sleep


def main(a):
    """Emulate some time consuming task.
    """
    sleep(a / 10)
    return a
