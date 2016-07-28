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
        (list of any): value of variables named in outputs
    """
    loc = dict(env)

    ast = compile(pycode, "<rem str>", 'exec')
    eval(ast, loc)
    return [loc[name] for name in outputs]
