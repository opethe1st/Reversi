
class _member_table(dict):
    def __init__(self):
        self.ALL = set()

    def __setitem__(self, key, value):
        if key.isupper():
            self.ALL.add(value)
        dict.__setitem__(self, key, value)


class _EnumMeta(type):

    @classmethod
    def __prepare__(metacls, name, bases):
        return _member_table()

    def __new__(cls, name, bases, classdict):
        result = type.__new__(cls, name, bases, dict(classdict))
        result.ALL = classdict.ALL
        for base in bases:
            # Update with ALL from the super classes.
            if issubclass(base, Enum) and getattr(base, 'ALL'):
                result.ALL |= getattr(base, 'ALL')
        return result


class Enum(metaclass=_EnumMeta):
    pass
