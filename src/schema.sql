-- MTG Brain — canonical schema. ALL loaders must conform to this file.
-- Do not invent columns. If you need a new column, it goes here first.

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

-- ---------------------------------------------------------------- cards
CREATE TABLE IF NOT EXISTS cards (
    oracle_id        TEXT PRIMARY KEY,
    name             TEXT NOT NULL,
    mana_cost        TEXT,
    cmc              REAL,
    type_line        TEXT,
    oracle_text      TEXT,
    colors           TEXT,          -- JSON array e.g. ["G","U"]
    color_identity   TEXT,          -- JSON array e.g. ["G","U","W"]
    keywords         TEXT,          -- JSON array
    power            TEXT,
    toughness        TEXT,
    loyalty          TEXT,
    rarity           TEXT,
    layout           TEXT,
    card_faces_json  TEXT,          -- JSON or NULL
    legal_commander  TEXT,          -- 'legal' | 'not_legal' | 'banned' | 'restricted'
    edhrec_rank      INTEGER,
    price_usd        REAL,
    scryfall_uri     TEXT,
    image_normal     TEXT
);
CREATE INDEX IF NOT EXISTS idx_cards_name       ON cards(name);
CREATE INDEX IF NOT EXISTS idx_cards_name_nocase ON cards(name COLLATE NOCASE);
CREATE INDEX IF NOT EXISTS idx_cards_cmc        ON cards(cmc);
CREATE INDEX IF NOT EXISTS idx_cards_edhrec     ON cards(edhrec_rank);

-- FTS5 over the searchable text. Populated by the loader (external-content
-- is avoided deliberately: the rebuild is a full truncate+reload, so a plain
-- contentless-shadow table is simpler and cannot desync.)
CREATE VIRTUAL TABLE IF NOT EXISTS cards_fts USING fts5(
    oracle_id UNINDEXED,
    name,
    oracle_text,
    type_line,
    tokenize = 'unicode61 remove_diacritics 2'
);

-- ---------------------------------------------------- scryfall id bridge
-- MTGJSON joins on scryfallId (a *print* id), not oracle_id. This maps them.
CREATE TABLE IF NOT EXISTS card_prints (
    scryfall_id TEXT PRIMARY KEY,
    oracle_id   TEXT NOT NULL REFERENCES cards(oracle_id)
);
CREATE INDEX IF NOT EXISTS idx_prints_oracle ON card_prints(oracle_id);

-- ------------------------------------------------------------- rulings
CREATE TABLE IF NOT EXISTS rulings (
    oracle_id     TEXT NOT NULL,
    published_at  TEXT,
    comment       TEXT,
    source        TEXT
);
CREATE INDEX IF NOT EXISTS idx_rulings_oracle ON rulings(oracle_id);

CREATE VIRTUAL TABLE IF NOT EXISTS rulings_fts USING fts5(
    oracle_id UNINDEXED,
    comment,
    tokenize = 'unicode61 remove_diacritics 2'
);

-- --------------------------------------------------------------- rules
CREATE TABLE IF NOT EXISTS rules (
    rule_number   TEXT PRIMARY KEY,   -- '601.2a', '100.1', '1' (section header)
    section       TEXT,               -- '6' for 601.2a
    parent_number TEXT,               -- '601.2' for '601.2a'; NULL for top level
    text          TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_rules_section ON rules(section);
CREATE INDEX IF NOT EXISTS idx_rules_parent  ON rules(parent_number);

CREATE VIRTUAL TABLE IF NOT EXISTS rules_fts USING fts5(
    rule_number UNINDEXED,
    text,
    tokenize = 'unicode61 remove_diacritics 2'
);

-- ------------------------------------------------------------ glossary
CREATE TABLE IF NOT EXISTS glossary (
    term       TEXT PRIMARY KEY,
    definition TEXT NOT NULL
);
CREATE VIRTUAL TABLE IF NOT EXISTS glossary_fts USING fts5(
    term UNINDEXED,
    definition,
    tokenize = 'unicode61 remove_diacritics 2'
);

-- --------------------------------------------------------------- decks
CREATE TABLE IF NOT EXISTS decks (
    deck_id        TEXT PRIMARY KEY,   -- slug: 'tidus' | 'bumbleflower' | 'dogmeat' | 'merged-bant'
    name           TEXT NOT NULL,
    set_code       TEXT,
    release_date   TEXT,
    commander_name TEXT,
    source_file    TEXT
);

CREATE TABLE IF NOT EXISTS deck_cards (
    deck_id   TEXT NOT NULL REFERENCES decks(deck_id),
    oracle_id TEXT NOT NULL REFERENCES cards(oracle_id),
    count     INTEGER NOT NULL,
    board     TEXT NOT NULL CHECK (board IN ('main','commander')),
    PRIMARY KEY (deck_id, oracle_id, board)
);
CREATE INDEX IF NOT EXISTS idx_deckcards_deck ON deck_cards(deck_id);

-- ------------------------------------------------------------- edhrec
CREATE TABLE IF NOT EXISTS edhrec_cache (
    slug         TEXT PRIMARY KEY,
    fetched_at   TEXT,
    payload_json TEXT
);

-- ------------------------------------------------------- learning loop
CREATE TABLE IF NOT EXISTS game_log (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    played_at TEXT,
    deck_id   TEXT,
    opponents TEXT,
    result    TEXT,
    notes     TEXT
);

CREATE TABLE IF NOT EXISTS rules_missed (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    logged_at         TEXT,
    rule_number       TEXT,
    what_i_got_wrong  TEXT
);

-- -------------------------------------------------------- build metadata
CREATE TABLE IF NOT EXISTS build_meta (
    key   TEXT PRIMARY KEY,
    value TEXT
);
