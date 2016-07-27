from nose.tools import assert_raises

from oaserver.eval_script import eval_script


def test_script_is_python():
    script = "<html><body>toto</body></html>"
    status, vals = eval_script(script, {}, [])
    assert status[0] == 'SyntaxError'


def test_script_is_valid_python():
    script = "a = 1\nb"
    status, vals = eval_script(script, {}, [])
    assert status[0] == 'NameError'
    script = "a = (}"
    status, vals = eval_script(script, {}, [])
    assert status[0] == 'SyntaxError'
    script = "a = []\na[1]"
    status, vals = eval_script(script, {}, [])
    assert status[0] == 'IndexError'
    script = "a = []\na.toto"
    status, vals = eval_script(script, {}, [])
    assert status[0] == 'AttributeError'
    script = "def toto():\n  print(1)\n print(2)"
    status, vals = eval_script(script, {}, [])
    assert status[0] == 'IndentationError'


def test_eval_script_raise_keyerror_if_return_value_do_not_exists():
    script = "c = a + b"
    env = {'a': 1, 'b': 2}
    assert_raises(KeyError, lambda: eval_script(script, env, ['toto']))


def test_eval_script_is_working():
    script = "c = a + b"
    status, vals = eval_script(script, {'a': 1, 'b': 2}, ['c'])
    assert status[0] == 'OK'
    assert vals[0] == 3
