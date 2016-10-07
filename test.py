class Pop(object):
    @classmethod
    def foo(cls):
        print cls.__class__

class A(Pop):
    pass

class B(Pop):
    pass

print A.foo()
print B.foo()
