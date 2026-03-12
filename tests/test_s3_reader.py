import pytest

from botocore.exceptions import ClientError, BotoCoreError

import s3_reader


class DummyBody:
    def __init__(self, data: bytes):
        self._data = data

    def read(self) -> bytes:
        return self._data


def test_read_s3_bytes_success(monkeypatch):
    """read_s3_bytes should return raw bytes from object body"""

    def fake_client(region=None, profile=None):
        class C:
            def get_object(self, Bucket, Key):
                return {"Body": DummyBody(b"binary-data")}

        return C()

    monkeypatch.setattr(s3_reader, "_s3_client", fake_client)
    res = s3_reader.read_s3_bytes("bucket", "key")
    assert res == b"binary-data"


def test_read_s3_text_success(monkeypatch):
    """read_s3_text should decode bytes to str using utf-8 by default"""

    def fake_client(region=None, profile=None):
        class C:
            def get_object(self, Bucket, Key):
                return {"Body": DummyBody("hello world".encode("utf-8"))}

        return C()

    monkeypatch.setattr(s3_reader, "_s3_client", fake_client)
    text = s3_reader.read_s3_text("bucket", "key")
    assert text == "hello world"


def test_read_s3_bytes_raises_client_error(monkeypatch):
    """ClientError from boto3 should be propagated"""

    def fake_client(region=None, profile=None):
        class C:
            def get_object(self, Bucket, Key):
                raise ClientError({"Error": {"Code": "NoSuchKey"}}, "GetObject")

        return C()

    monkeypatch.setattr(s3_reader, "_s3_client", fake_client)
    with pytest.raises(ClientError):
        s3_reader.read_s3_bytes("bucket", "key")


def test_read_s3_bytes_raises_botocore_error(monkeypatch):
    """BotoCoreError from boto3 should be propagated"""

    def fake_client(region=None, profile=None):
        class C:
            def get_object(self, Bucket, Key):
                raise BotoCoreError()

        return C()

    monkeypatch.setattr(s3_reader, "_s3_client", fake_client)
    with pytest.raises(BotoCoreError):
        s3_reader.read_s3_bytes("bucket", "key")
