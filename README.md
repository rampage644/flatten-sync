# Flatten scheme sync experiments

The goal of this project is to evaluate how costly and difficult it is to maintain mongodb's flattened data.

Let's say we have such document:

```json
{
    "name": "userA",
    "posts": [
        {
            "title": "title1",
            "body": "body1"
            "comments": [
                {
                    "content": "comment1"
                },
                {
                    "content": "comment2"
                }
            ]
        }
    ]
}
```

So, there is user `embeds_many` posts relationship and also post `embeds_many` comments relationship.

First idea is to maintain in child tables link to parent and also index field that makes it easy to find child entry based on index.

```sql
create table users (_id TEXT, name TEXT);
create table posts (_id TEXT, title TEXT, body TEXT, u_id TEXT, u_index INT);
create table comments (_id TEXT, content TEXT, p_id TEXT, p_index INT);
```

Second idea is to store all parents' id in chain.

```sql
create table users (_id TEXT, name TEXT);
create table posts (_id TEXT, title TEXT, body TEXT, u_id TEXT, u_index INT);
create table comments (_id TEXT, content TEXT, u_id TEXT, u_index INT, p_id TEXT, p_index INT);
```

## Experiment

 * Generate data so users table contains 100 records, posts contains 10000 records and comments table contains 1M records
 * Query comments table to get some field vale
 * Delete all records related to some user `_id` from all tables.

 ## How to

```bash
python schema1.py # generate data according to schema1
python schema2.py # generate data according to schema2
```

```sql
# query to get id for update
select comments.value from users join posts on users._id = posts.user_id join comments on posts._id = comments.post_id where users._id = '33' and posts.user_index = 27 and comments.post_index = 14; # for schema1
select comments.value from comments where user_id = '33' and post_index = 27 and index = 14; # for schema2

# delete stmts for nested strucure updates
delete from comments where user_id = '33'; 
delete from posts where user_id = '33'; 
delete from users where _id = '33'; 
```

## Results

 * Do **not** use postgre features such as `CASCADE DELETE` of any kind of constraints (foreign key: `REFERENCES`). Implement all sync logic on app side: will make updates **much** faster and can easily switch SQL engine.
 * **No** difference between schemas. 
 * Query results in 150ms for 1M table.
 * Delete takes 150ms to remove 10000 records in 1M table. I guess, `logN` complexity

## TODO

 * Implement sync functionality
 * Stress test on events stream