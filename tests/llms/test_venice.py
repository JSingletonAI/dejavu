import pytest

from dejavu.configs.llms.venice import VeniceConfig
from dejavu.llms.venice import VeniceLLM, _drop_nulls


def test_drop_nulls_removes_nested_none():
    payload = {'a': None, 'b': {'c': None, 'd': 1}, 'e': [None, {'x': None, 'y': 2}]}
    assert _drop_nulls(payload) == {'b': {'d': 1}, 'e': [None, {'y': 2}]}


def test_venice_requires_api_key(monkeypatch):
    monkeypatch.delenv('VENICE_API_KEY', raising=False)
    with pytest.raises(ValueError):
        VeniceLLM(VeniceConfig(api_key=None))
