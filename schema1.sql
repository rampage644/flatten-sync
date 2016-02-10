drop table if exists users CASCADE;
drop table if exists posts CASCADE;
drop table if exists comments CASCADE;
drop table if exists likes CASCADE;

create table users (_id TEXT PRIMARY KEY, value TEXT, root_id TEXT, root_index INT);
create table posts (_id TEXT PRIMARY KEY, value TEXT, user_id TEXT REFERENCES users (_id) ON DELETE CASCADE, user_index INT);
create table comments (_id TEXT PRIMARY KEY, value TEXT, post_id TEXT REFERENCES posts (_id) ON DELETE CASCADE, post_index INT);
create table likes (_id TEXT PRIMARY KEY, value TEXT, comment_id TEXT REFERENCES comments (_id) ON DELETE CASCADE, comment_index INT);

create index on users (_id);
create index on posts (_id);
create index on comments (_id);
create index on likes (_id);
