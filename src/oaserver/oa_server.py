""" Implement an OA server according to communication protocol
with scifloware specifications.
"""

# from eval_dataflow import eval_dataflow
# from eval_node import eval_node
from .eval_script import eval_script
from .json_tools import get_json, post_json
from .uos import ensure_url, URLError


class OAServer(object):
    """ object used to encapsulate communication with SFW server
    """
    def __init__(self, sid):
        """Constructor

        Args:
            sid: (str) unique id for this server.

        Returns:
            None
        """
        self._sid = sid
        self._state = "created"

    def state(self):
        """Return current state of server.

        Returns:
            (str): "created", "waiting" or "running"
        """
        return self._state

    def server_id(self):
        """Return id of this server.
        """
        return self._sid

    def set_server_id(self, sid):
        """Set id of a non launched server.

        Args:
            sid: (str)

        Returns:
            None
        """
        assert self._state == "created"
        self._sid = sid

    def registered(self):
        """Call this function once server registration is effective
        """
        self._state = "waiting"

    def ping(self, url):
        """Check the actual state of the server.

        Args:
            url: (url) url used to send response message

        Returns:
            None
        """
        data = {"id": self._sid, "state": self._state}
        post_json(url, data)

    def _compute(self, workflow, url_data):
        # analyse url_data argument
        url_data = ensure_url(url_data, 'code')
        if url_data.scheme == 'code':
            ast = compile(url_data.path, "<rem str>", 'exec')
            data = {}
            try:
                eval(ast, data)
            except Exception as e:
                raise UserWarning("error in data pycode: %s" % e)

            del data['__builtins__']
        else:
            data = get_json(url_data)

        # analyse workflow argument and perform computation
        if workflow.startswith("pycode:"):
            pycode = workflow[7:]
            if len(pycode) == 0:
                raise UserWarning("pycode not defined")

            self._state = "running"
            return eval_script(pycode, data)

        # elif workflow.startswith("dataflow:"):
        #     dataflow = workflow[9:]
        #     if len(dataflow) == 0:
        #         raise UserWarning("dataflow code not defined")
        #
        #     self._state = "running"
        #     return eval_dataflow(dataflow, data)
        #
        # elif ":" in workflow:
        #     pkg_id, node_id = workflow.split(":")
        #     if len(pkg_id) == 0:
        #         raise UserWarning("package not defined")
        #     if len(node_id) == 0:
        #         raise UserWarning("node not defined")
        #
        #     self._state = "running"
        #     return eval_node((pkg_id, node_id), data)

        else:
            raise UserWarning("unrecognized workflow type")

    def compute(self, workflow, url_data, url_return):
        """Compute given workflow and send back result.

        Args:
            workflow: (str) id of dataflow to use or python code
            url_data: (url) url of file to read to get data or python dict
            url_return: (url) url to use to send result

        Returns:

        """
        assert self._state == "waiting"
        self._state = "running"

        try:
            result = self._compute(workflow, url_data)

            # send result
            data = {"id": self._sid,
                    "result": result}

            post_json(url_return, data)
        except (URLError, UserWarning, ValueError) as e:
            raise UserWarning(e)
        finally:
            self._state = "waiting"

    def delete(self):
        """Invalidate this server.
        """
        self._state = "deleted"
        print "deleted", self._sid
