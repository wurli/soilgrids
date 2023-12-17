import pytest

from soilgrids._utils import _check_arg, _rscript, _r_available, _to_list


def test_check_arg():
    assert _check_arg(None,       'arg', ['a', 'b']) == ['a', 'b'], 'None should be replaced with all allowed values'
    assert _check_arg([],         'arg', ['a', 'b']) == ['a', 'b'], 'Empty list should be replaced with all allowed values'
    assert _check_arg('a',        'arg', ['a', 'b']) == ['a'],      'Single value should be returned as a list'
    assert _check_arg(['a'],      'arg', ['a', 'b']) == ['a'],      'List of single value should be returned as a list'
    assert _check_arg(['a', 'b'], 'arg', ['a', 'b']) == ['a', 'b'], 'List of multiple values should be returned as a list'
    
    with pytest.raises(AssertionError) as err:
        _check_arg('c', 'arg', ['a', 'b'])
    assert 'Invalid `arg`.'                in str(err.value), 'Error message should indicate name of argument'
    assert "Check 'c'"                     in str(err.value), 'Error message should indicate invalid argument'
    assert "Allowed values are: 'a', 'b'." in str(err.value), 'Error message should indicate allowed values'


def test_rscript():
    if not _r_available():
        pytest.skip('No R installation available')
        
    dummy_data = '"clay","sand","silt","ocs"\n' + \
        '5.1,3.5,1.4,0.2\n' + \
        '4.9,3,1.4,0.2\n' + \
        '4.7,3.2,1.3,0.2\n' + \
        '4.6,3.1,1.5,0.2\n' + \
        '5,3.6,1.4,0.2\n' + \
        '5.4,3.9,1.7,0.4\n' + \
        '4.6,3.4,1.4,0.3\n' + \
        '5,3.4,1.5,0.2\n' + \
        '4.4,2.9,1.4,0.2\n' + \
        '4.9,3.1,1.5,0.1\n'

    lm_summary = _rscript('r-scripts/linear-regression.R', dummy_data)
    assert 'clay + sand + silt ~ ocs' in lm_summary, 'R script should return a linear model summary'
    
    with pytest.raises(RuntimeError) as err:
        _rscript('r-scripts/linear-regression.R', "Bananas")
    
    assert "Arg 1: `Bananas`" in str(err.value),        "Error message should include supplied arguments"
    assert "object 'clay' not found" in str(err.value), "Error message should include R error message"
    
    
def test_to_list():
    assert _to_list('a')   == ['a'],   'Scalar should be converted to list'
    assert _to_list(['a']) == ['a'],   'List should be unchanged'
    assert _to_list('abc') == ['abc'], 'String should be converted to list'
    assert _to_list(1)     == [1],     'Integer should be converted to list'
    assert _to_list(1.0)   == [1.0],   'Float should be converted to list'
    assert _to_list(True)  == [True],  'Boolean should be converted to list'
    assert _to_list(False) == [False], 'Boolean should be converted to list'
    assert _to_list(None)  == [None],  'None should be converted to list'
    
    with pytest.raises(TypeError) as err:
        _to_list({'a': 1})
    assert "Cannot convert <class 'dict'>" in str(err.value), \
        'Invalid input should raise an error specifying the problematic type'
    