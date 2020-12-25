import math

from functools import partial
from inspect import signature


class Curry(object):
    
    def __init__(self, func):
        self.func = func
        self.argc = len(signature(self.func).parameters)
        self.resolved = False
        self.answer = None

    def __call__(self, *args):
        if len(args) == self.argc:
            self.answer = self.func(*args)
            self.resolved = True

        for arg in args:
            self.func = partial(self.func, arg)
            self.argc = len(signature(self.func).parameters)

        return self


class RPNEngine(object):
   
    def __init__(self):
        self.stack = []
        self.functions = self._get_functions()

    def _get_functions(self):
        return {
            '+' or 'add': Curry(lambda x, y: x + y),
            '-' or 'sub': Curry(lambda x, y: x - y),
            '*' or 'mul': Curry(lambda x, y: x * y),
            '/' or 'div': Curry(lambda x, y: x / y)
        }

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        try:
            return self.stack.pop()
        except IndexError:
            pass

    def compute(self, operation):
        func = self.functions.get(operation)

        if not func:
            raise BaseException('%s not a valid function' % operation)

        if len(self.stack) < func.argc:
            raise BaseException(
                '%s requires %d operands, %d given' % (
                    operation,
                    func.argc,
                    len(self.stack)
                )
            )

        if func.argc == 0:
            func()

        while not func.resolved:
            func(self.pop())

        return func.answer