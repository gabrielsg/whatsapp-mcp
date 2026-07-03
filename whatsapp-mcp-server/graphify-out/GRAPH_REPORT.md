# Graph Report - whatsapp-mcp-server  (2026-07-03)

## Corpus Check
- 13 files · ~8,888 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 208 nodes · 374 edges · 15 communities (9 shown, 6 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 15 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `da335b57`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]

## God Nodes (most connected - your core abstractions)
1. `str` - 22 edges
2. `str` - 16 edges
3. `Message` - 16 edges
4. `Chat` - 15 edges
5. `Any` - 14 edges
6. `msg_to_dict()` - 13 edges
7. `chat_to_dict()` - 12 edges
8. `_sender_aliases()` - 12 edges
9. `Any` - 11 edges
10. `list_messages()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `TestChatConversion` --uses--> `Message`  [INFERRED]
  tests/test_whatsapp.py → whatsapp.py
- `TestContactConversion` --uses--> `Message`  [INFERRED]
  tests/test_whatsapp.py → whatsapp.py
- `TestMessageConversion` --uses--> `Message`  [INFERRED]
  tests/test_whatsapp.py → whatsapp.py
- `TestResolveLIDToPhone` --uses--> `Message`  [INFERRED]
  tests/test_whatsapp.py → whatsapp.py
- `TestSenderAliases` --uses--> `Message`  [INFERRED]
  tests/test_whatsapp.py → whatsapp.py

## Import Cycles
- None detected.

## Communities (15 total, 6 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.09
Nodes (31): Tests for WhatsApp MCP server functions., Test chat without last message time., Tests for message conversion functions., Tests for contact conversion functions., Test contact to dict conversion., Test contact without name., Tests for chat conversion functions., Test direct message chat conversion. (+23 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (37): Any, bool, int, str, Path, download_media(), get_bridge_status(), get_chat() (+29 more)

### Community 2 - "Community 2"
Cohesion: 0.13
Nodes (32): Test basic message to dict conversion., Test message from self shows 'Me' as sender., Test message with media type., Handle shutdown signals gracefully to prevent zombie processes., shutdown_handler(), _bridge_headers(), download_media(), format_message() (+24 more)

### Community 4 - "Community 4"
Cohesion: 0.14
Nodes (12): _make_messages_db(), messages_db(), Regression tests for list_chats / get_chat.  The previous SQL referenced messa, Regression: same bug existed in get_chat., Create a minimal messages.db that matches the real bridge schema., Default behavior: include the joined last_message fields., Regression: include_last_message=False must not error and must     still return, Filter by query while not including the last message — both code paths     shou (+4 more)

### Community 7 - "Community 7"
Cohesion: 0.29
Nodes (7): str, convert_to_opus_ogg(), convert_to_opus_ogg_temp(), Convert an audio file to Opus format in an Ogg container and store in a temporar, Convert an audio file to Opus format in an Ogg container.      Args:, Transcribe an audio file to text using faster-whisper.      Args:         fil, transcribe_audio()

### Community 8 - "Community 8"
Cohesion: 0.39
Nodes (3): Tests for _sender_aliases — verify it calls the bridge and falls back to DB., TestSenderAliases, _sender_aliases()

### Community 10 - "Community 10"
Cohesion: 0.38
Nodes (4): Tests for _resolve_lid_to_phone — verify it calls the bridge and falls back., TestResolveLIDToPhone, Resolve a WhatsApp LID to a phone number via the bridge, falling back to DB., _resolve_lid_to_phone()

## Knowledge Gaps
- **4 isolated node(s):** `str`, `start-sse.sh script`, `version`, `sessions`
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Chat` connect `Community 0` to `Community 8`, `Community 10`, `Community 2`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `transcribe_audio()` connect `Community 7` to `Community 1`, `Community 2`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `Message` connect `Community 2` to `Community 0`, `Community 8`, `Community 10`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `Message` (e.g. with `TestChatConversion` and `TestContactConversion`) actually correct?**
  _`Message` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `Chat` (e.g. with `TestChatConversion` and `TestContactConversion`) actually correct?**
  _`Chat` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `str`, `Convert an audio file to Opus format in an Ogg container.      Args:`, `Convert an audio file to Opus format in an Ogg container and store in a temporar` to the rest of the system?**
  _63 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.09246088193456614 - nodes in this community are weakly interconnected._