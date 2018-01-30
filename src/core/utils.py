class CallableMixin(object):
    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class SerializableMixin(object):
    def encode(self):
        raise NotImplementedError

    @classmethod
    def decode(cls, **kwargs):
        raise NotImplementedError


class ImmutableMixin(object):
    __slots__ = ()
