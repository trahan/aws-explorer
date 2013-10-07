Dependencies
------------

* Elastic Search ([http://www.elasticsearch.org/download](http://www.elasticsearch.org/download))

Setup
-----

1. Start elastic search
2. Create/source a virtual env
3. Run Crawler to get stuff in elastic search
4. Run flask server for UI
5. ???
6. Profit

Crawler
------
```
python src/aws_explorer/crawler.py <es_host> <es_port>
```

UI
--
```
python src/aws_explorer/app.py <es_host> <es_port>
```
Just kidding this doesn't exist yet ...
