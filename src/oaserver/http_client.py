import requests
from time import sleep

from oaserver.http_server import sw

server_url = "http://127.0.0.1:6544/"


def format_res(response):
    """Return status, ans from result of a request

    Args:
        response (Response): res of a requests to the server

    Returns:
        (tuple):
    """
    d = response.json()
    return d['status'], d['ans']


def ping():
    """Ping server

    Returns:
        (tuple): status, answer
    """
    res = requests.post(server_url + "ping")
    return format_res(res)


def server_state():
    """Ping server to know its state

    Returns:
        (str): actual state of the server
    """
    status, answer = ping()
    return answer['state']


def compute(workflow, data, outputs):
    """Launch a computation on the server

    Args:
        workflow (str): workflow def or python script
        data (dict): set of variables to use as input
        outputs (list of str): name of outputs to retrieve

    Returns:
        (bool): whether the computation started or not
    """
    data = dict(workflow=sw(workflow), data=sw(data), outputs=sw(outputs))
    res = requests.post(server_url + "compute", data=data)
    status, answer = format_res(res)
    return status[0] == 'OK'


def retrieve_results():
    """Fetch results from server.

    Warnings: no attempt are being made to check for validity of results

    Returns:
        (tuple): status, answer
    """
    res = requests.post(server_url + "results")
    return format_res(res)


def wait_for_result(max_time=10, step=0.1):
    """Wait for a computation to finish on the server and retrieve results

    Args:
        max_time (int): maximum number of seconds to wait for answer
        step (float): sleep time between trials

    Returns:
        (tuple): tuple of status, answer
    """
    cum_time = 0.
    while server_state() == "running":
        sleep(step)
        cum_time += step
        if cum_time > max_time:
            raise UserWarning("Maximum time reached without answer")

    return retrieve_results()


if __name__ == '__main__':
    pycode = """
from time import sleep

c = a + b
sleep(c)
"""

    ans = compute("pycode:%s" % pycode, dict(a=1, b=2), ["c"])
    print "compute", ans
    print "results", wait_for_result()

