import requests

import whatsapp


class DummyResponse:
    def __init__(self, status_code=200, payload=None):
        self.status_code = status_code
        self._payload = payload if payload is not None else {}

    def json(self):
        if self._payload is None:
            raise ValueError("no json")
        return self._payload


def test_bridge_unreachable_reports_not_running(monkeypatch):
    def fake_get(url, headers=None, timeout=None):
        raise requests.ConnectionError("connection refused")

    monkeypatch.setattr(whatsapp.requests, "get", fake_get)

    status = whatsapp.get_bridge_status()

    assert status["bridge_running"] is False
    assert status["connected"] is False
    assert "unreachable" in status["error"]
    assert "hint" in status


def test_connected_bridge_reports_healthy(monkeypatch):
    def fake_get(url, headers=None, timeout=None):
        return DummyResponse(200, {"status": "ok", "connected": True, "timestamp": 123})

    monkeypatch.setattr(whatsapp.requests, "get", fake_get)

    status = whatsapp.get_bridge_status()

    assert status == {
        "bridge_running": True,
        "connected": True,
        "status": "ok",
        "timestamp": 123,
    }


def test_client_outdated_surfaces_reason_and_hint(monkeypatch):
    payload = {
        "status": "disconnected",
        "connected": False,
        "reason": "client outdated (405) — update the whatsmeow dependency and rebuild the bridge",
        "client_outdated": True,
    }

    def fake_get(url, headers=None, timeout=None):
        return DummyResponse(503, payload)

    monkeypatch.setattr(whatsapp.requests, "get", fake_get)

    status = whatsapp.get_bridge_status()

    assert status["bridge_running"] is True
    assert status["connected"] is False
    assert status["client_outdated"] is True
    assert "whatsmeow" in status["hint"]


def test_logged_out_surfaces_hint(monkeypatch):
    payload = {
        "status": "disconnected",
        "connected": False,
        "reason": "device logged out — delete whatsapp.db and re-scan the QR code",
        "logged_out": True,
    }

    def fake_get(url, headers=None, timeout=None):
        return DummyResponse(503, payload)

    monkeypatch.setattr(whatsapp.requests, "get", fake_get)

    status = whatsapp.get_bridge_status()

    assert status["logged_out"] is True
    assert "QR code" in status["hint"]


def test_auth_failure_reports_stale_token(monkeypatch):
    def fake_get(url, headers=None, timeout=None):
        return DummyResponse(401, None)

    monkeypatch.setattr(whatsapp.requests, "get", fake_get)

    status = whatsapp.get_bridge_status()

    assert status["bridge_running"] is True
    assert status["connected"] is False
    assert "401" in status["error"]


def test_malformed_health_response(monkeypatch):
    class BadJSON:
        status_code = 200

        def json(self):
            raise ValueError("not json")

    def fake_get(url, headers=None, timeout=None):
        return BadJSON()

    monkeypatch.setattr(whatsapp.requests, "get", fake_get)

    status = whatsapp.get_bridge_status()

    assert status["bridge_running"] is True
    assert status["connected"] is False
    assert "malformed" in status["error"]
