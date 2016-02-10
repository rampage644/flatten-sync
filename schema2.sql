drop table if exists users;
drop table if exists posts;
drop table if exists comments;

create table users (_id TEXT, name TEXT);
create table posts (_id TEXT, title TEXT, body TEXT, u_id TEXT, u_index INT);
create table comments (_id TEXT, content TEXT, u_id TEXT, u_index INT, p_id TEXT, p_index INT);