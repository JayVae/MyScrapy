from scrapy import cmdline

cmdline.execute("scrapy crawl FGW -o items.csv -t csv".split())

# scrapy crawl firstspider -o items.json -t json