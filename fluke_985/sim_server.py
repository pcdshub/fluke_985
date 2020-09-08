import logging
import pathlib

from aiohttp import web

logger = logging.getLogger(__name__)

MODULE_PATH = pathlib.Path(__file__).parent
HTML_PATH = MODULE_PATH / 'html'

SAMPLE_DATA_FILE = MODULE_PATH / 'sample_data.tsv'


class GlobalState:
    state = 'new_data'
    STATE_TO_HTML = {
        'new_data': HTML_PATH / 'new_data.html',
        'rebuilding': HTML_PATH / 'rebuilding.html',
        'download': HTML_PATH / 'ready-to-download.html',
        'request': HTML_PATH / 'rebuilding.html',
    }

    @staticmethod
    def get_html():
        with open(GlobalState.STATE_TO_HTML[GlobalState.state], 'rt') as f:
            return f.read()

    @staticmethod
    def reset():
        GlobalState.state = 'new_data'

    @staticmethod
    def transition():
        state = GlobalState.state
        new_state = state

        if state == 'request':
            new_state = 'rebuilding'
        elif state == 'rebuilding':
            new_state = 'download'
        elif state == 'download':
            new_state = 'new_data'

        logger.warning('** State=%s -> new state=%s', state, new_state)
        GlobalState.state = new_state


async def handle_data(request):
    with open(SAMPLE_DATA_FILE, 'rt') as f:
        data = f.read()
    GlobalState.reset()
    return web.Response(text=data)


async def handle_main(request):
    data = GlobalState.get_html()
    GlobalState.transition()
    return web.Response(text=data)


async def handle_rebuild(request):
    post_data = await request.post()
    logger.warning('** Got a rebuild POST request! (data=%s)', post_data)

    if post_data.get('BuildFile', None) == 'Build':
        # "BuildFile=Build" to request a data file rebuild
        GlobalState.state = 'request'
        data = GlobalState.get_html()
        # Go to rebuilding for next access
        GlobalState.transition()
    else:
        data = GlobalState.get_html()

    return web.Response(text=data)


app = web.Application()
app.add_routes(
    [
        web.get('/DATA.TSV', handle_data),
        web.get('/', handle_main),
        web.post('/', handle_rebuild),
    ]
)


def main():
    web.run_app(app)


if __name__ == '__main__':
    main()
