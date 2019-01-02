#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""The script generates the following 3 simple reports
for an aribtary news website:
    The most popular three articles of all time
    The most popular article authors of all time
    Days where more than 1% of requests lead to errors
"""

import psycopg2

# Select statement for getting the most
# popular three articles of all time
GET_POP_ARTICLES = """
select article, count(id) as views
from articles_log
group by article
order by views desc
limit 3;
"""

# Select statement for getting the most
# popular article authors of all time
GET_POP_AUTHORS = """
select author, count(id) as views
from articles_log
group by author
order by views desc;
"""

# Select statement for getting days where
# more than 1% of requests lead to errors
GET_BAD_DAYS = """
select *
from daily_err_perc
where err_perc > 1;
"""


def get_news_records(sql):
    """Returns all records returned from the passed query
    from the 'news' database."""
    db_conn = psycopg2.connect("dbname=news")
    conn_cur = db_conn.cursor()
    conn_cur.execute(sql)
    recs = conn_cur.fetchall()
    db_conn.close()
    return recs


def get_pop_articles():
    """Return formatted plain text containing
    the most popular three articles of all time."""
    recs = get_news_records(GET_POP_ARTICLES)
    text = "The most popular three articles of all time:\n"
    text += "".join(" \"%s\" — %d views\n" % (article, views)
                    for article, views in recs)
    return text


def get_pop_authors():
    """Return formatted plain text containing
    the most popular article authors of all time."""
    recs = get_news_records(GET_POP_AUTHORS)
    text = "The most popular article authors of all time:\n"
    text += "".join(" %s — %d views\n" % (author, views)
                    for author, views in recs)
    return text


def get_bad_days():
    """Return formatted plain text containing
    days where more than 1% of requests lead to errors."""
    recs = get_news_records(GET_BAD_DAYS)
    text = "Days where more than 1% of requests lead to errors:\n"
    text += "".join(" {:%B %d, %Y} — {:.1f}% errors\n"
                    .format(view_day, err_perc)
                    for view_day, err_perc in recs)
    return text


# Finally print the three reports
print(get_pop_articles())
print(get_pop_authors())
print(get_bad_days())
