import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from shutil import which



class NetnaijamoviesSpider(scrapy.Spider):
    name = 'netnaijamovies'
    allowed_domains = ['www.thenetnaija.co']
    start_urls = ['https://www.thenetnaija.co']
    
    def __init__(self):
        movie_name = 'x men'
        self.chrome_option = Options()
        self.chrome_option.add_argument('--headless')
        driver = webdriver.Chrome(executable_path=which('chromedriver'), options=self.chrome_option)
        driver.get("https://www.thenetnaija.co")

        search_btn = driver.find_element_by_xpath('//*[@id="search-anchor"]')
        search_btn.click()

        search_box = driver.find_element_by_xpath("//form[@class='app-header-search open']")
        if search_box:
            search_input = driver.find_element_by_xpath('//*[@id="ahs-i-text"]')
            search_input.send_keys(movie_name)
            search_input.send_keys(Keys.ENTER)

        self.html = driver.page_source
        driver.close()


    def parse(self, response):
        resp = Selector(text=self.html)
        results = resp.xpath("//article[@class='sr-one']")
        for link in results:
            if_startwith_movie = link.xpath(".//div[@class='info']/h3/a/text()").get()
            # print(if_startwith_movie)
            if if_startwith_movie.startswith('Movie:'):
                yield response.follow(link.xpath(".//div[@class='info']/h3/a/@href").get(), callback=self.parse_movie_link)

    def parse_movie_link(self, response):
        movie_url = response.xpath("//a[@title='Download Video']/@href").get()
        absolute_url = response.urljoin(movie_url)
        yield {
            'TARGET URL': absolute_url
        }

    # def download_url(self, response):
    #     get_link = response.meta['link']
    #     download_driver = webdriver.Chrome(executable_path=which('chromedriver'), options=self.chrome_option)
    #     download_driver.get(get_link)
    #     download_btn = download_driver.find_element_by_xpath('//*[@id="action-buttons"]/button')
    #     download_btn.click()
    #     time.sleep(3)
    #     download_link = download_driver.find_element_by_xpath("//strong/a[@class='download-url']").get()
    #     if download_link:
    #         yield {'TARGET LINK': download_link}

