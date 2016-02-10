#!/usr/bin/env python
"""Main module."""
from __future__ import print_function


import psycopg2
import itertools
import sys

DSN = 'dbname=testDB'


def generate_schema():
    """Drop and create tables."""
    with psycopg2.connect(DSN) as conn:
        with conn.cursor() as cur:
            with open('schema1.sql') as ifile:
                cur.execute(ifile.read())
    conn.close()


def generate_id(prev_id, count):
    """Generate ID."""
    for id in range(prev_id, prev_id + count):
        yield id


def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks."""
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)


class Generator(object):
    """Generate data for schema."""

    def __init__(self, factor):
        """Ctor."""
        self.factor = factor

    def generate_records(self, table, start_id, parent_id, count):
        """Generate records.

        Generates `count` records for `table` with given
        `start_id` and `parent_id`

        Yields every record id
        """
        for index, record_id in enumerate(generate_id(start_id, count)):
            sql = 'insert into {0} values (%s, %s, %s, %s);'.format(table)
            self.cur.execute(sql, (str(record_id),
                                   'value' + str(record_id),
                                   str(parent_id),
                                   index))
            yield record_id

    def generate_data(self):
        """Generate data."""
        p_user_id = 1
        p_post_id = 1
        p_comment_id = 1
        p_like_id = 1

        self.conn = psycopg2.connect(DSN)
        self.cur = self.conn.cursor()

        def posts(post_id, pid):
            return self.generate_records('posts',
                                         post_id, pid, self.factor)

        def comments(comment_id, pid):
            return self.generate_records('comments',
                                         comment_id, pid, self.factor)

        def likes(like_id, pid):
            return self.generate_records('likes',
                                         like_id, pid, self.factor)

        users = self.generate_records('users', p_user_id, '0', self.factor)
        for user in users:
            for post in posts(p_post_id, user):
                for comment in comments(p_comment_id, post):
                    for like in likes(p_like_id, comment):
                        p_like_id = like + 1
                    p_comment_id = comment + 1
                p_post_id = post + 1

        self.conn.commit()
        self.cur.close()
        self.conn.close()


# TODO don't  try to understand, just refactor
def query(id, query_string):
    """Query the data."""
    breadcrumbs = query_string.split('.')
    field_name = breadcrumbs[-1]

    prev_table = 'users'
    join_clause = [prev_table + ' ']
    where_clause = ['{table}._id = %s '.format(table=prev_table)]
    args = [id]
    for table, index in grouper(breadcrumbs[:-1], 2):
        join_clause.append(' {rtable} on {ltable}._id = {rtable}.{ltable_id} '.
                           format(ltable=prev_table, rtable=table, ltable_id=prev_table[:-1] + '_id'))
        where_clause.append(' {ltable}.{rtable}_index = %s '.format(ltable=table, rtable=prev_table[:-1]))
        prev_table = table
        args.append(index)

    sql = 'select {table}.{field} from {join} where {where}'.format(
        table=breadcrumbs[-3],
        field=field_name,
        join='join'.join(join_clause),
        where='and'.join(where_clause))

    with psycopg2.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, tuple(args))
            res = cur.fetchmany()
    conn.close()
    return res


def main():
    """Main function."""
    generate_schema()

    g = Generator(40)
    g.generate_data()
    return 0


if __name__ == '__main__':
    sys.exit(main())
