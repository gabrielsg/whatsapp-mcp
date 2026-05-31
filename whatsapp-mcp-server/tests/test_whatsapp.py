"""Tests for WhatsApp MCP server functions."""

from datetime import datetime
from unittest.mock import MagicMock, patch

from whatsapp import Chat, Contact, Message, chat_to_dict, contact_to_dict, msg_to_dict
from whatsapp import _sender_aliases
from whatsapp import _resolve_lid_to_phone


class TestMessageConversion:
    """Tests for message conversion functions."""

    def test_msg_to_dict_basic(self):
        """Test basic message to dict conversion."""
        msg = Message(
            id="msg123",
            timestamp=datetime(2024, 1, 15, 10, 30, 0),
            sender="1234567890@s.whatsapp.net",
            content="Hello, world!",
            is_from_me=False,
            chat_jid="1234567890@s.whatsapp.net",
            chat_name="John Doe",
            media_type=None,
        )

        result = msg_to_dict(msg, include_sender_name=False)

        assert result["id"] == "msg123"
        assert result["timestamp"] == "2024-01-15T10:30:00"
        assert result["sender_jid"] == "1234567890@s.whatsapp.net"
        assert result["sender_phone"] == "1234567890"
        assert result["content"] == "Hello, world!"
        assert result["is_from_me"] is False
        assert result["chat_jid"] == "1234567890@s.whatsapp.net"
        assert result["chat_name"] == "John Doe"
        assert result["media_type"] is None

    def test_msg_to_dict_from_me(self):
        """Test message from self shows 'Me' as sender."""
        msg = Message(
            id="msg456",
            timestamp=datetime(2024, 1, 15, 10, 30, 0),
            sender="me@s.whatsapp.net",
            content="My message",
            is_from_me=True,
            chat_jid="1234567890@s.whatsapp.net",
        )

        result = msg_to_dict(msg, include_sender_name=True)

        assert result["sender_name"] == "Me"
        assert result["sender_display"] == "Me"

    def test_msg_to_dict_with_media(self):
        """Test message with media type."""
        msg = Message(
            id="msg789",
            timestamp=datetime(2024, 1, 15, 10, 30, 0),
            sender="1234567890@s.whatsapp.net",
            content="",
            is_from_me=False,
            chat_jid="1234567890@s.whatsapp.net",
            media_type="image",
        )

        result = msg_to_dict(msg, include_sender_name=False)

        assert result["media_type"] == "image"


class TestChatConversion:
    """Tests for chat conversion functions."""

    def test_chat_to_dict_dm(self):
        """Test direct message chat conversion."""
        chat = Chat(
            jid="1234567890@s.whatsapp.net",
            name="John Doe",
            last_message_time=datetime(2024, 1, 15, 10, 30, 0),
            last_message="Hello!",
            last_sender="1234567890@s.whatsapp.net",
            last_is_from_me=False,
        )

        result = chat_to_dict(chat)

        assert result["jid"] == "1234567890@s.whatsapp.net"
        assert result["name"] == "John Doe"
        assert result["is_group"] is False
        assert result["last_message_time"] == "2024-01-15T10:30:00"
        assert result["last_message"] == "Hello!"

    def test_chat_to_dict_group(self):
        """Test group chat conversion."""
        chat = Chat(
            jid="123456789@g.us",
            name="Family Group",
            last_message_time=datetime(2024, 1, 15, 10, 30, 0),
        )

        result = chat_to_dict(chat)

        assert result["jid"] == "123456789@g.us"
        assert result["is_group"] is True

    def test_chat_to_dict_no_last_message(self):
        """Test chat without last message time."""
        chat = Chat(
            jid="1234567890@s.whatsapp.net",
            name="Jane Doe",
            last_message_time=None,
        )

        result = chat_to_dict(chat)

        assert result["last_message_time"] is None


class TestContactConversion:
    """Tests for contact conversion functions."""

    def test_contact_to_dict(self):
        """Test contact to dict conversion."""
        contact = Contact(
            phone_number="1234567890",
            name="John Doe",
            jid="1234567890@s.whatsapp.net",
        )

        result = contact_to_dict(contact)

        assert result["phone_number"] == "1234567890"
        assert result["name"] == "John Doe"
        assert result["jid"] == "1234567890@s.whatsapp.net"

    def test_contact_to_dict_no_name(self):
        """Test contact without name."""
        contact = Contact(
            phone_number="9876543210",
            name=None,
            jid="9876543210@s.whatsapp.net",
        )

        result = contact_to_dict(contact)

        assert result["name"] is None


class TestSenderAliases:
    """Tests for _sender_aliases — verify it calls the bridge and falls back to DB."""

    def test_resolves_lid_via_bridge(self):
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.json.return_value = {
            "phone": "13232432100",
            "lid": "231241139937355",
            "aliases": [
                "13232432100",
                "13232432100@s.whatsapp.net",
                "231241139937355",
                "231241139937355@lid",
            ],
        }
        with patch("whatsapp.requests.get", return_value=mock_resp) as mock_get:
            result = _sender_aliases("231241139937355@lid")

        mock_get.assert_called_once()
        assert mock_get.call_args[1].get("params", {}).get("jid") == "231241139937355@lid"
        assert result == [
            "13232432100",
            "13232432100@s.whatsapp.net",
            "231241139937355",
            "231241139937355@lid",
        ]

    def test_falls_back_to_db_when_bridge_unavailable(self):
        import requests as req_lib
        with patch("whatsapp.requests.get", side_effect=req_lib.RequestException("down")):
            result = _sender_aliases("13232432100@s.whatsapp.net")

        bare = "13232432100"
        assert bare in result
        assert f"{bare}@s.whatsapp.net" in result

    def test_falls_back_to_db_when_bridge_returns_error_status(self):
        mock_resp = MagicMock()
        mock_resp.ok = False
        with patch("whatsapp.requests.get", return_value=mock_resp):
            result = _sender_aliases("13232432100")

        assert "13232432100" in result

    def test_falls_back_when_bridge_returns_malformed_json(self):
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.json.side_effect = ValueError("not json")
        with patch("whatsapp.requests.get", return_value=mock_resp):
            result = _sender_aliases("13232432100")
        assert "13232432100" in result

    def test_falls_back_when_bridge_returns_empty_aliases(self):
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.json.return_value = {"phone": "", "lid": "", "aliases": []}
        with patch("whatsapp.requests.get", return_value=mock_resp):
            result = _sender_aliases("13232432100")
        assert "13232432100" in result
        assert "13232432100@s.whatsapp.net" in result


class TestResolveLIDToPhone:
    """Tests for _resolve_lid_to_phone — verify it calls the bridge and falls back."""

    def test_resolves_lid_via_bridge(self):
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.json.return_value = {
            "phone": "13232432100",
            "lid": "231241139937355",
            "aliases": ["13232432100", "13232432100@s.whatsapp.net",
                        "231241139937355", "231241139937355@lid"],
        }
        with patch("whatsapp.requests.get", return_value=mock_resp):
            result = _resolve_lid_to_phone("231241139937355@lid")

        assert result == "13232432100"

    def test_returns_none_when_bridge_returns_empty_phone(self):
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_resp.json.return_value = {"phone": "", "lid": "", "aliases": []}
        with patch("whatsapp.requests.get", return_value=mock_resp):
            result = _resolve_lid_to_phone("999@lid")

        assert result is None

    def test_falls_back_to_db_when_bridge_unavailable(self):
        import requests as req_lib
        with patch("whatsapp.requests.get", side_effect=req_lib.RequestException("down")):
            result = _resolve_lid_to_phone("231241139937355@lid")

        assert result is None
