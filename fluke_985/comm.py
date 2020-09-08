import re
from typing import Optional

import aiohttp

BASE_URL = 'http://{host}:{port}/'
DATA_FILE_URL = BASE_URL + 'DATA.TSV'
REBUILD_URL = BASE_URL
CHECK_STATE_URL = BASE_URL

RE_NUM_RECORDS = re.compile(r'DATA\.TSV.*?left>(\d\d*)<.td>')

REBUILD_POST_DATA = {'BuildFile': 'Build'}


_session = None


def get_global_session() -> aiohttp.ClientSession:
    """Get the shared aiohttp ClientSession."""
    global _session
    if _session is None:
        _session = aiohttp.ClientSession()
    return _session


async def get_data_file(
        host: str,
        *,
        port: int = 80,
        session: Optional[aiohttp.ClientSession] = None,
        ) -> str:
    """
    Query the Fluke and retrieve the TSV file.

    Parameters
    ----------
    host : str
        The Fluke hostname.

    port : int, optional
        The webserver port - should likely remain as the default of 80.

    session : aiohttp.ClientSession, optional
        The client session - defaults to using the globally shared one.
    """

    if session is None:
        session = get_global_session()

    url = DATA_FILE_URL.format(host=host, port=port)

    async with session.get(url) as response:
        data = await response.text()
        # assert response.status == 200
        return data


async def request_rebuild(
        host: str,
        *,
        port: int = 80,
        session: Optional[aiohttp.ClientSession] = None,
        data: Optional[dict] = None,
        ) -> str:
    """
    Request that the Fluke rebuild its data file.

    Parameters
    ----------
    host : str
        The Fluke hostname.

    port : int, optional
        The webserver port - should likely remain as the default of 80.

    session : aiohttp.ClientSession, optional
        The client session - defaults to using the globally shared one.

    data : dict, optional
        Post data to send, in place of the confirmed-working
        ``REBUILD_POST_DATA``.
    """

    if session is None:
        session = get_global_session()

    if data is None:
        data = REBUILD_POST_DATA

    url = REBUILD_URL.format(host=host, port=port)

    async with session.put(url, data=data) as response:
        data = await response.text()
        # assert response.status == 200
        return data


async def check_state(
        host: str,
        *,
        port: int = 80,
        session: Optional[aiohttp.ClientSession] = None,
        ) -> str:
    """
    Query the Fluke and check for its current state.

    Parameters
    ----------
    host : str
        The Fluke hostname.

    port : int, optional
        The webserver port - should likely remain as the default of 80.

    session : aiohttp.ClientSession, optional
        The client session - defaults to using the globally shared one.

    Returns
    -------
    state_info : dict
    """

    if session is None:
        session = get_global_session()

    url = CHECK_STATE_URL.format(host=host, port=port)

    async with session.get(url) as response:
        data = await response.text()
        return get_state_information(data)


def get_state_information(html) -> dict:
    """
    Get Fluke state information from a given html source.

    Does not use any html parsers as the format appears to be reasonably
    static.

    Parameters
    ----------
    html : str
        Raw HTML source code.

    Returns
    -------
    state_info : dict
        State information.
    """
    if 'New data available.' in html:
        state = 'new_data'
    elif 'Building Data file' in html:
        state = 'rebuilding'
    elif 'Click link above to download' in html:
        state = 'download'
    else:
        state = 'unknown'

    state_info = {'state': state}

    m = RE_NUM_RECORDS.search(html)
    if m:
        records, = m.groups()
        state_info['records'] = int(records)

    return state_info
