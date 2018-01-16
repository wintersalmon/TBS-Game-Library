class CallableMixin(object):
    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class Serializable(object):
    def encode(self):
        raise NotImplementedError

    @classmethod
    def decode(cls, **kwargs):
        raise NotImplementedError


class ImmutableObject(object):
    __slots__ = ()
