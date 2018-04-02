class Manager(object):
    def __init__(self, wrapper):
        self.wrapper = wrapper

    def __str__(self):
        title = self.__class__.__name__
        content = str(self.wrapper)
        return '\n'.join((title, content))
