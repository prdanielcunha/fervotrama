CREATE TABLE IF NOT EXISTS records (id TEXT PRIMARY KEY NOT NULL, kind TEXT NOT NULL, parent TEXT, data TEXT NOT NULL, updated_at TEXT NOT NULL);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS records_kind_parent ON records(kind,parent);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS revisions (id INTEGER PRIMARY KEY AUTOINCREMENT, record_id TEXT NOT NULL, data TEXT NOT NULL, created_at TEXT NOT NULL);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS files (id TEXT PRIMARY KEY NOT NULL, record_id TEXT, name TEXT NOT NULL, type TEXT NOT NULL, size INTEGER NOT NULL, created_at TEXT NOT NULL, role TEXT);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY NOT NULL, value TEXT NOT NULL);
