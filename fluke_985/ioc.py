import io
import pathlib
import time

from caproto import AlarmSeverity, AlarmStatus
from caproto.server import (PVGroup, SubGroup, pvproperty, run,
                            template_arg_parser)
from caproto.server.autosave import AutosaveHelper, RotatingFileManager

from . import comm, data, util  # noqa


class Fluke985Base(PVGroup):
    """
    Base class for the Fluke985 IOC.

    Parameters
    ----------
    host : Tuple[str, int]
        Fluke 985 device hostname or IP address and port.

    prefix : str
        Prefix for all PVs in the group.

    macros : dict, optional
        Dictionary of macro name to value.

    name : str, optional
        Name for the group, defaults to the class name.
    """

    def __init__(self, *args, host, **kwargs):
        super().__init__(*args, **kwargs)
        self._default_host = host

    host = pvproperty(
        value='',
        max_length=60,
        name='Host',
        read_only=True,
        record='stringin',
    )

    port = pvproperty(
        value=80,
        name='Port',
        read_only=True,
        record='longin',
    )

    @host.startup
    async def host(self, instance, async_lib):
        await self.host.write(self._default_host[0])
        await self.port.write(self._default_host[1])

    server_state = pvproperty(
        value='unknown',
        max_length=40,
        name='ServerState',
        read_only=True,
        record='stringin',
    )

    num_records = pvproperty(
        value=0,
        name='NumRecords',
        read_only=True,
        record='longin',
    )

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
        alarm_group='sample_period',
    )

    sample_volume = pvproperty(
        name='SampleVolume',
        value=0.0,
        read_only=True,
        record='ai',
        units='L',
        alarm_group='sample_volume',
    )

    count_mode = pvproperty(
        name='CountMode',
        value='',
        max_length=40,
        read_only=True,
        record='stringin',
        alarm_group='count_mode',
    )

    concentration_mode = pvproperty(
        name='ConcentrationMode',
        value='',
        max_length=40,
        read_only=True,
        record='stringin',
        alarm_group='concentration_mode',
    )

    norm_0_3um = pvproperty(
        name='Norm0_3um',
        value=0.0,
        read_only=True,
        record='ai',
        units='',
        doc='0.3um Normalized to conc. mode volume',
        alarm_group='norm_0_3um',
    )

    norm_0_5um = pvproperty(
        name='Norm0_5um',
        value=0.0,
        read_only=True,
        record='ai',
        units='',
        doc='0.5um Normalized to conc. mode volume',
        alarm_group='norm_0_5um',
    )

    norm_1_0um = pvproperty(
        name='Norm1_0um',
        value=0.0,
        read_only=True,
        record='ai',
        units='',
        doc='1.0um Normalized to conc. mode volume',
        alarm_group='norm_1_0um',
    )

    norm_2_0um = pvproperty(
        name='Norm2_0um',
        value=0.0,
        read_only=True,
        record='ai',
        units='',
        doc='2.0um Normalized to conc. mode volume',
        alarm_group='norm_2_0um',
    )

    norm_5_0um = pvproperty(
        name='Norm5_0um',
        value=0.0,
        read_only=True,
        record='ai',
        units='',
        doc='5.0um Normalized to conc. mode volume',
        alarm_group='norm_5_0um',
    )

    norm_10_0um = pvproperty(
        name='Norm10_0um',
        value=0.0,
        read_only=True,
        record='ai',
        units='',
        doc='10.0um Normalized to conc. mode volume',
        alarm_group='norm_10_0um',
    )

    sample_mode = pvproperty(
        name='SampleMode',
        value='',
        max_length=40,
        read_only=True,
        record='stringin',
        doc='Sample mode (e.g., Automatic)',
        alarm_group='sample_mode',
    )

    location_name = pvproperty(
        name='LocationName',
        value='',
        max_length=40,
        read_only=True,
        record='stringin',
        doc='Configured location name on device',
        alarm_group='location_name',
    )

    sample_number = pvproperty(
        name='SampleNumber',
        value=0,
        read_only=True,
        record='longin',
        units='',
        doc='Sample number index',
        alarm_group='sample_number',
    )

    laser_current = pvproperty(
        name='LaserCurrent',
        value=0.0,
        read_only=True,
        record='ai',
        units='mA',
        doc='',
        alarm_group='laser_current',
    )

    calibrated_value = pvproperty(
        name='CalibratedValue',
        value=0.0,
        read_only=True,
        record='ai',
        units='',
        doc='',
        alarm_group='calibrated_value',
    )

    raw_0_3um = pvproperty(
        name='Raw0_3um',
        value=0.0,
        read_only=True,
        record='ai',
        units='',
        doc='0.3um cumulative raw counts',
        alarm_group='raw_0_3um',
    )

    raw_0_5um = pvproperty(
        name='Raw0_5um',
        value=0.0,
        read_only=True,
        record='ai',
        units='',
        doc='0.5um cumulative raw counts',
        alarm_group='raw_0_5um',
    )

    raw_1_0um = pvproperty(
        name='Raw1_0um',
        value=0.0,
        read_only=True,
        record='ai',
        units='',
        doc='1.0um cumulative raw counts',
        alarm_group='raw_1_0um',
    )

    raw_2_0um = pvproperty(
        name='Raw2_0um',
        value=0.0,
        read_only=True,
        record='ai',
        units='',
        doc='2.0um cumulative raw counts',
        alarm_group='raw_2_0um',
    )

    raw_5_0um = pvproperty(
        name='Raw5_0um',
        value=0.0,
        read_only=True,
        record='ai',
        units='',
        doc='5.0um cumulative raw counts',
        alarm_group='raw_5_0um',
    )

    raw_10_0um = pvproperty(
        name='Raw10_0um',
        value=0.0,
        read_only=True,
        record='ai',
        units='',
        doc='10.0um cumulative raw counts',
        alarm_group='raw_10_0um',
    )

    overall_alarm = pvproperty(
        name='OverallAlarm',
        value=0,
        read_only=True,
        record='longin',
        units='',
        doc='Summed alarm status (cal, flow, etc.)',
        alarm_group='overall_alarm',
    )

    cal_alarm = pvproperty(
        name='CalAlarm',
        value=0,
        read_only=True,
        record='longin',
        units='',
        doc='Calibration alarm',
        alarm_group='cal_alarm',
    )

    flow_alarm = pvproperty(
        name='FlowAlarm',
        value=0,
        read_only=True,
        record='longin',
        units='',
        doc='Flow alarm',
        alarm_group='flow_alarm',
    )

    over_conc_alarm = pvproperty(
        name='OverConcAlarm',
        value=0,
        read_only=True,
        record='longin',
        units='',
        doc='Over concentration alarm',
        alarm_group='over_conc_alarm',
    )

    system_alarm = pvproperty(
        name='SystemAlarm',
        value=0,
        read_only=True,
        record='longin',
        units='',
        doc='System alarm',
        alarm_group='system_alarm',
    )

    count_alarm = pvproperty(
        name='CountAlarm',
        value=0,
        read_only=True,
        record='longin',
        units='',
        doc='Count alarm',
        alarm_group='count_alarm',
    )

    battery_alarm = pvproperty(
        name='BatteryAlarm',
        value=0,
        read_only=True,
        record='longin',
        units='',
        doc='Battery alarm',
        alarm_group='battery_alarm',
    )

    laser_alarm = pvproperty(
        name='LaserAlarm',
        value=0,
        read_only=True,
        record='longin',
        units='',
        doc='Laser alarm',
        alarm_group='laser_alarm',
    )

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
        # Sample Units
        # Sample Period
        # overall_alarm (custom)
    }

    async def _write_metadata(self,
                              pvprop: pvproperty,
                              value: str,
                              timestamp: float):
        """
        Update the metadata, if changed.
        """
        value = value[:pvprop.max_length]
        if pvprop.value != value:
            await pvprop.write(value=value, timestamp=timestamp)

    async def _query_server_state(self):
        state_info = await comm.check_state(host=self.host.value,
                                            port=self.port.value)
        records = state_info.get('records')
        if records is not None:
            await self.num_records.write(value=records)

        state = state_info.get('state')
        if state is not None:
            await self.server_state.write(value=state)

    async def _query_data_file(self):
        data_text = await comm.get_data_file(host=self.host.value,
                                             port=self.port.value)
        strio = io.StringIO(data_text)
        return data.load_fluke_data_file(strio)

    update_hook = pvproperty(
        value=0,
        name='__update_hook__',
        read_only=True
    )

    @update_hook.startup
    async def update_hook(self, instance, async_lib):
        try:
            await self._query_server_state()
            metadata, df = await self._query_data_file()
        except Exception:
            for key, alarm in self.alarms.items():
                if key is not None:
                    await alarm.write(
                        status=AlarmStatus.COMM,
                        severity=AlarmSeverity.MAJOR_ALARM,
                    )
            return

        timestamp = time.time()
        for key, pvprop in self._metadata_to_property.items():
            await self._write_metadata(
                pvprop=getattr(self, pvprop.attr_name),
                value=metadata.get(key, 'unknown'),
                timestamp=timestamp,
            )

        timestamp, row = list(df.tail().iterrows())[-1]

        try:
            alarm_summary = data.summarize_alarms(row)
            await self.overall_alarm.write(value=alarm_summary,
                                           timestamp=timestamp)
        except Exception as ex:
            self.log.exception('Failed to update overall alarm: %s', ex)
            alarm_summary = 1

        if alarm_summary:
            status, severity = (AlarmStatus.READ, AlarmSeverity.MAJOR_ALARM)
        else:
            status, severity = (AlarmStatus.NO_ALARM, AlarmSeverity.NO_ALARM)

        for key, value in row.items():
            try:
                prop = self._data_key_to_property[key]
            except KeyError:
                continue

            prop = getattr(self, prop.attr_name)
            try:
                await prop.write(value=value, timestamp=timestamp,
                                 status=status,
                                 severity=severity)
            except Exception as ex:
                self.log.exception('Failed to update key %s=%s: %s', key,
                                   value, ex)

        try:
            units = row['Sample Units']
        except KeyError:
            self.log.exception('Sample Units unavailable?')
        else:
            await self.sample_volume.write_metadata(units=units)
            await self.sample_volume.field_inst.engineering_units.write(
                value=value)

        try:
            await self.sample_period.write(
                value=data.sample_period_to_seconds(row['Sample Period']),
                timestamp=timestamp,
            )
        except Exception as ex:
            self.log.exception('Failed to update sample period: %s', ex)

        # TODO: caproto alarm handling needs some work
        # await self.alarms['reading'].write(
        #     severity=severity,
        #     status=status,
        #     publish=True,
        #     # alarm_string='One or more alarms tripped',
        # )

        # TODO:
        # and optional e-mail?


