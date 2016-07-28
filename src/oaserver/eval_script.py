"""Evaluate some code within a provided environment
and returning the value of specific evaluated variables
"""


def eval_script(pycode, env, outputs):
    """Evaluate pycode in the given environment.

    Args:
        pycode (str): python script as txt
        env (dict of any): preset values used as globals during evaluation
        outputs (list of str): list of variable names to retrieve
                               at the end of execution

    Returns:
        (str, str): status of execution and error message if any
        (list of any): value of variables named in outputs
    """
    loc = dict(env)

    try:
        ast = compile(pycode, "<rem str>", 'exec')
        eval(ast, loc)
        outvals = [loc[name] for name in outputs]
        status = ('OK', "")
    except Exception as e:
        status = (e.__class__.__name__, e.message)
        outvals = []

    return status, outvals
