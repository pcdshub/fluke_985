import pytest

import fluke_985


@pytest.fixture
def ioc_instance() -> fluke_985.Fluke985Base:
    ioc = fluke_985.create_ioc(prefix='prefix',
                               host=('hostname', 8080),
                               autosave='autosave.json')
    return ioc


def test_init(ioc_instance):
    assert ioc_instance.prefix == 'prefix'
    assert ioc_instance._default_host == ('hostname', 8080)


# TODO: not much else we can do easily here
