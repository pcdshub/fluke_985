from typing import Optional

import aiohttp

DATA_FILE_URL = 'http://{host}:{port}/DATA.TSV'
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
    """

    if session is None:
        session = get_global_session()

    url = DATA_FILE_URL.format(host=host, port=port)

    async with session.get(url) as response:
        data = await response.text()
        # assert response.status == 200
        return data
