from core.utils import CallableMixin


class ManagerFunctionHandler(CallableMixin):
    def __init__(self, manager):
        self.manager = manager

    def __call__(self, *args, **kwargs):
        self.function(*args, **kwargs)

    def function(self, *args, **kwargs):
        raise NotImplementedError
