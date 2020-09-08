import pathlib

import pytest

import fluke_985
import fluke_985.html

HTML_PATH = pathlib.Path(fluke_985.html.__file__).parent


@pytest.mark.parametrize(
    'html_filename, expected',
    [
        pytest.param(HTML_PATH / 'new_data.html',
                     {"state": 'new_data', 'records': 8402},
                     id='new_data'),
        pytest.param(HTML_PATH / 'rebuilding.html',
                     {"state": 'rebuilding', 'records': 8746},
                     id='rebuilding'),
        pytest.param(HTML_PATH / 'ready-to-download.html',
                     {"state": 'download', 'records': 8746},
                     id='download',
                     ),
    ],
)
def test_get_information(html_filename, expected):
    with open(html_filename, 'rt') as f:
        html = f.read()
    assert fluke_985.comm.get_state_information(html) == expected
