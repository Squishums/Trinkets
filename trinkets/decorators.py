"""
Contains decorators which apply to standard methods.
"""

############################################################################### imports
import inspect
import functools

import trinkets.log


############################################################################### utils
def _allow_no_args_call(deco):
  """
  Decorates a decorator to allow it to be called either with or without arguments.

  The decorated decorator should take the method its wrapping as the first
  parameter, followed by any decorator parameters.

  Example:
    Creating an annotation which hides exceptions and can provide an optional
    return value.

      @_allow_no_args_call
      def no_exceptions(fn, *, default_return=None):
        def wrapped(*args, **kwargs):
          try:
            fn(*args, **kwargs)
          except Exception:
            return default_return

      @no_exceptions
      def some_method(...):  # Exceptions return None
        ...

      @no_exceptions(default_return='uh oh!')
      def some_method(...):  # Exceptions return 'uh oh!'
        ...

  """
  @functools.wraps(deco)
  def wrapped(*args, **kwargs):
    if (len(args) == 1 and len(kwargs == 0) and callable(args[0])):
      # Signature matches what we'd recieve if deco was called without
      # arguments. It's possible this is incorrect, if it was passed a single
      # callable as an argument.
      return deco(args[0])
    else:
      # Decorated decorator was passed arguments. Forward them.
      return lambda deco_inner: deco(deco_inner, *args, **kwargs)
  return wrapped


###############################################################################
def overrides(interface_class):
  """
  Indicates that a method overrides an implementation in a base class.

  Requires that there exists a callable defined with the same name in the
  class hierarchy of interface_class.

  Args:
    interface_class (class): base class with the method definition

  Raises:
    TypeError: if the decorated method is not present in the interface_class
  """
  if (not inspect.isclass(interface_class)):
    raise TypeError(f'Must specify a class')

  # TODO: Ensure interface_class is a subclass of the passed method, or
  #       inspect base classes of interface_class directly

  def wrapped(method):
    # Check that the method exists in the interface
    method_name = method.__name__
    qualified_method_name = f'{interface_class.__name__}.{method.__name__}'
    try:
      interface_method = getattr(interface_class, method.__name__)
      if (not callable(interface_method)):
        raise TypeError(f'{qualified_method_name} is not callable.')
    except AttributeError:
      raise TypeError(f'Method {qualified_method_name} not found.')
    return method
  return wrapped


############################################################################### builder
class Builder:
  METHOD_PATTERN = 'with_'

  def __init__(self, cls):
    self._cls = cls
    self._argpack = {}

  def __getattr__(self, attr):
    if (attr.startswith(self.METHOD_PATTERN)):
      # Requested a builder attribute setter
      var_name = attr[len(self.METHOD_PATTERN):]
      def with_value(val):
        self._argpack[var_name] = val
        return self
      return with_value

  def build(self):
    return self._cls(**self._argpack)


def builder(cls):
  def builder():
    """
    Creates a class builder instance which allows for fluent object building.
    """
    return Builder(cls)
  cls.builder = builder
  return cls


############################################################################### retries
@_allow_no_args_call
def retries(
    func,
    *,
    return_filter=None,
    exception_filter=None,
    attempt_filter=None,
    delay_strategy=None):
  """
  Decorates a method to retry failed execution attempts.

  When no arguments are passed, retries
  """
  @functools.wraps(func)
  def wrapped(*args, **kwargs):

    return func(*args, **kwargs)
  return wrapped