class LinearHandle:
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

def demonstrate():
    packet = LinearHandle(bytearray(b"21"))
    assert packet.borrow() == bytearray(b"21")
    owned = packet.consume()
    result = int(owned.decode()) * 2
    owned.clear()
    try:
        packet.consume()
    except RuntimeError as exc:
        assert str(exc) == "double consume"
    else:
        raise AssertionError("linear resource was consumed twice")
    print(result)

if __name__ == "__main__":
    demonstrate()