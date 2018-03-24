from scrapy import cmdline

cmdline.execute("scrapy crawl douban_movie_top250 -o douban.csv".split())

# scrapy crawl firstspider -o items.json -t json