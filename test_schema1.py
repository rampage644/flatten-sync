#!/usr/bin/env python
"""Tests for schema1 module."""

import schema1


def setup_module(module):
    """Generate data."""
    factor = 5  # 5 ** 4
    schema1.generate_schema()

    g = schema1.Generator(factor)
    g.generate_data()


def test_query():
    """Test basic queries."""
    assert schema1.query("2", "posts.3.value") == [("value9",)]
    assert schema1.query("5", "posts.2.value") == [("value23",)]
    assert schema1.query("3", "posts.3.comments.2.value") == [("value68",)]
