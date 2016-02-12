#!/usr/bin/env python
"""Main module."""
from __future__ import print_function


import psycopg2
import itertools
import sys

DSN = 'dbname=testDB'


def generate_schema(filename):
    """Drop and create tables."""
    with psycopg2.connect(DSN) as conn:
        with conn.cursor() as cur:
            with open(filename) as ifile:
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
                    # for like in likes(p_like_id, comment):
                        # p_like_id = like + 1
                    p_comment_id = comment + 1
                p_post_id = post + 1

        self.conn.commit()
        self.cur.close()
        self.conn.close()


def main():
    """Main function."""
    generate_schema('schema1.sql')

    g = Generator(100)
    g.generate_data()
    return 0


if __name__ == '__main__':
    sys.exit(main())
