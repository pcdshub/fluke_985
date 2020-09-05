import functools
import sys
import typing

import caproto
import caproto._log as caproto_log
import caproto.threading

_default_thread_context = None


def config_logging(logger, file=sys.stdout, datefmt='%H:%M:%S', color=True,
                   level='WARNING'):
    """
    Add a new handler to the logger.

    Parameters
    ----------
    logger : logging.Logger
        The logger to configure.

    file : object with ``write`` method or filename string
        Default is ``sys.stdout``.

    datefmt : string
        Date format. Default is ``'%H:%M:%S'``.

    color : boolean
        Use ANSI color codes. True by default.

    level : str or int
        Python logging level, given as string or corresponding integer.
        Default is 'WARNING'.

    Examples
    --------
    Log to a file.

    >>> config_logging(file='/tmp/what_is_happening.txt')

    Include the date along with the time. (The log messages will always include
    microseconds, which are configured separately, not as part of 'datefmt'.)

    >>> config_logging(datefmt="%Y-%m-%d %H:%M:%S")

    Turn off ANSI color codes.

    >>> config_logging(color=False)

    Increase verbosity: show level INFO or higher.

    >>> config_logging(level='INFO')
    """
    caproto_log._set_handler_with_logger(logger_name=logger.name,
                                         file=file, datefmt=datefmt,
                                         color=color, level=level)


def process_writes_value(pvprop: caproto.server.pvproperty, *,
                         value: typing.Any = None):
    """
    When `.PROC` is changed, write the value `value` to the pvproperty.

    Parameters
    ----------
    pvprop : caproto.server.pvproperty
        The property.

    value : any
        The value to write upon processing.  If `None`, defaults to re-writing
        the current value of `pvprop`.
    """

    async def wrapped(fields, instance, proc_value, *, value_to_write=value):
        pvprop_instance = fields.parent
        if value_to_write is None:
            value_to_write = pvprop_instance.value
        await pvprop_instance.write(value_to_write)

    pvprop.fields.process_record.putter(wrapped)


def block_on_reentry(token=None):
    """
    [Decorator] If an asynchronous handler is called multiple times, block.

    Requires that a dictionary `self._context` be available for usage, where
    the Lock will be stored with the provided token.

    Also requires `self.async_lib` to exist.

    Parameters
    ----------
    token : str, optional
        Defaults to the wrapped method name if not provided.
    """

    def inner(func):
        @functools.wraps(func)
        async def wrapped(self, *args, **kwargs):
            key = token or func.__name__
            if key not in self._context:
                self._context[key] = self.async_lib.library.Lock()

            lock = self._context[key]
            async with lock:
                return await func(self, *args, **kwargs)

        return wrapped

    return inner
