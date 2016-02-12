drop table if exists users CASCADE;
drop table if exists posts CASCADE;
drop table if exists comments CASCADE;

create table users (_id TEXT PRIMARY KEY, 
                    value TEXT, 
                    index INT);
create table posts (_id TEXT PRIMARY KEY, 
                    value TEXT, 
                    index INT,
                    user_id TEXT, 
                    user_index INT);
create table comments (_id TEXT PRIMARY KEY, 
                       value TEXT, 
                       index INT,
                       user_id TEXT, 
                       user_index INT, 
                       post_id TEXT, 
                       post_index INT);

create index on users (_id);
create index on posts (_id);
create index on comments (_id);
