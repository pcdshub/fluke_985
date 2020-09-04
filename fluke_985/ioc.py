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

    sample_period = pvproperty(
        name='SamplePeriod',
        value=0,
        read_only=True,
        record='longin',
        units='sec',
    )

    sample_volume = pvproperty(
        name='SampleVolume',
        value=0.0,
        read_only=True,
        record='ai',
        units='L',  # TODO update by key
    )

    count_mode = pvproperty(
        name='CountMode',
        value='',
        max_length=40,
        read_only=True,
        record='stringin',
    )

    concentration_mode = pvproperty(
        name='ConcentrationMode',
        value='',
        max_length=40,
        read_only=True,
        record='stringin',
    )

    norm_0_3um = pvproperty(
        name='Norm0_3um',
        value=0.0,
        read_only=True,
        record='ai',
        units='',
        doc='0.3um Normalized to conc. mode volume',
    )

    norm_0_5um = pvproperty(
        name='Norm0_5um',
        value=0.0,
        read_only=True,
        record='ai',
        units='',
        doc='0.5um Normalized to conc. mode volume',
    )

    norm_1_0um = pvproperty(
        name='Norm1_0um',
        value=0.0,
        read_only=True,
        record='ai',
        units='',
        doc='1.0um Normalized to conc. mode volume',
    )

    norm_2_0um = pvproperty(
        name='Norm2_0um',
        value=0.0,
        read_only=True,
        record='ai',
        units='',
        doc='2.0um Normalized to conc. mode volume',
    )

    norm_5_0um = pvproperty(
        name='Norm5_0um',
        value=0.0,
        read_only=True,
        record='ai',
        units='',
        doc='5.0um Normalized to conc. mode volume',
    )

    norm_10_0um = pvproperty(
        name='Norm10_0um',
        value=0.0,
        read_only=True,
        record='ai',
        units='',
        doc='10.0um Normalized to conc. mode volume',
    )

    sample_mode = pvproperty(
        name='SampleMode',
        value='',
        max_length=40,
        read_only=True,
        record='stringin',
        doc='Sample mode (e.g., Automatic)',
    )

    location_name = pvproperty(
        name='LocationName',
        value='',
        max_length=40,
        read_only=True,
        record='stringin',
        doc='Configured location name on device',
    )

    sample_number = pvproperty(
        name='SampleNumber',
        value=0,
        read_only=True,
        record='longin',
        units='',
        doc='Sample number index',
    )

    laser_current = pvproperty(
        name='LaserCurrent',
        value=0.0,
        read_only=True,
        record='ai',
        units='mA',
        doc='',
    )

    calibrated_value = pvproperty(
        name='CalibratedValue',
        value=0.0,
        read_only=True,
        record='ai',
        units='',
        doc='',
    )

    raw_0_3um = pvproperty(
        name='Raw0_3um',
        value=0.0,
        read_only=True,
        record='ai',
        units='',
        doc='0.3um cumulative raw counts',
    )

    raw_0_5um = pvproperty(
        name='Raw0_5um',
        value=0.0,
        read_only=True,
        record='ai',
        units='',
        doc='0.5um cumulative raw counts',
    )

    raw_1_0um = pvproperty(
        name='Raw1_0um',
        value=0.0,
        read_only=True,
        record='ai',
        units='',
        doc='1.0um cumulative raw counts',
    )

    raw_2_0um = pvproperty(
        name='Raw2_0um',
        value=0.0,
        read_only=True,
        record='ai',
        units='',
        doc='2.0um cumulative raw counts',
    )

    raw_5_0um = pvproperty(
        name='Raw5_0um',
        value=0.0,
        read_only=True,
        record='ai',
        units='',
        doc='5.0um cumulative raw counts',
    )

    raw_10_0um = pvproperty(
        name='Raw10_0um',
        value=0.0,
        read_only=True,
        record='ai',
        units='',
        doc='10.0um cumulative raw counts',
    )

    overall_alarm = pvproperty(
        name='OverallAlarm',
        value=0,
        read_only=True,
        record='longin',
        units='',
        doc='Summed alarm status (cal, flow, etc.)',
    )

    cal_alarm = pvproperty(
        name='CalAlarm',
        value=0,
        read_only=True,
        record='longin',
        units='',
        doc='Calibration alarm',
    )

    flow_alarm = pvproperty(
        name='FlowAlarm',
        value=0,
        read_only=True,
        record='longin',
        units='',
        doc='Flow alarm',
    )

    over_conc_alarm = pvproperty(
        name='OverConcAlarm',
        value=0,
        read_only=True,
        record='longin',
        units='',
        doc='Over concentration alarm',
    )

    system_alarm = pvproperty(
        name='SystemAlarm',
        value=0,
        read_only=True,
        record='longin',
        units='',
        doc='System alarm',
    )

    count_alarm = pvproperty(
        name='CountAlarm',
        value=0,
        read_only=True,
        record='longin',
        units='',
        doc='Count alarm',
    )

    battery_alarm = pvproperty(
        name='BatteryAlarm',
        value=0,
        read_only=True,
        record='longin',
        units='',
        doc='Battery alarm',
    )

    laser_alarm = pvproperty(
        name='LaserAlarm',
        value=0,
        read_only=True,
        record='longin',
        units='',
        doc='Laser alarm',
    )
    update_hook = pvproperty(value=0, name='__update_hook__', read_only=True)

    _metadata_to_property = {
        'Model Number': model_number,
        'Serial Number': serial_number,
        'Firmware Version': firmware_version,
        'Hardware Version': hardware_version,
        'Bootloader': bootloader_version,
    }

    _data_key_to_property = {
        'Sample Volume': sample_volume,
        'Count Mode': count_mode,
        'Concentration Mode': concentration_mode,
        '0.3um': norm_0_3um,
        '0.5um': norm_0_5um,
        '1.0um': norm_1_0um,
        '2.0um': norm_2_0um,
        '5.0um': norm_5_0um,
        '10.0um': norm_10_0um,
        'Sample Mode': sample_mode,
        'Location Name': location_name,
        'Sample Number': sample_number,
        'Cal. Value': calibrated_value,
        'Laser Current': laser_current,
        '0.3um (Cum. Counts)': raw_0_3um,
        '0.5um (Cum. Counts)': raw_0_5um,
        '1.0um (Cum. Counts)': raw_1_0um,
        '2.0um (Cum. Counts)': raw_2_0um,
        '5.0um (Cum. Counts)': raw_5_0um,
        '10.0um (Cum. Counts)': raw_10_0um,
        'Cal Alarm': cal_alarm,
        'Flow Alarm': flow_alarm,
        'Over Conc. Alarm': over_conc_alarm,
        'System Alarm': system_alarm,
        'Count Alarm': count_alarm,
        'Battery Alarm': battery_alarm,
        'Laser Alarm': laser_alarm,
        # Custom
        # 'Sample Units': ,
        # overall_alarm
        # 'Sample Period': sample_period,
    }

    async def _write_metadata(self,
                              pvprop: pvproperty,
                              value: str):
        """
        Update the metadata, if changed.
        """
        value = value[:pvprop.max_length]
        if pvprop.value != value:
            await pvprop.write(value=value)

    @update_hook.startup
    async def update_hook(self, instance, async_lib):
        metadata, df = load_fluke_data_file('data.tsv')

        for key, pvprop in self._metadata_to_property.items():
            await self._write_metadata(
                pvprop=getattr(self, pvprop.attr_name),
                value=metadata.get(key, 'unknown')
            )

        timestamp, row = list(df.tail().iterrows())[-1]
        for key, value in row.items():
            try:
                prop = self._data_key_to_property[key]
            except KeyError:
                continue

            prop = getattr(self, prop.attr_name)
            await prop.write(value=value)

        try:
            units = row['Sample Units']
        except KeyError:
            ...
        else:
            await self.sample_volume.write_metadata(units=units)

        # TODO:
        # row['Sample Period']


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
