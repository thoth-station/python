class Lazy(object):
    """Calculates function exactly once then sets it to be and attribute of object.

    Intended to optimize cases in which a class function is called and does not change
    after repeated calls. Attribute lookup is ~2x as fast as even the simples function
    calls.
    """

    def __init__(self, calculate_function):
        """Create lazy function."""
        self._calculate = calculate_function

    def __get__(self, obj, _=None):
        """Call function and set obj.func_name to value."""
        if obj is None:
            return self
        value = self._calculate(obj)
        setattr(obj, self._calculate.__name__, value)
        return value
