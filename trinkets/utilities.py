############################################################################### imports
import inspect
import os
import sys

import trinkets.log


############################################################################### config
logger = trinkets.log.getLogger(__name__)


###############################################################################
def defaultarg(arg, default):
  """
  Returns default, if arg is None.

  Facilitates using None as a default argument value by reducing the
  assign-then-check-null paradigm to a single assignment.

  Example:
    def method(self, optional=None):
      self.optional = optionalarg(optional, DEFAULT_VALUE)

  """
  if (arg is None):
    return default
  return arg


############################################################################### file system
def script_dir(backstep=None):
  """
  Returns the directory in which the code of the caller of this method is located.

  Args:
    backstep (int, optional): Number of frames to backtrack. Defaults to 1
  """
  # Not sure if there are cases where the filename can be blank, but I suspect
  # so, so find the first non-blank filename
  backstep = defaultarg(backstep, 1)
  stack = inspect.stack()
  filename = next(
    (frame.filename for frame in stack[backstep:] if frame.filename),
    None)

  return os.path.dirname(filename)


def open_script_resource(filename, *args, **kwargs):
  """
  Opens a file relative to the directory of the caller.
  """
  caller_dir = script_dir(backstep=2)
  abs_path = os.path.normpath(os.path.join(caller_dir, filename))
  return open(abs_path, *args, **kwargs)


def add_package_dir(path):
  """
  Adds a path to the package resolution paths.

  The path can be absolute or relative to the script directory of the caller

  Args:
    path (str): path to make available for imports
  """
  # Ensure we're adding an absolute path
  abs_path = path
  if (not os.path.isabs(abs_path)):
    caller_dir = script_dir(backstep=2)
    abs_path = os.path.join(caller_dir, abs_path)
    abs_path = os.path.normpath(abs_path)

  logger.info('Adding {} to the path', abs_path)
  sys.path.insert(0, abs_path)