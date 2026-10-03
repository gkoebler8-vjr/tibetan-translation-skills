# Programmatic access to Dharmamitra / DharmaNexus / BuddhaNexus (research, 2026-10-03)

Method: WebFetch only (no outbound network from Bash). WebFetch routes pages through a summarising model, so "verbatim" claims are second-hand unless marked. I could issue GET requests only, so no POST endpoint was exercised live. Every claim below is tagged CONFIRMED (seen in a source) or UNCONFIRMED.

## 0. Bottom line

- There IS a working, unauthenticated, JSON/REST API behind dharmamitra.org. It has Swagger/OpenAPI specs, and Dharmamitra's own GitHub org publishes a Claude Code agent starter pack that calls it. (CONFIRMED)
- There is NO separately documented "developer API with keys" for the public. The only API key found (`x-key` header) guards three summary/explanation endpoints. (CONFIRMED)
- Two caveats must be weighed before automating:
  1. robots.txt disallows `/api-search/` and `/api-db/` for all user agents. (CONFIRMED)
  2. The project's DharmaNexus guide page states Terms of Service that forbid using the API to "populate third-party applications, presentation layers, or 'staging' environments", and says to email dharmamitra.project@gmail.com for data use. (CONFIRMED, see section 7)
  Their own starter pack nonetheless says "No DharmaMitra account or API key required. Endpoints are public." Personal research use of single-passage queries by an agent is plausibly fine, but pipeline-embedded or bulk use should be cleared with the team.

## 1. dharmamitra.org site

