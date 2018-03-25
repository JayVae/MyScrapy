from scrapy import cmdline

cmdline.execute("scrapy crawl trans -o xinjiang2.csv".split())

# scrapy crawl firstspider -o items.json -t json