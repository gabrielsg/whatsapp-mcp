# Graph Report - whatsapp-bridge  (2026-06-10)

## Corpus Check
- 33 files · ~151,864 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 776 nodes · 1845 edges · 65 communities (35 shown, 30 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 133 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `34117a42`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_WhatsApp MCP Test Suite|WhatsApp MCP Test Suite]]
- [[_COMMUNITY_Go SQLite Data Types|Go SQLite Data Types]]
- [[_COMMUNITY_Docs & CI Architecture|Docs & CI Architecture]]
- [[_COMMUNITY_MCP Server Tools (Python)|MCP Server Tools (Python)]]
- [[_COMMUNITY_Ephemeral Message Settings|Ephemeral Message Settings]]
- [[_COMMUNITY_HTTP Auth & Routing|HTTP Auth & Routing]]
- [[_COMMUNITY_Bridge Token & Startup|Bridge Token & Startup]]
- [[_COMMUNITY_Message Store Schema|Message Store Schema]]
- [[_COMMUNITY_Media Path Safety|Media Path Safety]]
- [[_COMMUNITY_List Chats Tests|List Chats Tests]]
- [[_COMMUNITY_Chat Sync & Metadata|Chat Sync & Metadata]]
- [[_COMMUNITY_Release Config & Versioning|Release Config & Versioning]]
- [[_COMMUNITY_Example Use Screenshot|Example Use Screenshot]]
- [[_COMMUNITY_Media Download & Classification|Media Download & Classification]]
- [[_COMMUNITY_LID Migration|LID Migration]]
- [[_COMMUNITY_Bridge Auth Tests|Bridge Auth Tests]]
- [[_COMMUNITY_Release-Please Config|Release-Please Config]]
- [[_COMMUNITY_Audio Conversion & REST Auth|Audio Conversion & REST Auth]]
- [[_COMMUNITY_Changelog & Release History|Changelog & Release History]]
- [[_COMMUNITY_Version Check Script|Version Check Script]]
- [[_COMMUNITY_Go Test Mocks|Go Test Mocks]]
- [[_COMMUNITY_Get Contact Tests|Get Contact Tests]]
- [[_COMMUNITY_Webhook Dispatch|Webhook Dispatch]]
- [[_COMMUNITY_Python Audio Conversion|Python Audio Conversion]]
- [[_COMMUNITY_MCP Query Utilities|MCP Query Utilities]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]

## God Nodes (most connected - your core abstractions)
1. `handleMessage()` - 48 edges
2. `T` - 43 edges
3. `T` - 43 edges
4. `newTestMessageStore()` - 42 edges
5. `T` - 41 edges
6. `newTestClient()` - 31 edges
7. `MessageStore` - 30 edges
8. `testLogger()` - 28 edges
9. `main()` - 23 edges
10. `msg_to_dict()` - 23 edges

## Surprising Connections (you probably didn't know these)
- `resolveLIDChat()` --semantically_similar_to--> `_sender_aliases`  [INFERRED] [semantically similar]
  /mnt/c/Users/gabri/Projects/whatsapp-bridge/whatsapp-bridge/main.go → whatsapp-mcp-server/whatsapp.py
- `analyzeOggOpus()` --semantically_similar_to--> `convert_to_opus_ogg`  [INFERRED] [semantically similar]
  /mnt/c/Users/gabri/Projects/whatsapp-bridge/whatsapp-bridge/main.go → whatsapp-mcp-server/audio.py
- `Bearer-token + Host-header authentication` --conceptually_related_to--> `_bridge_headers`  [INFERRED]
  whatsapp-bridge/auth.go → whatsapp-mcp-server/whatsapp.py
- `LID Resolution Consolidation Implementation Plan` --implements--> `/api/resolve`  [EXTRACTED]
  docs/superpowers/plans/2026-05-31-lid-resolution-consolidation.md → whatsapp-bridge/main.go
- `_sender_aliases` --references--> `whatsmeow_lid_map`  [EXTRACTED]
  whatsapp-mcp-server/whatsapp.py → whatsapp.db

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Release automation: release-please workflow + RELEASING.md playbook + manual fallback workflow produce versioned artifacts** — workflows_release_please_workflow, docs_releasing_releasing_md, workflows_release_manual_fallback, agents_release_please, changelog_changelog_md [EXTRACTED 1.00]

