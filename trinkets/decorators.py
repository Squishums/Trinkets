"""
Contains decorators which apply to standard methods.
"""

############################################################################### imports
import inspect

import trinkets.log


###############################################################################
def overrides(interface_class):
  """
  Indicates that a method overrides an implementation in a base class.

  Requires that there exists a callable defined with the same name in the
  class hierarchy of interface_class.

  Args:
    interface_class: (class) base class with the method definition

  Raises:
    TypeError: if the decorated method is not present in the interface_class
  """
  if (not inspect.isclass(interface_class)):
    raise TypeError(f'Must specify a class')

  # TODO: Ensure interface_class is a subclass of the passed method, or
  #       inspect base classes of interface_class directly

  def decorator(method):
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
  return decorator


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


if __name__ == '__main__':
  @builder
  class Test:
    def __init__(self, a):
      print(a)

  (Test.builder()
    .with_a(3)
    .build())

