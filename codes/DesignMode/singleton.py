#decorator

def outter(cls):
    _instance = {}
    def inner():
        if not _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner

@outter
class Singleton(object):
    pass

a = Singleton()    
b = Singleton()    
print(a, b, a is b)

class Singleton2(object):
    __instance=None
    def __init__(self):
        pass
        
    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

a = Singleton2()    
b = Singleton2()    
print(a, b, a is b)

class Singleton3(type):
    _instance = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(Singleton3, cls).__call__(*args, **kwargs)
        return cls._instance[cls]

class A(metaclass=Singleton3):
    pass

a= A()    
b= A()    
print(a, b, a is b)        