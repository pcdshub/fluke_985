import pathlib

from aiohttp import web

MODULE_PATH = pathlib.Path(__file__).parent
SAMPLE_DATA_FILE = MODULE_PATH / 'sample_data.tsv'


async def handle(request):
    with open(SAMPLE_DATA_FILE, 'rt') as f:
        data = f.read()
    return web.Response(text=data)


app = web.Application()
app.add_routes([web.get('/DATA.TSV', handle)])


def main():
    web.run_app(app)


if __name__ == '__main__':
    main()
