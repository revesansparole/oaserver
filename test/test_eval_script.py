from nose.tools import assert_raises

from oaserver.eval_script import eval_script


def test_script_is_python():
    script = "<html><body>toto</body></html>"
    assert_raises(SyntaxError, lambda: eval_script(script, {}, []))


def test_script_is_valid_python():
    script = "a = 1\nb"
    assert_raises(NameError, lambda: eval_script(script, {}, []))
    script = "a = (}"
    assert_raises(SyntaxError, lambda: eval_script(script, {}, []))
    script = "a = []\na[1]"
    assert_raises(IndexError, lambda: eval_script(script, {}, []))
    script = "a = []\na.toto"
    assert_raises(AttributeError, lambda: eval_script(script, {}, []))
    script = "def toto():\n  print(1)\n print(2)"
    assert_raises(IndentationError, lambda: eval_script(script, {}, []))


def test_eval_script_raise_keyerror_if_return_value_do_not_exists():
    script = "c = a + b"
    env = {'a': 1, 'b': 2}
    assert_raises(KeyError, lambda: eval_script(script, env, ['toto']))


def test_eval_script_is_working():
    script = "c = a + b"
    vals = eval_script(script, {'a': 1, 'b': 2}, ['c'])
    assert vals[0] == 3
