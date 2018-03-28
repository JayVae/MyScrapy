from scrapy import cmdline

cmdline.execute("scrapy crawl FGW".split())

# scrapy crawl firstspider -o items.json -t json