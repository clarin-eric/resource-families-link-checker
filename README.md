# resource-families-link-checker

Scrapy-based link checker for the [CLARIN resource families](https://www.clarin.eu/resource-families). Inspired by:

* [The DataCite PidCheck](https://github.com/datacite/pidcheck)
* [The Scrapy tutorial](https://docs.scrapy.org/en/1.6/intro/tutorial.html)

Use: `scrapy crawl resfam -o resfam-20200520.csv &> logs-resfam-20200520.txt`

This will store the resulting CSV with the check results in resfam-20200520.csv and store verbose logs in logs-resfam-20200520.txt

See the output directory for some examples of output and log files.

