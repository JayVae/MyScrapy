from scrapy import cmdline

cmdline.execute("scrapy crawl FGW -o FGW.csv".split())

# scrapy crawl firstspider -o items.json -t json