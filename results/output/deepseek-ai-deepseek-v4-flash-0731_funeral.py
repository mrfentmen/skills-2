class LinearResource:
    def __init__(self, value):
        self._value = value
        self._live = True

    def borrow(self):
        if not self._live:
            raise RuntimeError("use after consume")
        return self._value

    def consume(self):
        if not self._live:
            raise RuntimeError("double consume")
        value, self._value = self._value, None
        self._live = False
        return value

resource = LinearResource("precious")
assert resource.borrow() == "precious"
owned = resource.consume()
result = len(owned) * 2
try:
    resource.consume()
except RuntimeError as exc:
    assert str(exc) == "double consume"
else:
    raise AssertionError("resource was consumed twice")
try:
    resource.borrow()
except RuntimeError as exc:
    assert str(exc) == "use after consume"
else:
    raise AssertionError("borrow after consume accepted")
print(result)