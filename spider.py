import regex as re
import subprocess
import scrapy
from lxml.html import fromstring, tostring
from scrapy.http import TextResponse

index_url_base = "https://cjjc.weblio.jp/category/cgkgj/"


class entryspider(scrapy.Spider):
    name = "entries"
    # def __init__(self, links=[], *args, **kwargs):
    #     super(entryspider, self).__init__(*args, **kwargs)
    #     self.start_urls = links

    def start_requests(self):
        start_urls = [index_url_base + x for x in "abcdefghijklmnopqrstuvwxyz"]
        for s in start_urls:
            yield scrapy.Request(url=s, callback=self.parse_index, errback=self.err_index)

    def parse_index(self, response: TextResponse):  # parses index pages
        next_page = response.xpath(
            '//*[@id="main"]/div[4]/div[1]/span/a[text()="次へ＞"]/@href')
        for nextp in next_page:  # should be 0 or 1
            yield response.follow(nextp, callback=self.parse_index, errback=self.err_index)

        # should be two for two colums
        for entry in response.xpath('//*[@id="main"]/div[4]/div[2]/ul[position()>1]/li/a'):

            if re.fullmatch(r'\p{Han}*', entry.attrib["title"]):
                yield response.follow(entry, callback=self.parse_ent, cb_kwargs=dict(title=entry.attrib["title"]), errback=self.err_ent)

    def parse_ent(self, response: TextResponse, title):
        root = fromstring(response.text)
        elements = root.xpath(
            '//*[@id="main"]/descendant::a[text()="白水社 中国語辞典"]/ancestor::table[@class="wrp"]/following-sibling::div[@class="kijiWrp"][1]/div[@class="kiji"]/div[@class="Cgkgj" and child::*[1][@class="cgkgjC"]]')
        for i, e in enumerate(elements):
            midashigo = ''.join(
                e.xpath('.//preceding-sibling::h2[@class="midashigo"][1]//text()'))

            for lvl in e.xpath('.//div[@class="level0"]'):  # for 1, 2, 3, 4
                xx = lvl.xpath('.//p[@class="lvlNH" or @class="lvlNHN"]')
                for x in xx:
                    y = lvl.xpath('.//p[@class="lvlB"]')[0]
                    xtext = x.xpath('.//text()')
                    y.text = (''.join(xtext) + " " if xtext else "") + \
                        (str(y.text) if y.text else '')
                    x.drop_tree()

            text = subprocess.check_output(
                ["pandoc", "--from=html", "--to=plain", "--wrap=none"],
                input=tostring(e)).decode()

            text = text.replace("\n\n", "\n")

            yield {
                "type": "success",
                "url": response.url,
                "title": title,
                "midashigo": midashigo,
                "text": text,
                "entry": i,
            }

    def err_index(self, failure):
        err = {
            "type": "index_error",
            "url": failure.request.url,
        }
        yield err

    def err_ent(self, failure):
        yield {
            "type": "error",
            "url": failure.request.url,
            "title": failure.request.cb_kwargs["title"]
        }


if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess(settings={
        "FEEDS": {
            "entries.jsonl": {"format": "jsonl"},
        },
        "DOWNLOAD_DELAY": 0.8,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 20,
        "TELNETCONSOLE_ENABLED": False,
    })
    process.crawl(entryspider)
    process.start()
