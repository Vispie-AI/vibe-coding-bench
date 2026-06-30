-- creative-gen durable schema (VIZ-1402)
CREATE TABLE IF NOT EXISTS items (
    item_id     TEXT PRIMARY KEY,
    creator_id  TEXT NOT NULL,
    caption     TEXT,
    hook        TEXT,
    performance REAL,
    served_by   TEXT,
    created_at  TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS usage (
    creator_id TEXT PRIMARY KEY,
    count      INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS items_creator_idx ON items (creator_id);
CREATE INDEX IF NOT EXISTS items_perf_idx    ON items (performance DESC);
