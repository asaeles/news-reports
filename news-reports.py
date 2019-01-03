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


def get_news_records(cur, sql):
    """Returns all records returned from the passed query
    from the 'news' database."""
    cur.execute(sql)
    recs = cur.fetchall()
    return recs


def get_pop_articles(cur):
    """Return formatted plain text containing
    the most popular three articles of all time."""
    recs = get_news_records(cur, GET_POP_ARTICLES)
    text = "The most popular three articles of all time:\n"
    text += "".join(" \"%s\" — %d views\n" % (article, views)
                    for article, views in recs)
    return text


def get_pop_authors(cur):
    """Return formatted plain text containing
    the most popular article authors of all time."""
    recs = get_news_records(cur, GET_POP_AUTHORS)
    text = "The most popular article authors of all time:\n"
    text += "".join(" %s — %d views\n" % (author, views)
                    for author, views in recs)
    return text


def get_bad_days(cur):
    """Return formatted plain text containing
    days where more than 1% of requests lead to errors."""
    recs = get_news_records(cur, GET_BAD_DAYS)
    text = "Days where more than 1% of requests lead to errors:\n"
    text += "".join(" {:%B %d, %Y} — {:.1f}% errors\n"
                    .format(view_day, err_perc)
                    for view_day, err_perc in recs)
    return text


# Finally print the three reports
if __name__ == '__main__':
    db_conn = psycopg2.connect("dbname=news")
    cur = db_conn.cursor()
    print(get_pop_articles(cur))
    print(get_pop_authors(cur))
    print(get_bad_days(cur))
    db_conn.close()
