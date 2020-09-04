import pathlib

from caproto.server import (PVGroup, SubGroup, pvproperty, run,
                            template_arg_parser)
from caproto.server.autosave import AutosaveHelper, RotatingFileManager

from . import util
from .data import load_fluke_data_file


class Fluke985Base(PVGroup):
    model_number = pvproperty(
        value='',
        max_length=40,
        name='ModelNumber',
        read_only=True,
        record='stringin',
    )

    serial_number = pvproperty(
        value='',
        max_length=40,
        name='SerialNumber',
        read_only=True,
        record='stringin',
    )

    firmware_version = pvproperty(
        value='',
        max_length=40,
        name='FirmwareVersion',
        read_only=True,
        record='stringin',
    )

    hardware_version = pvproperty(
        value='',
        max_length=40,
        name='HardwareVersion',
        read_only=True,
        record='stringin',
    )

    bootloader_version = pvproperty(
        value='',
        max_length=40,
        name='BootloaderVersion',
        read_only=True,
        record='stringin',
    )

    update_hook = pvproperty(value=0, name='__update_hook__', read_only=True)

    metadata_to_property = {
        'Model Number': model_number,
        'Serial Number': serial_number,
        'Firmware Version': firmware_version,
        'Hardware Version': hardware_version,
        'Bootloader': bootloader_version,
    }

    async def _write_metadata(self, pvprop, value):
        if pvprop.value == value:
            return

        await pvprop.write(value=value)

    @update_hook.startup
    async def update_hook(self, instance, async_lib):
        metadata, df = load_fluke_data_file('data.tsv')
        print('update')

        for key, pvprop in self.metadata_to_property.items():
            await self._write_metadata(
                pvprop=getattr(self, pvprop.attr_name),
                value=metadata.get(key, 'unknown')
            )


def create_ioc(prefix: str, *,
               autosave: str,
               **ioc_options) -> Fluke985Base:
    """
    Create a new Fluke 985 IOC.

    Parameters
    ----------
    prefix : str
        The IOC prefix.

    autosave : str or pathlib.Path
        Path for autosave settings (JSON format).

    **ioc_options :
        Passed to Fluke985Base().

    Returns
    -------
    ioc : Fluke985Main
        IOC instance.
    """
    autosave = pathlib.Path(autosave).resolve().absolute()

    class Fluke985Main(Fluke985Base):
        autosave_helper = SubGroup(AutosaveHelper,
                                   file_manager=RotatingFileManager(autosave))
        autosave_helper.filename = autosave

    return Fluke985Main(
        prefix=prefix,
        **ioc_options
    )


def main():
    parser, split_args = template_arg_parser(
        default_prefix='TEST:FLUKE:985:',
        desc='Fluke 985 particle counter IOC',
        supported_async_libs=('asyncio', )
    )

    parser.add_argument(
        '--autosave',
        help='Path to the autosave file',
        default='autosave.json',
        type=str
    )

    args = parser.parse_args()
    print(args)
    ioc_options, run_options = split_args(args)

    ioc = create_ioc(autosave=args.autosave, **ioc_options)
    if args.verbose is None or args.verbose == 0:
        log_level = 'INFO'
    else:
        log_level = 'DEBUG'

    util.config_logging(ioc.log, level=log_level)
    run(ioc.pvdb, **run_options)


if __name__ == '__main__':
    main()
