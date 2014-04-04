
CREATE TABLE IF NOT EXISTS logs (
    ref char(40) PRIMARY KEY,
    json text NOT NULL
);

CREATE TABLE IF NOT EXISTS logs_name (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ref char(40) NOT NULL,
    name char(40) NOT NULL
);

CREATE INDEX IF NOT EXISTS name_index on logs_name(name);
