import datetime
import pathlib

import pytest

import fluke_985
import fluke_985.data

TEST_ROOT = pathlib.Path(__file__).parent


@pytest.fixture
def data_filename() -> pathlib.Path:
    return TEST_ROOT.parent / 'sample_data.tsv'


def test_load(data_filename):
    with open(data_filename, 'rt') as f:
        metadata, data = fluke_985.load_fluke_data_file(f)

    assert metadata['Model Number'] == '985'
    timestamp, row = list(data.iterrows())[-1]
    assert timestamp == datetime.datetime.fromisoformat('2020-08-25 09:53:31')
    assert row['Sample Period'] == '00:15:00'
    # Lots o' data
    assert len(row) == 29

    assert fluke_985.data.sample_period_to_seconds(
        '01:02:03') == (3600 + 120 + 3)
    assert fluke_985.data.summarize_alarms(row) == 0
