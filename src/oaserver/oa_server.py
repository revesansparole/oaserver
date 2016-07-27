""" Implement an OA server according to communication protocol
with scifloware specifications.
"""

from threading import Thread

# from eval_dataflow import eval_dataflow
# from eval_node import eval_node
from .eval_script import eval_script


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
        self._status = None
        self._buffer = {}

    def registered(self):
        """Call this function once server registration is effective
        """
        self._state = "waiting"

    def ping(self):
        """Check the actual state of the server.

        Returns:
            (dict)
        """
        return dict(id=self._sid, state=self._state)

    def compute(self, workflow, data, outputs):
        """Launch computation in a separated thread and return.

        Args:
            workflow (str): workflow def or python script
            data (dict): set of variables to use as input
            outputs (list of str): name of outputs to retrieve

        Returns:
            (bool): whether the computation started or not
        """
        if self._state != "waiting":
            return False

        self._state = "running"
        self._status = None
        self._buffer.clear()

        # launch computation in separated thread
        th = Thread(target=self.perform_task, args=(workflow, data, outputs))
        th.start()

        # return
        return True

    def retrieve_results(self):
        """Retrieves result from last task.
        """
        return self._status, dict(self._buffer)

    def delete(self):
        """Invalidate this server.
        """
        self._state = "deleted"
        print "deleted", self._sid

    def perform_task(self, workflow, data, outputs):
        """Compute given workflow and send back result.

        Notes: write directly result in buffer

        Args:
            workflow (str): workflow def or python script
            data (dict): set of variables to use as input
            outputs (list of str): name of outputs to retrieve

        Returns:
            None
        """
        print "task started"
        # analyse workflow argument and perform computation
        if workflow.startswith("pycode:"):
            pycode = workflow[7:]
            if len(pycode) == 0:
                raise UserWarning("pycode not defined")

            status, vals = eval_script(pycode, data, outputs)
            res = dict(zip(outputs, vals))

        # elif workflow.startswith("dataflow:"):
        #     dataflow = workflow[9:]
        #     if len(dataflow) == 0:
        #         raise UserWarning("dataflow code not defined")
        #
        #     return eval_dataflow(dataflow, data)
        #
        # elif ":" in workflow:
        #     pkg_id, node_id = workflow.split(":")
        #     if len(pkg_id) == 0:
        #         raise UserWarning("package not defined")
        #     if len(node_id) == 0:
        #         raise UserWarning("node not defined")
        #
        #     return eval_node((pkg_id, node_id), data)

        else:
            raise UserWarning("unrecognized workflow type")

        print "task done"
        if self._state == "running":
            # write result in buffer
            if len(self._buffer) > 0:
                # problem somebody else mess up with buffer
                raise UserWarning("Problem with parallel computations")
            self._status = status
            self._buffer.update(res)

            self._state = "waiting"
