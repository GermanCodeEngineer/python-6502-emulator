"""M6502 Module."""
from .main import *

class Memory(object):
    def __init__(self, *args, **kwargs):
        self.__CORE__ = M___init__(*args, **kwargs)
    def __getattr__(self, name):
        if name in self.__CORE__:
            return self.__CORE__[name]
        try:
            func = eval("M_" + name)
        except NameError:
            raise Exception("NOT FOUND", name)
        else:
            return lambda *args, **kwargs: (
                func(self.__CORE__, *args, **kwargs)
            )
    def __setitem__(self, name, value):
        self.__CORE__ = M___setitem__(self.__CORE__, name, value)
    def __getitem__(self, name):
        return M___getitem__(self.__CORE__, name)

class Processor(object):
    def __init__(self, *args, **kwargs):
        super().__setattr__("__CORE__", P___init__(*args, **kwargs))
    def __getattr__(self, name):
        if name in self.__CORE__:
            return self.__CORE__[name]
        try:
            func = eval("P_" + name)
        except NameError:
            raise Exception("NOT FOUND", name)
        else:
            return lambda *args, **kwargs: (
                func(self.__CORE__, *args, **kwargs)
            )
    #def __setattr__(self, name, value):
    #    self.__CORE__[name] = value
    