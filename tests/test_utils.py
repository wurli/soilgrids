import pytest

from soilgrids._utils import _check_arg, _rscript, _r_available

def test_check_arg():
    assert _check_arg(None,       'arg', ['a', 'b']) == ['a', 'b'], "None should be replaced with all allowed values"
    assert _check_arg([],         'arg', ['a', 'b']) == ['a', 'b'], "Empty list should be replaced with all allowed values"
    assert _check_arg('a',        'arg', ['a', 'b']) == ['a'],      "Single value should be returned as a list"
    assert _check_arg(['a'],      'arg', ['a', 'b']) == ['a'],      "List of single value should be returned as a list"
    assert _check_arg(['a', 'b'], 'arg', ['a', 'b']) == ['a', 'b'], "List of multiple values should be returned as a list"
    
    with pytest.raises(AssertionError) as err:
        _check_arg('c', 'arg', ['a', 'b'])
    assert 'Invalid `arg`.'                in str(err.value), "Error message should contain name of argument"
    assert 'Check "c"'                     in str(err.value), "Error message should contain invalid argument"
    assert 'Allowed values are: "a", "b".' in str(err.value), "Error message should include allowed values"


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

    assert 'clay + sand + silt ~ ocs'        in lm_summary, "R script should return a linear model summary"
    assert 'Residual standard error: 0.5446' in lm_summary, "Model summary should give a standard error of 0.5446"
    assert 'Multiple R-squared:  0.3475'     in lm_summary, "Model summary should give an R-squared of 0.3475"