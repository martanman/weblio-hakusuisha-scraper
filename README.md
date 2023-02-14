### Outline

A scraper for the Chinese--Japanese dictionary 白水社中国語辞典 hosted by Weblio and found [here](https://cjjc.weblio.jp/category/cgkgj/). Includes a script to convert the scraped data into a [yomichan](https://github.com/FooSoft/yomichan-import) compatible dictionary format for use in yomichan.
e
### Requirements

The python libraries needed can be installed with

```
pip install scrapy html5lib regex
```

[Pandoc](https://pandoc.org/index.html) is also required; used to convert html to plain text.

### Usage

```
python spider.py
```

runs the scraper. It takes about a day to scrape all the pages depending on the value of `DOWNLOAD_DELAY` in `spider.py`. Then run

```
python export.py
```

to create a yomichan compatible dictionary zip file from `entries.jsonl`.


### Disclaimer 

Please don't go around sharing copies of the scraped dictionary for copyright reasons. These scripts are intended for individual use.
