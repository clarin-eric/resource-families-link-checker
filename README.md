# resource-families-link-checker

Scrapy-based link checker for the [https://www.clarin.eu/resource-families](CLARIN resource families). Inspired by:

* [https://github.com/datacite/pidcheck](The DataCite PidCheck)
* [https://docs.scrapy.org/en/1.6/intro/tutorial.html](The Scrapy tutorial)

Use: ```scrapy crawl resfam -o resfam-20200520.csv &> logs-resfam-20200520.txt

This will store the resulting CSV with the check results in resfam-20200520.csv and store verbose logs in logs-resfam-20200520.txt

See the output directory for some examples of output and log files.

