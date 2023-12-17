import pytest

from soilgrids._utils import _check_arg, _rscript, _r_available, _to_list, _pkg_file


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
        
    assert _rscript('r-scripts/eval-parse.R', 'cat(1 + 1)') == '2', \
        'R script should return the console output of the expression'
    
    with pytest.raises(RuntimeError) as err:
        _rscript('r-scripts/eval-parse.R', 'stop("Oh no!")')
    
    assert 'Check the R script at r-scripts/eval-parse.R' in str(err.value), \
        "Error message should indicate the location of the problematic script"
    
    assert '`stop("Oh no!")' in str(err.value), \
        "Error message should indicate the supplied arguments"
        
    assert 'Error in eval(parse(text = line)) : Oh no!' in str(err.value), \
        "Error message should indicate the error returned by R"
    
    with pytest.raises(FileNotFoundError) as err:
        _rscript('r-scripts/bananas.R', 'cat(1 + 1)')
    

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
 
    
def test_pkg_file():
    file = _pkg_file('../tests/test_utils.py')
    
    assert file.endswith('tests/test_utils.py'), \
        "_pkg_file() should return the absolute path to the specified file"
        
    with pytest.raises(FileNotFoundError) as err:
        _pkg_file('bananas.txt')
    assert 'bananas.txt' in str(err.value), \
        "_pkg_file() should raise an informative error if the file doesn't exist"