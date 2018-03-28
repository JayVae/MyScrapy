from scrapy import cmdline

cmdline.execute("scrapy crawl scrapy_splash".split())

# scrapy crawl firstspider -o items.json -t json