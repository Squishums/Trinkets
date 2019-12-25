"""
Provides a simple logging implementation with pre-defined output

Allows logging messages to use parentheses style string formats, but loggers
must be acquired through the getLogger method defined in this module.

Example:
  import trinkets

  trinkets.getLogger(__name__)

  trinkets.init_logging()

"""
############################################################################### imports
import collections
import inspect
import logging
import sys

from logging import CRITICAL
from logging import ERROR
from logging import WARNING
from logging import INFO
from logging import DEBUG
from logging import NOTSET

############################################################################### logger
def getLogger(*args, **kwargs):
  """
  Returns a LoggerAdapter, which allows for braced formatting.

  Direct logging methods are wrapped, but manipulation of the Logger object
  itself should be done through the adapter's logger property.
  """
  return StyleAdapter(logging.getLogger(*args, **kwargs))


############################################################################### adapter
class BraceMessage(object):
  def __init__(self, fmt, args, kwargs):
    self.fmt = fmt
    self.args = args
    self.kwargs = kwargs

  def __str__(self):
    return str(self.fmt).format(*self.args, **self.kwargs)


class StyleAdapter(logging.LoggerAdapter):
  def __init__(self, logger):
    self.logger = logger

  def log(self, level, msg, *args, **kwargs):
    if self.isEnabledFor(level):
      msg, log_kwargs = self.process(msg, kwargs)
      self.logger._log(
        level,
        BraceMessage(msg, args, kwargs), (), **log_kwargs)

  @staticmethod
  def __make_curry(level, **kwargs2):
    def curry(self, msg, *args, **kwargs):
      kwargs3 = kwargs2.copy()
      kwargs3.update(kwargs)
      self.log(level, msg, *args, **kwargs3)
    return curry

  # Hack for weird issue where methods weren't forwarding to the StyleAdapter's
  # log(...) method. Forcing it like this seems to work.
  critical  = __make_curry.__func__(CRITICAL)
  error     = __make_curry.__func__(ERROR)
  warning   = __make_curry.__func__(WARNING)
  info      = __make_curry.__func__(INFO)
  debug     = __make_curry.__func__(DEBUG)
  exception = __make_curry.__func__(ERROR, exc_info=1)

  def process(self, msg, kwargs):
    return (
      msg,
      {
        key: kwargs[key]
        for key in inspect.getfullargspec(self.logger._log).args[1:]
        if key in kwargs
      })


###############################################################################
def init_logging(level=None):
  """
  Initializes the logging system.

  Adds a single console handler. Particularly useful for small scripts which
  want logging, but don't want to handle initialization.

  Args:
    level (int): Logging level, as defined in the logging module.
      Defaults to INFO
  """
  if (level is None):
    level = INFO

  logger = logging.getLogger()

  logger.setLevel(level)
  # Console
  console = logging.StreamHandler()
  console.setLevel(level)
  console.setFormatter(logging.Formatter(
    '%(asctime)s - [%(name)20.20s] <%(levelname)8s> - %(message)s'))
  logger.addHandler(console)


def disable_module_logger(name):
  """
  Sets a third party logger to only show errors.
  """
  logging.getLogger(name).setLevel(ERROR)