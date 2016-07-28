"""Evaluate some code within a provided environment
and returning the value of specific evaluated variables
"""
from openalea.core import CompositeNodeFactory as CNF
from openalea.core.pkgmanager import PackageManager


def find_cnf(env):
    """Try to find the first CNF in the given environment.

    Raises: NameError if no CNF can be found
    Args:
        env (dict):

    Returns:
        (CNF): the found CNF
    """
    for k, v in env.items():
        if isinstance(v, CNF):
            return v

    raise NameError("CNF not found")


def find_inport_index(node, name):
    """Find index of an input port based on its name

    Args:
        node (Node):
        name (str): must be unique to node

    Returns:
        (int)
    """
    for i, pdef in enumerate(node.factory.inputs):
        if pdef['name'] == name:
            return i

    raise KeyError("name '%s' not found in inputs of this node" % name)


def find_outport_index(node, name):
    """Find index of an output port based on its name

    Args:
        node (Node):
        name (str): must be unique to node

    Returns:
        (int)
    """
    for i, pdef in enumerate(node.factory.outputs):
        if pdef['name'] == name:
            return i

    raise KeyError("name '%s' not found in outputs of this node" % name)


def eval_workflow(workflow, env, outputs):
    """Evaluate the workflow in the given environment.

    Raises: KeyError if no object called 'main' is found in the code.
    Args:
        workflow (str): workflow definition (as written in wralea files)
        env (dict of any): preset values used as globals during evaluation
        outputs (list of str): list of variable names to retrieve
                               at the end of execution

    Returns:
        (str, str): status of execution and error message if any
        (list of any): value of variables named in outputs
    """
    env = dict(env)
    outvals = []

    try:
        loc = {}
        ast = compile(workflow, "<rem str>", 'exec')
        eval(ast, loc)

        # try to find a CNF in loc
        cnf = find_cnf(loc)

        # instantiate workflow
        pm = PackageManager()
        pm.init()
        cn = cnf.instantiate()

        # fill inputs
        for inname, value in env.items():
            vid_str, pname_str = inname.split(":")
            vid = int(vid_str)
            pname = pname_str.strip()
            n = cn.node(vid)
            n.inputs[find_inport_index(n, pname)] = value

        # evaluate workflow
        prov = cn.eval_as_expression(record_provenance=True)

        # get outputs as result
        if len(outputs) == 1 and outputs[0] == "prov":
            outvals.append(prov.as_wlformat())
        else:
            for outname in outputs:
                vid_str, pname_str = outname.split(":")
                vid = int(vid_str)
                pname = pname_str.strip()
                n = cn.node(vid)
                outvals.append(n.outputs[find_outport_index(n, pname)])

        status = ('OK', "")
    except Exception as e:
        status = (e.__class__.__name__, e.message)

    return status, outvals
