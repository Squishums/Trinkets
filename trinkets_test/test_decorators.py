############################################################################### imports
from trinkets import builder
from trinkets import overrides

import pytest

import trinkets


############################################################################### overrides
class TestOverrides:
  def test_base_method_in_interface(self):
    # Setup
    class A:
      def a(): pass

    # Invoke
    class B(A):
      @overrides(A)
      def a(): pass

  def test_base_method_in_subclass(self):
    # Setup
    class A:
      def a(): pass

    class B(A):
      pass

    # Invoke
    class C(B):
      @overrides(B)
      def a(): pass

  def test_base_method_missing(self):
      # Setup
      class A:
        pass

      # Invoke
      with pytest.raises(TypeError):
        class B(A):
          @overrides
          def a(): pass

  def test_base_method_not_method(self):
    # Setup
    class A:
      a = 3

    # Invoke
    with pytest.raises(TypeError):
      class B:
        @overrides
        def a(): pass

  def test_interface_missing(self):
    # Setup

    # Invoke
    with pytest.raises(TypeError):
      class B:
        @overrides
        def a(): pass


############################################################################### builder
class TestBuilder:
  GENERATED_CLASS_NAME = 'gen_class'

  def make_builder(self, init):
    cls = type(self.GENERATED_CLASS_NAME, (object,), {'__init__': init})
    return builder(cls).builder()

  def test_no_args(self):
    # Setup
    val_a = 'some_data'
    def __init__(self):
      self.a = val_a

    # Invoke
    a = (self.make_builder(__init__)
      .build())

    # Verify
    assert a.a == val_a
    assert type(a).__name__ == self.GENERATED_CLASS_NAME

  def test_none_arg(self):
    # Setup
    val_a = None
    def __init__(self, a):
      self.a = a

    # Invoke
    a = (self.make_builder(__init__)
      .with_a(val_a)
      .build())

    # Verify
    assert a.a == val_a
    assert type(a).__name__ == self.GENERATED_CLASS_NAME

  def test_positional_args(self):
    # Setup
    val_a = 'some_data_a'
    val_b = 'some_data_b'
    val_c = 'some_data_c'
    def __init__(self, a, b, c):
      self.a = a
      self.b = b
      self.c = c

    # Invoke
    a = (self.make_builder(__init__)
      .with_a(val_a)
      .with_b(val_b)
      .with_c(val_c)
      .build())

    # Verify
    assert a.a == val_a
    assert a.b == val_b
    assert a.c == val_c
    assert type(a).__name__ == self.GENERATED_CLASS_NAME

  def test_kwargs(self):
    # Setup
    val_a = 'some_data_a'
    val_b = 'some_data_b'
    val_c = 'some_data_c'
    def __init__(self, *, a, b, c):
      self.a = a
      self.b = b
      self.c = c

    # Invoke
    a = (self.make_builder(__init__)
      .with_a(val_a)
      .with_b(val_b)
      .with_c(val_c)
      .build())

    # Verify
    assert a.a == val_a
    assert a.b == val_b
    assert a.c == val_c
    assert type(a).__name__ == self.GENERATED_CLASS_NAME

  def test_default_arg(self):
    # Setup
    val_a = 'some_data_a'
    def __init__(self, a=val_a):
      self.a = a

    # Invoke
    a = (self.make_builder(__init__)
      .build())

    # Verify
    assert a.a == val_a
    assert type(a).__name__ == self.GENERATED_CLASS_NAME

  def test_default_arg_set(self):
    # Setup
    val_a = 'some_data_a'
    def __init__(self, a='INVALID'):
      self.a = a

    # Invoke
    a = (self.make_builder(__init__)
      .with_a(val_a)
      .build())

    # Verify
    assert a.a == val_a
    assert type(a).__name__ == self.GENERATED_CLASS_NAME

  def test_mixed_args(self):
    # Setup
    val_a = 'some_data_a'
    val_b = None
    val_c = {'complex': 322}
    def __init__(self, a, b=val_b, *, c):
      self.a = a
      self.b = b
      self.c = c

    # Invoke
    a = (self.make_builder(__init__)
      .with_a(val_a)
      .with_c(val_c)
      .build())

    # Verify
    assert a.a == val_a
    assert a.b == val_b
    assert a.c == val_c
    assert type(a).__name__ == self.GENERATED_CLASS_NAME

  def test_missing_arg(self):
    # Setup
    def __init__(self, a):
      self.a = a

    # Invoke
    with pytest.raises(TypeError):
      a = (self.make_builder(__init__)
        .build())

  def test_extra_arg(self):
    # Setup
    val_a = 'some_data_a'
    val_b = 'some_data_b'
    def __init__(self, a):
      self.a = a

    # Invoke
    with pytest.raises(TypeError):
      (self.make_builder(__init__)
        .with_a(val_a)
        .with_b(val_b)
        .build())

  def test_arg_redefined(self):
    # Setup
    val_a = 'some_data_a'
    def __init__(self, a):
      self.a = a

    # Invoke
    a = (self.make_builder(__init__)
      .with_a('INVALID')
      .with_a(val_a)
      .build())

    # Verify
    assert a.a == val_a
    assert type(a).__name__ == self.GENERATED_CLASS_NAME



if __name__ == '__main__':
  pytest.main(args=['-s'])