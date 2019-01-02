# News Website Reporting Tool

A simple Python script to generate 3 simple reports for an aribtary news website:
* The most popular three articles of all time
* The most popular article authors of all time
* Days where more than 1% of requests lead to errors

The result is output in plain text as in this [sample file](sample.txt)

## Prerequisites

* Vagrant VM hosted [here](https://github.com/udacity/fullstack-nanodegree-vm)
  The VM contains Python 2 + Postgres DB

* The `news` database (*not included*) with its 3 main tables `articles`, `authors` and `log`

* Several views to be created detailed in the following section

## Views

Create the following views using `psql news` in order:

--The views take into consideration that an author might not have any articles yet or that an article might not have any logs yet

`create view authors_articles as
select au.name author, ar.title article, ar.slug, '/article/' || ar.slug path
from authors au left join articles ar on ar.author = au.id;`

`create view articles_log as
select ar.author, ar.article, ar.slug, ar.path, l.status, l.time access_time, l.id
from authors_articles ar left join log l on l.path = ar.path;`

--The view considers only staus codes starting with 4 or 5 as errors

`create view daily_errors as
select date_trunc('day', time) view_day, count(1) as num
from log
where status like '4%' or status like '5%'
group by date_trunc('day', time);`

`create view daily_requests as
select date_trunc('day', time) view_day, count(1) as num
from log
group by date_trunc('day', time);`

--The view requires multiplication by 1.0 to cast into float

`create view daily_err_perc as
select e.view_day, (e.num*1.0/r.num*1.0)*100 as err_perc
from daily_errors e, daily_requests r
where r.view_day = e.view_day;`

## Usage

Simply run the Python script `python2 news-reports.py` or directly from Linux `./news-reports.py`.

## Known Issues

The script has no caching mechanism, so it loads all te results from the DB everytime.

## Contributions

I encourage you all to contribute into this simple project to make better and more usable.
