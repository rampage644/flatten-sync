#!/usr/bin/env python
"""Main module."""
from __future__ import print_function


import psycopg2
import itertools
import sys

from schema1 import generate_schema, generate_id, grouper, DSN


class Generator(object):
    """Generate data for schema."""

    def __init__(self, factor):
        """Ctor."""
        self.factor = factor

    def generate_records(self, table, start_id, parents, count):
        """Generate records.

        Generates `count` records for `table` with given
        `start_id` and `parents`: list of (id, index) pairs

        Yields every record id and index
        """
        for index, record_id in enumerate(generate_id(start_id, count)):
            sql = 'insert into {0} values ({1});'.format(
                table, ', '.join(['%s'] * (3 + 2 * len(parents))))
            args = [str(record_id),
                    'value' + str(record_id),
                    index] + list(self._flatten_list(map(lambda x: (x[0], str(x[1])), parents)))
            self.cur.execute(sql, tuple(args))
            yield (record_id, index)

    def _flatten_list(self, list):
        return itertools.chain(*list)

    def generate_data(self):
        """Generate data."""
        p_user_id = 1
        p_post_id = 1
        p_comment_id = 1
        p_like_id = 1

        self.conn = psycopg2.connect(DSN)
        self.cur = self.conn.cursor()

        def posts(post_id, parents):
            return self.generate_records('posts',
                                         post_id, parents, self.factor)

        def comments(comment_id, parents):
            return self.generate_records('comments',
                                         comment_id, parents, self.factor)

        def likes(like_id, parents):
            return self.generate_records('likes',
                                         like_id, parents, self.factor)

        users = self.generate_records('users', p_user_id, [], self.factor)
        for user in users:
            for post in posts(p_post_id, [user]):
                for comment in comments(p_comment_id, [user, post]):
                    # for like in likes(p_like_id, comment):
                        # p_like_id = like + 1
                    p_comment_id = comment[0] + 1
                p_post_id = post[0] + 1

        self.conn.commit()
        self.cur.close()
        self.conn.close()


def main():
    """Main function."""
    generate_schema('schema2.sql')

    g = Generator(100)
    g.generate_data()
    return 0


if __name__ == '__main__':
    sys.exit(main())
