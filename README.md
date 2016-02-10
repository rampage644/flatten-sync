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