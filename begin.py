from scrapy import cmdline

cmdline.execute("scrapy crawl taobao".split())

# scrapy crawl firstspider -o items.json -t json