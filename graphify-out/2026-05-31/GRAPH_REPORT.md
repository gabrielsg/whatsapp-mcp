# Graph Report - .  (2026-05-30)

## Corpus Check
- 41 files · ~147,669 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 476 nodes · 974 edges · 41 communities (26 shown, 15 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 90 edges (avg confidence: 0.79)
- Token cost: 199,697 input · 0 output

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
- [[_COMMUNITY_Webhook Dispatch|Webhook Dispatch]]
- [[_COMMUNITY_Python Audio Conversion|Python Audio Conversion]]
- [[_COMMUNITY_MCP Query Utilities|MCP Query Utilities]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]

## God Nodes (most connected - your core abstractions)
1. `handleMessage()` - 42 edges
2. `T` - 37 edges
3. `newTestMessageStore()` - 32 edges
4. `MessageStore` - 29 edges
5. `testLogger()` - 25 edges
6. `newTestClient()` - 22 edges
7. `main()` - 21 edges
8. `str` - 21 edges
9. `handleHistorySync()` - 17 edges
10. `sendWhatsAppMessage()` - 15 edges

## Surprising Connections (you probably didn't know these)
- `resolveLIDChat()` --semantically_similar_to--> `_sender_aliases`  [INFERRED] [semantically similar]
  whatsapp-bridge/main.go → whatsapp-mcp-server/whatsapp.py
- `analyzeOggOpus()` --semantically_similar_to--> `convert_to_opus_ogg`  [INFERRED] [semantically similar]
  whatsapp-bridge/main.go → whatsapp-mcp-server/audio.py
- `Bearer-token + Host-header authentication` --conceptually_related_to--> `_bridge_headers`  [INFERRED]
  whatsapp-bridge/auth.go → whatsapp-mcp-server/whatsapp.py
- `captureWebhook()` --calls--> `HandlerFunc`  [INFERRED]
  whatsapp-bridge/main_test.go → whatsapp-bridge/auth.go
- `list_messages` --references--> `store/messages.db (SQLite)`  [EXTRACTED]
  whatsapp-mcp-server/whatsapp.py → whatsapp-bridge/main.go

## Hyperedges (group relationships)
- **REST auth pipeline: token generation, header enforcement, host validation** — whatsapp_bridge_auth_loadorcreatabridgetoken, whatsapp_bridge_auth_witauth, whatsapp_bridge_auth_buildallowdhosts, whatsapp_bridge_auth_checkbearertoken, whatsapp_mcp_server_whatsapp_bridgeheaders [EXTRACTED 0.95]
- **LID-to-phone normalization: live resolution, DB migration, Python fallback** — whatsapp_bridge_main_resolvelidchat, whatsapp_bridge_main_resolveuserjid, whatsapp_bridge_main_migratelegacylidchatstophonejids, whatsapp_bridge_main_migratelegacylidsenderstophones, whatsapp_mcp_server_whatsapp_resolvelidtophone, whatsapp_mcp_server_whatsapp_senderaliases [EXTRACTED 0.95]
- **Inbound message handling: receive event, resolve JID, store, forward webhook** — whatsapp_bridge_main_handlemessage, whatsapp_bridge_main_storechat, whatsapp_bridge_main_storemessage, whatsapp_bridge_webhook_sendwebhook, whatsapp_bridge_webhook_sendwebhookwithmedia [EXTRACTED 0.95]
- **CI pipeline: ci.yml enforces blocking gates defined in AGENTS.md, linting config in .golangci.yml** — workflows_ci_ci_workflow, agents_ci_blocking_gates, golangci_golangci_yml, workflows_security_workflow, agents_ci_informational_gates [EXTRACTED 1.00]
- **Release automation: release-please workflow + RELEASING.md playbook + manual fallback workflow produce versioned artifacts** — workflows_release_please_workflow, docs_releasing_releasing_md, workflows_release_manual_fallback, agents_release_please, changelog_changelog_md [EXTRACTED 1.00]
- **Contribution governance: AGENTS.md PR rules + ROADMAP.md scope + CONTRIBUTING.md workflow + PR template enforce quality and direction** — agents_agents_md, agents_pr_rules, roadmap_roadmap_md, contributing_contributing_md, pr_template_pr_template [EXTRACTED 1.00]

## Communities (41 total, 15 thin omitted)

### Community 0 - "WhatsApp MCP Test Suite"
Cohesion: 0.06
Nodes (62): Tests for WhatsApp MCP server functions., Test chat without last message time., Tests for contact conversion functions., Test basic message to dict conversion., Test contact to dict conversion., Test contact without name., Test message from self shows 'Me' as sender., Test message with media type. (+54 more)

### Community 1 - "Go SQLite Data Types"
Cohesion: 0.13
Nodes (60): LIDStore, Message, MessageStore, NullInt64, NullString, Server, WebhookPayload, handleMessage() (+52 more)

### Community 2 - "Docs & CI Architecture"
Cohesion: 0.05
Nodes (48): AGENTS.md — AI Agent & Contributor Guide, Blocking CI gates: Python Lint, Python Tests, Go Lint, Go Build, Version Consistency, CodeQL, Informational CI gates: Bandit, pip-audit, govulncheck (continue-on-error), Data flow: AI client → MCP server → SQLite/bridge REST → bridge → WhatsApp Web, Environment variables: WHATSAPP_DB_PATH, WHATSAPP_API_URL, WHATSAPP_BRIDGE_PORT, WHATSAPP_BRIDGE_TOKEN, WHATSAPP_MEDIA_ROOTS, WEBHOOK_URL, FORWARD_SELF, whatsapp-bridge/ — Go bridge (main.go, webhook.go, store/), JID (WhatsApp identifier): DM @s.whatsapp.net, group @g.us, LID @lid, PR rules: one concern per PR, conventional commits, reference issue, update docs, tests, no drive-by formatting (+40 more)

### Community 3 - "MCP Server Tools (Python)"
Cohesion: 0.12
Nodes (32): download_media(), get_chat(), get_contact(), get_contact_chats(), get_direct_chat_by_contact(), get_last_interaction(), get_message_context(), list_chats() (+24 more)

### Community 4 - "Ephemeral Message Settings"
Cohesion: 0.13
Nodes (20): Disappearing-message (ephemeral) settings tracking, ContextInfo, DisappearingMode, ChatEphemeralSettings, DownloadMediaRequest, DownloadMediaResponse, analyzeOggOpus(), applyChatEphemeralSettings() (+12 more)

### Community 5 - "HTTP Auth & Routing"
Cohesion: 0.20
Nodes (19): HandlerFunc, ServeMux, buildAllowedHosts, buildAllowedHosts(), checkBearerToken(), hostAllowed(), loadOrCreateBridgeToken(), T (+11 more)

### Community 6 - "Bridge Token & Startup"
Cohesion: 0.15
Nodes (11): BasicCallMeta, store/.bridge-token file, loadOrCreateBridgeToken, printTokenBanner(), callChatJID(), Logger, handleCallOffer(), main() (+3 more)

### Community 7 - "Message Store Schema"
Cohesion: 0.20
Nodes (8): DB, ensureColumn(), ensureMessageStoreSchema(), Time, handleMessageRevoke(), MessageStore.MarkMessageDeleted, NewMessageStore(), MessageStore

### Community 8 - "Media Path Safety"
Cohesion: 0.26
Nodes (15): Media-path confinement (allowlist), canonicalizePath(), pathHasPrefix(), resolveMediaRoots(), T, TestPathHasPrefix(), TestResolveMediaRootsAcceptsEnvList(), TestResolveMediaRootsRejectsRelativeEnv() (+7 more)

### Community 9 - "List Chats Tests"
Cohesion: 0.14
Nodes (12): _make_messages_db(), messages_db(), Regression tests for list_chats / get_chat.  The previous SQL referenced messa, Regression: same bug existed in get_chat., Create a minimal messages.db that matches the real bridge schema., Default behavior: include the joined last_message fields., Regression: include_last_message=False must not error and must     still return, Filter by query while not including the last message — both code paths     shou (+4 more)

### Community 10 - "Chat Sync & Metadata"
Cohesion: 0.26
Nodes (14): HistorySync, MessageInfo, MessageStore.GetChatEphemeralSettings, GetChatName(), Client, JID, handleHistorySync(), resolveLIDChat() (+6 more)

### Community 11 - "Release Config & Versioning"
Cohesion: 0.15
Nodes (11): description, name, packages, repository, source, url, $schema, title (+3 more)

### Community 12 - "Example Use Screenshot"
Cohesion: 0.26
Nodes (12): Claude AI Chat Interface (claude.ai), Finding Contact Flow, get_direct_chat_by_contact Tool (WhatsApp local MCP), Getting Replies Flow, Haiku Message: 'Code builds bridges now / WhatsApp control at your touch / MCP takes form', Example Use - WhatsApp MCP Demo Screenshot, search_contacts Tool (WhatsApp local MCP), send_message Tool (WhatsApp local MCP) (+4 more)

### Community 13 - "Media Download & Classification"
Cohesion: 0.27
Nodes (4): MediaType, classifyMediaPath(), extractMediaInfo(), MediaDownloader

### Community 14 - "LID Migration"
Cohesion: 0.24
Nodes (10): LID-to-phone JID resolution, store/messages.db (SQLite), MessageStore.MigrateLegacyLIDChatsToPhoneJIDs, MessageStore.MigrateLegacyLIDSendersToPhones, store/whatsapp.db (whatsmeow session DB), get_sender_name, list_chats, _resolve_lid_to_phone (+2 more)

### Community 16 - "Release-Please Config"
Cohesion: 0.22
Nodes (8): bootstrap-sha, changelog-path, extra-files, include-component-in-tag, include-v-in-tag, packages, release-type, $schema

### Community 17 - "Audio Conversion & REST Auth"
Cohesion: 0.25
Nodes (9): Bearer-token + Host-header authentication, Go REST API bridge (localhost:8080), convert_to_opus_ogg, convert_to_opus_ogg_temp, _bridge_headers, download_media (whatsapp.py), send_audio_message (whatsapp.py), send_file (whatsapp.py) (+1 more)

### Community 18 - "Changelog & Release History"
Cohesion: 0.22
Nodes (9): Release Please — automated release management, CHANGELOG.md — project release history, Release v0.1.0 (2026-03-02) — initial fork release with typing API, webhook, MCP tools, CI/CD, Release v0.2.0 (2026-04-22) — image webhook, full-history flag, call events, LID fixes, security hardening, Release v0.2.1 (2026-05-14) — bridge bug fixes, disappearing messages, CI fix, docs/RELEASING.md — maintainer release playbook, Release (Manual Fallback) workflow — workflow_dispatch to rebuild/re-upload artifacts for existing tag, Release artifact publishing: whatsapp-bridge-linux-amd64, Python wheel+sdist, SHA256SUMS.txt (+1 more)

### Community 19 - "Version Check Script"
Cohesion: 0.52
Nodes (6): int, str, main(), normalize_tag(), read_pyproject_version(), read_server_json_versions()

### Community 20 - "Go Test Mocks"
Cohesion: 0.53
Nodes (4): Context, NoopStore, JID, mockLIDStore

### Community 22 - "Webhook Dispatch"
Cohesion: 0.70
Nodes (4): SendWebhook(), sendWebhookPayload(), SendWebhookWithMedia(), WebhookPayload

### Community 23 - "Python Audio Conversion"
Cohesion: 0.50
Nodes (4): convert_to_opus_ogg(), convert_to_opus_ogg_temp(), Convert an audio file to Opus format in an Ogg container and store in a temporar, Convert an audio file to Opus format in an Ogg container.      Args:

### Community 24 - "MCP Query Utilities"
Cohesion: 0.40
Nodes (5): get_contact_chats, get_last_interaction, get_message_context, list_messages, _sender_aliases

## Knowledge Gaps
- **81 isolated node(s):** `.`, `$schema`, `bootstrap-sha`, `release-type`, `include-v-in-tag` (+76 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `handleMessage()` connect `Go SQLite Data Types` to `Ephemeral Message Settings`, `Bridge Token & Startup`, `Message Store Schema`, `Chat Sync & Metadata`, `Media Download & Classification`, `Webhook Dispatch`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Why does `newRESTMux()` connect `HTTP Auth & Routing` to `Go SQLite Data Types`, `Ephemeral Message Settings`, `Message Store Schema`, `Media Path Safety`, `Chat Sync & Metadata`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Why does `main()` connect `Bridge Token & Startup` to `Go SQLite Data Types`, `Ephemeral Message Settings`, `HTTP Auth & Routing`, `Message Store Schema`, `Media Path Safety`, `Chat Sync & Metadata`, `LID Migration`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `handleMessage()` (e.g. with `TestHandleMessage_BackfillsEphemeralFromContextInfo()` and `TestHandleMessage_DuplicateRevokeKeepsEarliestDeletedAt()`) actually correct?**
  _`handleMessage()` has 17 INFERRED edges - model-reasoned connections that need verification._
- **What connects `.`, `$schema`, `bootstrap-sha` to the rest of the system?**
  _135 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `WhatsApp MCP Test Suite` be split into smaller, more focused modules?**
  _Cohesion score 0.06354642313546423 - nodes in this community are weakly interconnected._
- **Should `Go SQLite Data Types` be split into smaller, more focused modules?**
  _Cohesion score 0.1284153005464481 - nodes in this community are weakly interconnected._