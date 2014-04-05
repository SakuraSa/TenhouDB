
CREATE TABLE IF NOT EXISTS dbupdate (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key char(40) NOT NULL,
    value text NOT NULL,
    attime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS logs (
    ref char(40) PRIMARY KEY,
    json text NOT NULL,
    gameat timestamp NOT NULL,
    rulecode char(4) NOT NULL,
    lobby char(4) NOT NULL,
    createat timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ref_index on logs(ref);
CREATE INDEX IF NOT EXISTS gameat_index on logs(gameat);
CREATE INDEX IF NOT EXISTS rulecode_index on logs(rulecode);
CREATE INDEX IF NOT EXISTS lobby_index on logs(lobby);
CREATE INDEX IF NOT EXISTS createat_index on logs(createat);

CREATE TABLE IF NOT EXISTS logs_name (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ref char(40) NOT NULL,
    name char(40) NOT NULL
);

CREATE INDEX IF NOT EXISTS id_index on logs_name(id);
CREATE INDEX IF NOT EXISTS ref_index on logs_name(ref);
CREATE INDEX IF NOT EXISTS name_index on logs_name(name);

CREATE TABLE IF NOT EXISTS statistics_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name char(40) NOT NULL,
    hash char(64) NOT NULL,
    json text NOT NULL
);

CREATE INDEX IF NOT EXISTS name_index on statistics_cache(name);
CREATE INDEX IF NOT EXISTS hash_index on statistics_cache(hash);