def create_ioc(prefix: str, *,
               host: str,
               autosave: str,
               **ioc_options) -> Fluke985Base:
    """
    Create a new Fluke 985 IOC.

    Parameters
    ----------
    prefix : str
        The IOC prefix.

    host : str
        IP or hostname of the Fluke 985 to connect to.

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
        host=host,
        **ioc_options
    )


def create_parser():
    parser, split_args = template_arg_parser(
        default_prefix='TEST:FLUKE:985:',
        desc='Fluke 985 particle counter IOC',
        supported_async_libs=('asyncio', )
    )

    parser.add_argument(
        '--host',
        help='Hostname or IP of the Fluke 985',
        required=True,
        type=str
    )

    parser.add_argument(
        '--port',
        help='Port to connect to (mostly for debugging)',
        default=80,
        type=int
    )

    parser.add_argument(
        '--autosave',
        help='Path to the autosave file',
        default='autosave.json',
        type=str
    )
    return parser, split_args


def main():
    parser, split_args = create_parser()
    args = parser.parse_args()
    ioc_options, run_options = split_args(args)

    ioc = create_ioc(
        autosave=args.autosave,
        host=(args.host, args.port),
        **ioc_options
    )
    if args.verbose is None or args.verbose == 0:
        log_level = 'INFO'
    else:
        log_level = 'DEBUG'

    util.config_logging(ioc.log, level=log_level)
    run(ioc.pvdb, **run_options)


if __name__ == '__main__':
    main()
