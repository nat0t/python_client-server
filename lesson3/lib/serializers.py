import json


class JSONSerializer:
    @staticmethod
    def pack(data: dict) -> bytes:
        """Pack the data for send over the network."""

        return json.dumps(data).encode('utf-8')

    @staticmethod
    def unpack(data: bytes) -> dict:
        """Unpack the received data."""

        return json.loads(data.decode('utf-8'))
