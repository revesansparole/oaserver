""" Implement an OA client according to communication protocol
with scifloware specifications to communicate with OAServers.
"""

from time import sleep


class OAClient(object):
    """ object used to encapsulate communication with OA router
    """
    def __init__(self, router):
        """ Constructor
        """
        self._router = router

        self._answer = None

    def set_answer(self, ans):
        self._answer = ans

    def ping(self):
        """Poll all available OA servers for their current state

        Test function not hopefully useful
        """
        self._answer = None
        self._router.servers_state(self)
        while self._answer is None:
            sleep(0.5)

        return self._answer

    def compute(self, pycode, data):
        """Execute a script on OAS and wait for answer.
        """
        self._answer = None
        self._router.compute(self, pycode, data)
        while self._answer is None:
            sleep(0.5)

        return self._answer
