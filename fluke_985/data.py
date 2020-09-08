import itertools
from typing import Dict, Optional, TextIO, Tuple

import pandas as pd

ALARM_KEYS = (
    'Cal Alarm',
    'Flow Alarm',
    'Over Conc. Alarm',
    'System Alarm',
    'Count Alarm',
    'Battery Alarm',
    'Laser Alarm'
)


def load_fluke_data_file(
        fp: TextIO,
        timezone: Optional[str] = None
        ) -> Tuple[Dict[str, str], pd.DataFrame]:
    """
    Load a fluke 985 tab-delimited data file.

    Parameters
    ----------
    fp : file-like object
        The data file.

    timezone : str, optional
        Time zone to use for the date/time index.

    Returns
    -------
    metadata : dict
        A dictionary of metadata, including "Model Number" and others specified
        in the header.

    df : pandas.DataFrame
        The data.

    Notes
    -----

    The data file is of the general format::

        {metadata}
        (blank line)
        ... Counts normalized to concentration mode volume ...
        {table}
    """
    last_md_line, metadata = _get_metadata(fp)
    fp.seek(0)
    df = pd.read_csv(
        fp,
        skiprows=last_md_line + 1,
        delimiter='\t',
        parse_dates=[['Date', 'Time']],
        index_col='Date_Time'
    )

    if timezone is not None:
        df.index = df.index.tz_localize(timezone)

    return metadata, df


def _get_metadata(fp: TextIO) -> Tuple[int, Dict[str, str]]:
    """
    Load metadata from a fluke 985 tab-delimited data file.

    Parameters
    ----------
    fp : file-like object
        The data file.

    Returns
    -------
    last_md_line : int
        The index of the blank line between metadata and the table.

    metadata : dict
        A dictionary of metadata, including "Model Number" and others specified
        in the header.
    """
    metadata = {}
    last_md_line = 0
    fp.seek(0)
    for line_number in itertools.count(start=1):
        line = fp.readline().strip()
        if ':' not in line:
            last_md_line = line_number
            break

        key, value = line.split(':', 1)
        metadata[key.strip()] = value.strip()

    return last_md_line, metadata


def sample_period_to_seconds(sample_period: str) -> int:
    """
    Convert the sample period to seconds.

    Parameters
    ----------
    sample_period : str
        A sample period reading from the data file.

    Returns
    -------
    sample_period int
        Sample period in seconds.
    """
    hours, minutes, seconds = sample_period.split(':')
    return 3600 * int(hours) + 60 * int(minutes) + int(seconds)


def summarize_alarms(row) -> int:
    """
    Summarize alarm status from a given row.

    Parameters
    ----------
    row : pandas.Series
        The row from the dataframe.

    Returns
    -------
    summary : int
        An alarm value of zero is considered NO_ALARM, whereas a non-zero alarm
        value is considered MAJOR.
    """
    return max(row[key] for key in ALARM_KEYS)