## Communities (65 total, 30 thin omitted)

### Community 0 - "WhatsApp MCP Test Suite"
Cohesion: 0.11
Nodes (34): Any, bool, int, bool, str, store/messages.db (SQLite), format_message(), format_messages_list() (+26 more)

### Community 1 - "Go SQLite Data Types"
Cohesion: 0.07
Nodes (70): BasicCallMeta, Disappearing-message (ephemeral) settings tracking, LID-to-phone JID resolution, ContextInfo, DB, DisappearingMode, HistorySync, MediaType (+62 more)

### Community 2 - "Docs & CI Architecture"
Cohesion: 0.11
Nodes (82): LID Resolution Consolidation Implementation Plan, Client, JID, Logger, T, Time, Context, HandlerFunc (+74 more)

### Community 3 - "MCP Server Tools (Python)"
Cohesion: 0.05
Nodes (50): AGENTS.md — AI Agent & Contributor Guide, Blocking CI gates: Python Lint, Python Tests, Go Lint, Go Build, Version Consistency, CodeQL, Informational CI gates: Bandit, pip-audit, govulncheck (continue-on-error), Data flow: AI client → MCP server → SQLite/bridge REST → bridge → WhatsApp Web, Environment variables: WHATSAPP_DB_PATH, WHATSAPP_API_URL, WHATSAPP_BRIDGE_PORT, WHATSAPP_BRIDGE_TOKEN, WHATSAPP_MEDIA_ROOTS, WEBHOOK_URL, FORWARD_SELF, whatsapp-bridge/ — Go bridge (main.go, webhook.go, store/), JID (WhatsApp identifier): DM @s.whatsapp.net, group @g.us, LID @lid, PR rules: one concern per PR, conventional commits, reference issue, update docs, tests, no drive-by formatting (+42 more)

### Community 4 - "Ephemeral Message Settings"
Cohesion: 0.10
Nodes (27): int, str, int, str, main(), normalize_tag(), read_pyproject_version(), read_server_json_versions() (+19 more)

### Community 5 - "HTTP Auth & Routing"
Cohesion: 0.15
Nodes (38): Any, bool, int, str, download_media(), get_bridge_status(), get_chat(), get_contact() (+30 more)

### Community 6 - "Bridge Token & Startup"
Cohesion: 0.26
Nodes (12): Claude AI Chat Interface (claude.ai), Finding Contact Flow, get_direct_chat_by_contact Tool (WhatsApp local MCP), Getting Replies Flow, Haiku Message: 'Code builds bridges now / WhatsApp control at your touch / MCP takes form', Example Use - WhatsApp MCP Demo Screenshot, search_contacts Tool (WhatsApp local MCP), send_message Tool (WhatsApp local MCP) (+4 more)

### Community 7 - "Message Store Schema"
Cohesion: 0.04
Nodes (47): Architecture, Authentication Issues, Bridge authentication and media paths, Building, Call History, Caveats, Chat Operations, CLI flags (Go bridge) (+39 more)

### Community 8 - "Media Path Safety"
Cohesion: 0.31
Nodes (16): Media-path confinement (allowlist), T, canonicalizePath(), pathHasPrefix(), resolveMediaRoots(), T, TestPathHasPrefix(), TestResolveMediaRootsAcceptsEnvList() (+8 more)

### Community 9 - "List Chats Tests"
Cohesion: 0.40
Nodes (6): Go REST API bridge (localhost:8080), _bridge_headers, download_media (whatsapp.py), _read_bridge_token, send_file (whatsapp.py), send_message (whatsapp.py)

### Community 10 - "Chat Sync & Metadata"
Cohesion: 0.23
Nodes (19): Bearer-token + Host-header authentication, T, store/.bridge-token file, buildAllowedHosts, buildAllowedHosts(), checkBearerToken(), hostAllowed(), loadOrCreateBridgeToken() (+11 more)