Source: https://dharmamitra.org and https://dharmamitra.org/explore (CONFIRMED)
- Nav: Translate (/), Explore (/explore), OCR (/ocr), DB (/db), Lexicon (lexicon.dharmamitra.org), Visualizations, News, Guide (https://dharmamitra.github.io/dharmamitra-guides/), People. Footer: version v1.45.5 (28 Sept 2026).
- Statement on the page: "MITRA Deep Research and MITRA Explore use Google Gemini API features, all other MITRA tools are based on self-trained dedicated models." So the Explore AI summary and the Deep Research translate mode are Gemini-generated; the standalone MITRA translator is self-trained (Qwen3.5/Gemma-2 based).
- No login, no rate-limit text, no ToS link on the main page, /explore, or /db. https://dharmamitra.org/terms returns 404.
- https://buddhanexus.net (and /api/docs) 301-redirect to https://dharmamitra.org/db. BuddhaNexus is retired; its successor is DharmaNexus (= the /db section; paper cites https://dharmanexus.org).

## 2. The real API: base paths

Two OpenAPI-documented FastAPI backends on the same host:

| Backend | Swagger UI | OpenAPI JSON | Title / version |
|---|---|---|---|
| Search backend | https://dharmamitra.org/api-search/docs | https://dharmamitra.org/api-search/openapi.json | "Dharmamitra Search Backend" v0.1.0 |
| DharmaNexus DB backend | https://dharmamitra.org/api-db/docs | https://dharmamitra.org/api-db/openapi.json | "DharmaNexus Backend" v0.2.1 |

robots.txt (https://dharmamitra.org/robots.txt, CONFIRMED) also lists /api-tagging/ and /api-aligner/ as disallowed prefixes.

Note: the old BuddhaNexus api (api.buddhanexus.net, buddhanexus.net/api) is gone/redirected; the archived repos (BuddhaNexus/buddhanexus = backend, buddhanexus-frontend-next, segmented-tibetan/sanskrit/chinese/pali) are GitHub-archived. Not worth using.

## 3. Search backend endpoints (from https://dharmamitra.org/api-search/openapi.json, CONFIRMED)

Security: global none; `APIKeyHeader` (header `x-key`) is required ONLY on `/summary/`, `/explanation/`, `/explanation-parallel/`. All endpoints below need no key.

### 3a. Primary search (the engine under Explore)
`POST https://dharmamitra.org/api-search/primary/`  (Content-Type: application/json)
SearchRequest:
- `search_input` (string, required) - query in Tibetan script / Wylie / IAST / etc. or English
- `input_encoding`: auto | tibetan | wylie | dev | iast | hk (default auto)
- `search_type`: regular (lexical) | semantic (lexical + vector, default) | semantic_only
- `semantic_type`: paragraph | both (default both)
- `filter_source_language`: auto | bo | sa | zh | pa | all (default auto)
- `filter_target_language`: same set (default all)
- `source_filters`: {include_files[], include_categories[], include_collections[], segmentnr}
- `do_ranking` bool (default true; starter pack recommends false), `max_depth` int (default 200; starter pack recommends 30)
- `lexical_normalization` (Tibetan normalisation: mode single/fused, level 0-6, drop_nominal, slop, require_phrase, min_should_match), `expand_parallels` bool (default false)
Response PrimarySearchResponse: `{"results": [PrimarySearchResult...], "lexical_normalization": ...}`; each result has `id, query, lang, segmentnr, source, title, summary, text, text_new{text_before,text_main,text_after,translation}, src_link`, optionally `all_segmentnrs, vector, parallel_of`. `text_new.translation` is an English translation of the hit; `summary` is a per-hit summary string. Strip `vector`/`text_new` for agent use (starter pack). Reading-room deep link is in `src_link` (form https://dharmamitra.org/nexus/db/bo/BO_K01_D0006/text?active_segment=BO_K01_D0006:42b-3).
Example (from starter pack examples/primary-search-semantic.json, CONFIRMED request keys):
```
curl -sS -X POST https://dharmamitra.org/api-search/primary/ -H 'Content-Type: application/json' \
 -d '{"search_input":"the nature of mind is clear light","search_type":"semantic","filter_source_language":"bo","max_depth":30,"do_ranking":false}'
```
Direct segment lookup: `{"search_input":"BO_K01_D0006:42b-3","source_filters":{"segmentnr":"BO_K01_D0006:42b-3"}}`.
Segment IDs look like `BO_K01_D0006:42b-3` (lang_collection+category_Derge-number : folio-line). Tibetan files confirmed so far are Kangyur only (see section 6).

### 3b. Explore (with AI answer/summary) - what the web UI calls
- `POST /api-search/explore/v1/chat/completions` - "primary search + streaming chat response. Preferred endpoint for explore."
- `POST /api-search/explore/v2/chat/completions` - deep-research multi-turn (plan -> search loop -> synthesize); adds `planning_mode`, `stream_events` (typed JSON events). `GET /api-search/explore/v2/event-schema` exists (returns a `done` event with `rendered`, `skipped_duplicates`, `citations`; full event catalogue not seen). Legacy: `/search/v1/chat/completions`.
- Body = SearchChatRequest = OpenAI-style chat + SearchRequest fields: `model` (enum gpt-3.5-turbo|default|mitra-base|mitra-pro|fgs), `messages` (required, [{role,content}]), `stream` (default TRUE; set false for one JSON), `temperature` (0.2), `locale` (REQUIRED; en, bo, ja, ko, zh-Hans, zh-Hant, vi, hi, ru, fr, it, de, nl, es, pt, ar, tr, sa ...), plus `input_encoding, search_type, semantic_type, filter_source_language, filter_target_language, source_filters, max_depth (default 50), planning_mode, stream_events, force_planning`.
- Response schema is "{}" in OpenAPI, i.e. undocumented; it streams (SSE/OpenAI-like chunks) unless stream=false. Exact chunk format: UNCONFIRMED. `GET /api-search/v1/models` lists models `dharmamitra-translate` and `dharmamitra-explore` (CONFIRMED live GET), so an OpenAI-compatible client pointed at `/api-search/v1/chat/completions` with model `dharmamitra-explore` / `dharmamitra-translate` is plausible (UNCONFIRMED whether that path takes the same body).
- Other: `/secondary/` (secondary-literature search, body: search_input, input_encoding, search_type, filter_secondary, postprocess_model), `/chat-summary/v1/chat/completions` (takes `locale` + a PrimarySearchResult), `/citation/`, `/rag-examples`.

### 3c. Translate
- `POST /api-search/cat-translate/v1/translate` (CONFIRMED in starter pack + OpenAPI). Multi-witness translation. Body: `input_tibetan, input_chinese, input_pali, input_sanskrit` (strings, at least one), `context`, `focus` (equal|tibetan|chinese|pali|sanskrit), `target_language` (free-form label e.g. "english"), `style_instruction` (free prose), `highlight_term`. Response `{"translation": "..."}`. 3-8 s typical, up to ~60 s, upstream times out at 100 s (curl 524). Likely Gemini-backed (UNCONFIRMED).
- `POST /api-search/chat-translate/v1/chat/completions` and `/v2/...` (ChatCompletionRequest): OpenAI-style. Fields: `model, messages, stream (default false), temperature (0.1), do_grammar, input_encoding, target_lang (default english), mode (normal | explain-grammar | deep-research), gemini_model, stream_events, align, output_mode (block|interleaved)`. This is what the main Translate page and the "Deep Research" mode use. `messages` = [{"role":"user","content":"<source text>"}]. v2 adds typed events (`/chat-translate/v2/event-schema`, `/alignment-event-schema`, `/research-event-schema`).
- `POST /api-search/knn-translate-no-stream/` and `/knn-translate-gemini-no-stream/` (body `{query, language, do_grammar}`) - older retrieval-augmented ("kNN") translation, non-streaming.
- `POST /api-search/fgs-translate/v1/chat/completions` - a Fo Guang Shan style/domain variant.
- `POST /api-search/kundoku/v1/annotate`, `/ocr/` (+ status/result/cancel), `/rate_translations`, `/translation-rating/`, `GET /health`.

## 4. DharmaNexus DB backend (parallels) - https://dharmamitra.org/api-db/openapi.json (CONFIRMED)
No security scheme. Paths: `/matches/` (POST), `/menudata/` (GET), `/table-view/table/` (POST), `/graph-view/` (POST), `/download/` (POST), `/text-view/middle/` (POST), `/text-view/text-parallels/` (POST), `/numbers-view/numbers/` (POST), `/numbers-view/categories/` (GET), `/links/external/`, `/utils/count-matches/` (POST), `/utils/folios/`, `/utils/displayname/`, `/utils/raw-metadata/`, `/utils/segment-links/`, `/utils/active-segment-for-folio/`, `/alignment/` (POST), `/health`.
Request shapes (from starter pack scripts/nexus.sh, CONFIRMED via summary):
- `POST /api-db/matches/` body `{"segment_nrs":["SA_K02_sspp2_3u:7287","SA_K02_sspp2_3u:7288"]}` -> every stored parallel for those segments (aligned text, score, segment ids).
- `GET /api-db/menudata/?language=bo` (I did a live GET; it works) -> `{"menudata":[{collection, collectiondisplayname, categories:[{category, categorydisplayname, files:[{displayName, filename, textname, search_field}]}]}]}`. Filenames e.g. BO_K01_D0001.
- `POST /api-db/table-view/table/` body `{"filename":"SA_T07_vakobhau","filters":{"par_length":50,"score":70,"languages":["bo"],"include_files":[],"exclude_files":[],"include_categories":[],"exclude_categories":[],"include_collections":[],"exclude_collections":[]},"page":0,"sort_method":"position"|"length","folio":optional}` -> 100 rows/page; whole-text intersection with the rest of the corpus.
- `GET /api-db/utils/raw-metadata/?filename=BO_K01_D0006` (live GET works) -> bibliographic metadata (Tibetan/Wylie/Sanskrit/English titles, translators, Derge/Peking numbers, BDRC link, file ids) plus an AI-generated overview with bracketed source citations.
Exact response field names for matches/table: UNCONFIRMED (starter pack references `score`, `par_length`, segment ids and `displayName`; I did not see a sample payload).

## 5. GitHub / Hugging Face

GitHub org https://github.com/dharmamitra (CONFIRMED list): byt5-sanskrit-analyzers, dharmamitra-stardict-dictionaries, mitra-parallel, **dharmamitra-claude-code-agent**, dharmanexus-sanskrit / -pali / -chinese (data), dharmamitra-emacs, indology-genealogy, mitra-bo-zh-tagger, dharmamitra-guides, dvarapandita, dharmamitra-leaderboard. There is NO public repo for the search/db backend or the Next.js frontend (frontend source not found; the old BuddhaNexus backend/frontend repos are archived and obsolete). So (d) "self-host the backend" is not possible; only the models and datasets are self-hostable.

The key repo: https://github.com/dharmamitra/dharmamitra-claude-code-agent (CONFIRMED) - "starter toolkit for agentic translation, philology/critical-edition, and intertextuality research on classical Buddhist texts". Files: scripts/primary-search.sh, cat-translate.sh, nexus.sh, trim-primary.sh, identify-text.py, build-corpus-index.py; .claude/agents/{corpus-searcher,translator,philologist,intertextual-researcher,reference-reader}.md; .claude/commands/{translate,critical-edition,find-parallels,identify-text,intertextuality,lookup-segment}.md; examples/*.json (request bodies); CLAUDE.md (full API reference). Defaults in the scripts: PRIMARY = https://dharmamitra.org/api-search/primary/ ; CAT = https://dharmamitra.org/api-search/cat-translate/v1/translate ; DB = https://dharmamitra.org/api-db (env overrides DHARMAMITRA_PRIMARY_URL, DHARMAMITRA_CAT_TRANSLATE_URL, DHARMAMITRA_DB_URL). Raw URLs: https://raw.githubusercontent.com/dharmamitra/dharmamitra-claude-code-agent/main/{README.md,CLAUDE.md,scripts/*}. This is the best reference to copy.

Other published pieces: PyPI `dharmamitra-sanskrit-grammar` (Python client for grammar API; page could not be read, UNCONFIRMED details) and PyPI `mcp-dharmamitra` (an MCP server wrapping the public OCR endpoint; details unread). Browser extensions exist (Chrome/Firefox "Dharmamitra Language Tools").

Hugging Face: org `dharmamitra` (the `buddhist-nlp` org shows the same listing; huggingface.co/dharmamitra itself 404'd via WebFetch, buddhist-nlp worked): 62 models, 26 datasets. Recently updated models: mitra-qwen35-translate, mitra-qwen35-it, mitra-qwen35-embedder, mitra-qwen35-2b-embedder, mitra-qwen35-base-stage1/stage2, mitra-qwen35-2b-base-stage2, bdrc-mitra-ocr-qwen35-0.8b, mitra-bo-zh-tagger, byt5-mitra-bo-tagger, gemma-2-mitra-chat; also buddhist-nlp/gemma-2-mitra-e (9B embedding model, L2-normalised, query prompt `<instruct>Please find the semantically most similar text in {language}.\n<query>{text}`, corpus side raw text; loadable with Transformers/vLLM/SGLang). Datasets: mitrasamgraha-released-data-only, translation-postcorrection, tatpa-cleaned/-noisy, m2qa-training, mitra-instructions(1,5,6,8,9). Model cards for the Qwen3.5 embedder returned 401 via WebFetch (UNCONFIRMED contents). The parallel corpus is on GitHub: https://github.com/dharmamitra/mitra-parallel (v2 2026: 1,693,730 aligned records / 2,338,400 segment pairs; Sanskrit-Tibetan, Sanskrit-Chinese, Chinese-Tibetan; CC BY-SA 4.0 per guides' datasets page; paper says CC BY 4.0). Also github.com/sebastian-nehrdich/sanstib (317k Skt-Tib pairs). These are sentence-aligned translation pairs, NOT a canon-wide passage-parallel/commentary dataset; the DharmaNexus parallels themselves are only available via the API (a bulk dump was not found).

## 6. Explore internals, commentary, ranking, variants

Sources: MITRA paper https://arxiv.org/abs/2601.06400 (html: arxiv.org/html/2601.06400), guides https://github.com/dharmamitra/dharmamitra-guides/blob/main/docs/dharmanexus.md and mitra_tools/search.md.
- Embedding model: Gemma 2 MITRA-E (9B, contrastive fine-tune with task prompts). Lexical side: Tibetan Paul-Hackett-style substitution stemmer; ByT5-Sanskrit segmentation; Elasticsearch analyzers for Chinese. Vector store/DB product: UNCONFIRMED (paper says deployment is challenging because of vector size; "Elasticsearch" is named for lexical analysis). Starter pack says the default `semantic` mode = lexical + vector "via English pivot" (the OpenAPI `text_new.translation` field is the English pivot text).
- Data sources per guides: Pali - SuttaCentral + VRI Chaṭṭha Saṅgāyana; Sanskrit - GRETIL, DSBC, Muktabodha, SuttaCentral; Chinese - CBETA; Tibetan - ACIP and Tsadra's Dharma Cloud. BDRC links appear in metadata. No mention of eKangyur.
- Paper/doc: parallels are precomputed with a 3-stage pipeline (MADLAD-400 MT to English pivot, BGE-M3 candidate clusters via spatial hashing, BERTAlign refinement with domain-finetuned LaBSE) for the sentence corpus; DharmaNexus parallel matching uses "modernized algorithms ... combine multilingual matching with deep semantic similarity from Gemma 2 MITRA-E".
- Commentary: the guides say Search "performs particularly well locating canonical citations within commentaries across language barriers" and covers "Abhidharma commentaries"; the starter pack's corpus-searcher says use `include_collections: ["tengyur"]` for commentary material. BUT a live GET of /api-db/menudata/?language=bo showed only the "Kangyur" collection (K01-K10) in the portion I could read, and the tool said the output was truncated, so whether a Tengyur collection (Derge Tengyur commentaries, filenames likely BO_T..) is present is UNCONFIRMED. Test first: POST /primary/ with `source_filters.include_collections:["tengyur"]`, or inspect full menudata (curl locally on the user's machine, this sandbox cannot).
- Witnesses/variants: the index appears to be one text per Derge number (e.g. BO_K01_D0006, with a "-2" sibling file); no per-witness apparatus (Derge vs Narthang vs Stok Palace) was seen. UNCONFIRMED; likely single Derge-based edition for Kangyur.
- Ranking: `do_ranking` true by default (some reranking step; model unspecified); starter pack says pass false for agent use. `/table-view` rows carry `score` (0-100) and `par_length`; sort by position or length.
- Guides explicitly state Search is "not a conversational AI", does not write essays and cannot distinguish historical layers.
- The Explore AI summary (Gemini) is generated from the retrieved hits; in the API this is `/explore/v1/chat/completions` (streamed) or per-hit `summary` in `/primary/` results (cheaper, no LLM stream to parse).

## 7. Terms, robots, account
- No login needed on the web UI or API (CONFIRMED by use of public GETs and starter-pack text).
- robots.txt: `User-agent: *  Allow: /  Disallow: /api-db/ /api-search/ /api-tagging/ /api-aligner/ /TODO`; Googlebot and bingbot Crawl-delay 10. (CONFIRMED verbatim as returned by WebFetch.) This is a crawler directive; it conflicts in spirit with agent API calls, though the project's own starter pack tells agents to call these endpoints.
- ToS wording (via https://github.com/dharmamitra/dharmamitra-guides/blob/main/docs/dharmanexus.md as summarised by WebFetch): "You may not use the Dharmamitra API or DharmaNexus database API to populate third-party applications, presentation layers, or 'staging' environments"; scholarly work relying on unauthorised API access is considered a violation; "If you are interested in using our data for your project, please reach out to us" -> dharmamitra.project@gmail.com. No separate ToS page found. No rate limits are published for the API; starter pack says rate limits are in its CLAUDE.md but the CLAUDE.md I read listed none. Latency notes: primary 0.3-3 s; matches 1-5 s; cat-translate 3-8 s (cap 100 s).
- Dharmamitra tools are described as "free-to-use".

## 8. Recommended access strategy (ranked)

(a) Documented API with key: NOT available. No public developer program; the `x-key` header only guards summary/explanation endpoints. Possible only by emailing dharmamitra.project@gmail.com (also the right route to get permission and a Tengyur/bulk answer).

(b) Frontend-used endpoints (BEST practical route; officially sanctioned by the org's own agent starter pack, with OpenAPI at /api-search/docs and /api-db/docs). Needs: curl/Python `requests`, JSON POSTs run from the USER's machine (this sandbox's Bash has no network). Suggested minimal client:
   1. `POST /api-search/primary/` with `search_type:"semantic"`, `max_depth:30`, `do_ranking:false`, then keep only `segmentnr, lang, source, title, text, summary, src_link, text_new.translation`.
   2. For parallels of a located segment: `POST /api-db/matches/ {"segment_nrs":[...]}`.
   3. For an AI synthesis: `POST /api-search/explore/v1/chat/completions` with `stream:false`, `locale:"en"`, `messages:[{"role":"user","content":"..."}]` (non-streaming behaviour and output shape UNCONFIRMED; test it).
   4. Translate: `/api-search/cat-translate/v1/translate` (non-streaming JSON, simplest) or `/chat-translate/v1/chat/completions`.
   Mind: be polite (sequential calls, ~1 req/s or slower, cache results), keep it to personal research, do not feed it into a hosted/third-party app, cite via returned `src_link`, and consider emailing the team given the ToS and robots.txt. For the user's LZ pipeline, note this would be an extra optional reference/check, not a replacement of the local MITRA model (consistent with the memory note that the local Qwen3.5 model is the construal baseline; the hosted Translate uses Gemini for Deep Research).
   Cheapest first step: copy the starter pack repo's scripts (clone https://github.com/dharmamitra/dharmamitra-claude-code-agent) and run `./scripts/primary-search.sh` on one test query.

(c) Browser automation of dharmamitra.org/explore: unnecessary, because the same data comes from (b); it is slower and brittle and offers nothing extra except exactly what the UI renders. Only fall back if the endpoints start requiring tokens/CORS-bound headers. Needs the Browser pane or Playwright.

(d) Self-hosting from GitHub: NOT feasible for the DB/search backend (no public backend repo; old BuddhaNexus backend is archived, uses old data/algorithms). Partial self-host is possible: gemma-2-mitra-e (9B, heavy) or the smaller mitra-qwen35-embedder / 2b-embedder (HF; card not read) to embed your own Tibetan corpus (e.g. the user's own Kangyur/Tengyur files) plus mitra-parallel for sentence-level cross-language alignment; this reproduces semantic search but not DharmaNexus's precomputed canon-wide parallels or Gemini summaries.

(e) Manual copy-paste via the web UI: always works, zero ToS risk; use for one-off lookups (e.g. a sutra verse and its Tengyur commentary passages) and to verify what Tengyur coverage looks like before writing code.

## Things to verify next (unconfirmed)
1. Is a Tengyur collection indexed (try include_collections:["tengyur"], or run the full menudata GET locally and grep "Tengyur"/"BO_T").
2. Exact JSON/SSE shape of explore/v1 with stream false/true, and whether `/v1/chat/completions` is OpenAI-compatible.
3. Field names in `/matches/` and `/table-view/table/` responses.
4. Whether the ToS block applies to individual research use (ask dharmamitra.project@gmail.com).

---------------------------------------------------------------
## ADDENDUM (coordinator follow-up): BFF, frontend repos, plain DB search, segment-with-context

Repos:
- dharmamitra/dharmamitra-frontend-public and dharmamitra/dharmanexus-public: PLACEHOLDERS. Git tree = a single 30-byte README.md, 1 commit (CONFIRMED via api.github.com tree). No frontend source, no .env, no endpoint list there.
- Base URL: same origin, https://dharmamitra.org, with path prefixes /api-search, /api-db (OpenAPI, CONFIRMED). No api.dharmamitra.org seen in any source. Your /bff/api/search/explore is a Next.js backend-for-frontend proxy; no BFF OpenAPI/docs found (/bff/openapi.json, /bff/api/openapi.json, /bff/docs, /bff/api/docs all 404). A plain GET of /bff/api/search/explore returned 200 {"message":"Namo tassa bhagavato arahato sammaṅgamānuyo!"} (a root/greeting handler; POST does the work).
- The OpenAPI itself mentions the BFF: /citation/pending/{response_id} is "Used by the BFF to gate the cite-button enablement". Hypothesis (UNCONFIRMED): the BFF exists partly to attach the `x-key` for key-guarded routes.

"Database Results" list (the ~49 hits): almost certainly `POST https://dharmamitra.org/api-search/primary/` (SearchRequest; response `results[]` with segmentnr, all_segmentnrs, lang, source, title, text, summary, src_link, text_new{text_before,text_main,text_after,translation}). Same fields as your explore body (search_input, input_encoding, search_type, filter_source_language, filter_target_language, source_filters, do_ranking, max_depth, expand_parallels) minus target_lang. Not seen being called by the UI (UNCONFIRMED that the UI uses it), but it is public, keyless, and the starter pack uses it. Per-hit `summary` is already in the response. Starter pack recommends do_ranking:false, max_depth:30. Corpora per starter pack: Kangyur, Tengyur, Taisho, Pali Nikayas, Skt critical editions (Tengyur claim from starter pack text; my menudata read was truncated, so still verify).

Per-segment "Explanation" call: matching OpenAPI routes (both header-auth, `x-key`):
- POST /api-search/explanation/ body {"query":str,"summary":str,"locale":"en"} -> {"summary":str,"relevance":"low|medium|high"} (non-stream); /api-search/summary/ same body, SSE stream.
- POST /api-search/explanation-parallel/ body {"query","src_text","tgt_text","src_translation","tgt_translation","locale"} -> same SummaryRespone.
- Keyless alternative: POST /api-search/chat-summary/v1/chat/completions body {"locale":"en","search_result":<one PrimarySearchResult object copied from /primary/>,"stream":false?,"model":..} -> OpenAI-compatible SSE; "Behavior matches Explore segmentnr mode: full passage + translation". Likely what the UI's per-segment explanation uses (UNCONFIRMED). No key listed on it.
- The `x-key` value is not published anywhere I found; do not guess it. Without it, use chat-summary or the explore stream.

Fetching a segment WITH context:
- Starter pack's lookup-segment returns the matched segment only: POST /api-search/primary/ {"search_input":"BO_K12_D0381:158a-16","source_filters":{"segmentnr":"BO_K12_D0381:158a-16"}}. Its `text_new.text_before / text_main / text_after / translation` (TextSegment, CONFIRMED in OpenAPI: "We return text-Before and text_after as well to give context") is the in-response context window (starter pack strips text_new, so it did not document it; use it).
- For a wider window: POST /api-db/text-view/text-parallels/ body {"filename":"BO_K12_D0381","folio":"158a","active_segment":"BO_K12_D0381:158a-16","include_matches":false,"page":0,"page_size":100..1000} -> {"page","total_pages","items":[{"segnr","segtext":[{"text","highlightColor","matches":[parallel ids],"is_active_match"}],"lang"}]} (TextParallelsInput/TextViewLeftOutput, CONFIRMED in api-db OpenAPI; behaviour on a live call UNTESTED). Helpers: GET /api-db/utils/folios/?filename=..., GET /api-db/utils/active-segment-for-folio/?filename=..&folio=.., GET /api-db/utils/displayname/?segmentnr=.. -> {"displayname":[..]}, GET /api-db/utils/segment-links/?segmentnr=.. -> {rkts_link,touda_link,kokuyaku_link,archive_link,suttacentral_link}.

Parallels:
- POST /api-db/matches/ {"segment_nrs":[...]} -> {"matches":[{id,root_segnr[],par_segnr[],root_offset_beg/end,par_offset_beg/end,score,par_length,root_text,par_text,par_full_names,root_full_names}]} (CONFIRMED schema).
- POST /api-db/table-view/table/ {"filename","filters","page","sort_method":"position|quotedtext|length|length2","folio","skip_pagination"} -> array of {id,par_segnr_range,par_full_names,root_full_names,root_segnr_range,par_length,root_length,score,src_lang,tgt_lang,root_fulltext[],par_fulltext[]}.
- Shared `filters`: {par_length, score, languages:["all|bo|sa|pa|zh"], include/exclude_files|categories|collections, not_before, not_after, hide_stock(default true)}.
- POST /api-db/text-view/middle/ {"parallel_ids":[..],"filters"} -> per-parallel {id,par_segnr_range,par_segnr,display_name,tgt_lang,src_lang,filename,score,length,par_fulltext[]}. POST /api-db/alignment/ {"parallel_id"} -> syllable-level alignment columns. POST /api-db/utils/count-matches/.

Auth/key: none for /primary/, explore, chat-translate, cat-translate, chat-summary, and all /api-db routes. `x-key` header only on /summary/, /explanation/, /explanation-parallel/.