### Community 11 - "Release Config & Versioning"
Cohesion: 0.22
Nodes (9): Release Please — automated release management, CHANGELOG.md — project release history, Release v0.1.0 (2026-03-02) — initial fork release with typing API, webhook, MCP tools, CI/CD, Release v0.2.0 (2026-04-22) — image webhook, full-history flag, call events, LID fixes, security hardening, Release v0.2.1 (2026-05-14) — bridge bug fixes, disappearing messages, CI fix, docs/RELEASING.md — maintainer release playbook, Release (Manual Fallback) workflow — workflow_dispatch to rebuild/re-upload artifacts for existing tag, Release artifact publishing: whatsapp-bridge-linux-amd64, Python wheel+sdist, SHA256SUMS.txt (+1 more)

### Community 12 - "Example Use Screenshot"
Cohesion: 0.20
Nodes (14): _make_messages_db(), messages_db(), Regression tests for list_chats / get_chat.  The previous SQL referenced messa, Regression: same bug existed in get_chat., Create a minimal messages.db that matches the real bridge schema., Default behavior: include the joined last_message fields., Regression: include_last_message=False must not error and must     still return, Filter by query while not including the last message — both code paths     shou (+6 more)

### Community 13 - "Media Download & Classification"
Cohesion: 0.31
Nodes (6): DummyResponse, test_bridge_headers_falls_back_to_token_file(), test_bridge_headers_prefers_env_over_token_file(), test_bridge_headers_uses_env_token(), test_bridge_post_helpers_include_auth_headers(), test_send_message_without_token_surfaces_bridge_401()

### Community 14 - "LID Migration"
Cohesion: 0.16
Nodes (39): Any, int, str, _bridge_headers(), chat_to_dict(), download_media(), get_bridge_status(), get_chat() (+31 more)

### Community 15 - "Bridge Auth Tests"
Cohesion: 0.09
Nodes (21): 1.1 Install Go, 1.2 Install MSYS2, 1.3 Install uv and Python 3.11, 1.4 Install FFmpeg (for voice messages), 2.1 Clone the repository, 2.2 Build the Go bridge binary, 3.1 Run the bridge for the first time, 3.2 Scan the QR code (+13 more)

### Community 16 - "Release-Please Config"
Cohesion: 0.48
Nodes (5): test_get_contact_backward_compatible_phone_number_param(), test_get_contact_falls_back_to_lid_for_14_digit_numeric_identifier(), test_get_contact_normalizes_lid(), test_get_contact_normalizes_phone_number(), test_get_contact_unresolved_falls_back_to_jid_user()

### Community 17 - "Audio Conversion & REST Auth"
Cohesion: 0.73
Nodes (4): SendWebhook(), sendWebhookPayload(), SendWebhookWithMedia(), WebhookPayload

### Community 21 - "Get Contact Tests"
Cohesion: 0.20
Nodes (12): TestResolveLIDToPhone, TestSenderAliases, Tests for WhatsApp MCP server functions., Tests for _sender_aliases — verify it calls the bridge and falls back to DB., Tests for _resolve_lid_to_phone — verify it calls the bridge and falls back., TestResolveLIDToPhone, TestSenderAliases, whatsmeow_lid_map (+4 more)

### Community 22 - "Webhook Dispatch"
Cohesion: 0.12
Nodes (14): 0.1.0 (2026-03-02), [0.2.0](https://github.com/verygoodplugins/whatsapp-mcp/compare/v0.1.0...v0.2.0) (2026-04-22), [0.2.1](https://github.com/verygoodplugins/whatsapp-mcp/compare/v0.2.0...v0.2.1) (2026-05-14), Added, Bug Fixes, Bug Fixes, Changed, Changelog (+6 more)

### Community 23 - "Python Audio Conversion"
Cohesion: 0.22
Nodes (7): Tests for message conversion functions., Test basic message to dict conversion., Test message from self shows 'Me' as sender., Test message from self shows 'Me' as sender., Test message with media type., Test message with media type., TestMessageConversion

### Community 24 - "MCP Query Utilities"
Cohesion: 0.25
Nodes (9): Tests for contact conversion functions., Test contact to dict conversion., Test contact without name., Test contact without name., TestContactConversion, Contact, contact_to_dict(), Convert a Contact dataclass to a dictionary for JSON serialization. (+1 more)

### Community 25 - "Community 25"
Cohesion: 0.21
Nodes (10): Test chat without last message time., Test chat without last message time., Tests for chat conversion functions., Test direct message chat conversion., Test group chat conversion., Test group chat conversion., TestChatConversion, Chat (+2 more)

### Community 26 - "Community 26"
Cohesion: 0.14
Nodes (11): Architecture (read first), CI gates, Environment variables, Gotchas (read before editing), Local commands, Persona for AI agents working in this repo, PR rules, Reporting bugs / requesting features (+3 more)

### Community 27 - "Community 27"
Cohesion: 0.14
Nodes (12): Bridge stability (`whatsapp-bridge/`), CI / release, How to propose something larger, In scope, MCP correctness (`whatsapp-mcp-server/`), North star, Observability & ops, Out of scope (+4 more)

### Community 29 - "Community 29"
Cohesion: 0.32
Nodes (6): convert_to_opus_ogg(), convert_to_opus_ogg_temp(), convert_to_opus_ogg, Convert an audio file to Opus format in an Ogg container and store in a temporar, Convert an audio file to Opus format in an Ogg container.      Args:, send_audio_message (whatsapp.py)

### Community 30 - "Community 30"
Cohesion: 0.17
Nodes (10): Code style, Contributing, Credit, Security, Setup, TL;DR, What gets merged quickly, What needs more discussion (+2 more)

### Community 39 - "Community 39"
Cohesion: 0.17
Nodes (10): File Map, Final step: push, LID Resolution Consolidation Implementation Plan, Self-Review, Step 1a: Write the three failing tests, Step 2a: Write the failing tests, Step 3a: Write the failing tests, Task 1: Go — add `ResolveResponse` struct and `/api/resolve` endpoint (+2 more)

### Community 46 - "Community 46"
Cohesion: 0.29
Nodes (7): DummyResponse, test_auth_failure_reports_stale_token(), test_bridge_unreachable_reports_not_running(), test_client_outdated_surfaces_reason_and_hint(), test_connected_bridge_reports_healthy(), test_logged_out_surfaces_hint(), test_malformed_health_response()

### Community 47 - "Community 47"
Cohesion: 0.39
Nodes (7): Docs, Linked issues, Risk / rollback, Scope check, Summary, Testing, Type of change

### Community 48 - "Community 48"
Cohesion: 0.22
Nodes (7): Acknowledgments, Disclosure Policy, Reporting a Vulnerability, Scope and Threat Model, Security Policy, Supported Versions, What to Expect

### Community 49 - "Community 49"
Cohesion: 0.29
Nodes (5): 1) Ongoing Development, 2) First Fork Release Version Choice, 3) Artifact Publishing, 4) Manual Fallback (Rare), Releasing (Maintainers)

## Knowledge Gaps
- **172 isolated node(s):** `release-type`, `include-v-in-tag`, `include-component-in-tag`, `changelog-path`, `extra-files` (+167 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **30 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `downloadMedia()` connect `Go SQLite Data Types` to `WhatsApp MCP Test Suite`, `HTTP Auth & Routing`, `Media Path Safety`, `List Chats Tests`, `LID Migration`?**
  _High betweenness centrality (0.137) - this node is a cross-community bridge._
- **Why does `handleMessage()` connect `Go SQLite Data Types` to `Audio Conversion & REST Auth`, `Docs & CI Architecture`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._
- **Why does `newRESTMux()` connect `Go SQLite Data Types` to `Media Path Safety`, `Docs & CI Architecture`, `Chat Sync & Metadata`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Are the 20 inferred relationships involving `handleMessage()` (e.g. with `SendWebhook()` and `SendWebhookWithMedia()`) actually correct?**
  _`handleMessage()` has 20 INFERRED edges - model-reasoned connections that need verification._
- **What connects `release-type`, `include-v-in-tag`, `include-component-in-tag` to the rest of the system?**
  _259 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `WhatsApp MCP Test Suite` be split into smaller, more focused modules?**
  _Cohesion score 0.11092436974789915 - nodes in this community are weakly interconnected._
- **Should `Go SQLite Data Types` be split into smaller, more focused modules?**
  _Cohesion score 0.06600877192982456 - nodes in this community are weakly interconnected._