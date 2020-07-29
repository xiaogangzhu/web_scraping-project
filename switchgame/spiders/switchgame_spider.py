from scrapy import Spider,Request
from switchgame.items import SwitchgameItem
import re

class SwitchgameSpider(Spider):
    name = 'switchgame.spider'
    allow_urls = ["https://www.metacritic.com/"]
    start_urls = ["https://www.metacritic.com/browse/games/release-date/available/switch/name"]

    def parse(self,response):
        num_pages = int(response.xpath('//li[@class="page last_page"]/a/text()').extract_first())

        url_list = [f'https://www.metacritic.com/browse/games/release-date/available/switch/name?page={i}' for i in range(num_pages)]
        for url in url_list:
            yield Request(url=url,callback=self.parse_result_page)

    def parse_result_page(self,response):
        game_urls =  response.xpath('//a[@class="title"]/@href').extract()
        game_urls = [f'https://www.metacritic.com{suffix}' for suffix in game_urls]
        #print(len(game_urls))
        for url in game_urls:
            yield Request(url=url,callback=self.parse_game_page)

    def parse_game_page(self,response):
        name =  response.xpath('//div[@class="product_title"]/a/h1/text()').extract_first()

        developer = response.xpath('//li[@class="summary_detail publisher"]//span/a/text()').extract()
        if len(developer)>1:
            developer = [s.strip() for s in developer]
        else:
            developer = developer[0].strip()

        release_date = response.xpath('//li[@class="summary_detail release_data"]/span[@class="data"]/text()').extract_first()

        try:
            other_platform = response.xpath('//li[@class="summary_detail product_platforms"]/span[@class="data"]//a/text()').extract()
        except:
            other_paltform = None
            print('='*50)
            print(f'no other platform')
            print('='*50)

        try:
            meta_score = int(response.xpath('//a[@class="metascore_anchor"]/div/span/text()').extract_first())
        except:
            meta_score = None
            print('='*50)
            print(f'meta_score error with {response.url}')
            print('='*50)



        try:
            user_score = float(response.xpath('//a[@class="metascore_anchor"]/div/text()').extract_first())
        except:
            user_score = None
            print('='*50)
            print(f'user_score error with {response.url}')
            print('='*50)


        genre = response.xpath('//li[@class="summary_detail product_genre"]/span[@class="data"]/text()').extract()

        num_of_player = response.xpath('//li[@class="summary_detail product_players"]/span[@class="data"]/text()').extract_first()

        Rating = response.xpath('//li[@class="summary_detail product_rating"]/span[@class="data"]/text()').extract_first()
        try:
            rating_count = response.xpath('//div[@class="userscore_wrap feature_userscore"]/div/p/span/a/text()').extract_first()
            rating_count = int(re.findall('(\d+) Ratings',rating_count)[0])
        except:
            rating_count = 0
            print('='*50)
            print(f'rating_count error with {response.url}')
            print('='*50)

        attitudes =  response.xpath('//li[@class="score_count"]')
        critic_review_attitude = {attitude.xpath('./div/span/text()').extract_first()[:-1]:int(attitude.xpath('./div//span[@class="count"]/text()').extract_first().replace(',','')) for attitude in attitudes[:3]}
        users_review_attitude = {attitude.xpath('./div/span/text()').extract_first()[:-1]:int(attitude.xpath('./div//span[@class="count"]/text()').extract_first().replace(',','')) for attitude in attitudes[3:6]}

        try:
            critic_review_count = response.xpath('//p[@class="see_all"]/a/text()').extract_first()
            critic_review_count = int(re.findall('See all (\d+) Critic Reviews?',critic_review_count)[0])
        except:
            critic_review_count = sum([critic_review_attitude[key] for key in critic_review_attitude])
            print('='*50)
            print(f'critic_review_count error with {response.url}')
            print('='*50)

        try:
            users_review_count =  response.xpath('//div[@class="module reviews_module user_reviews_module"]/div/p/a/text()').extract_first()
            users_review_count = int(re.findall('See all (\d+) User Reviews?',users_review_count)[0])
        except:
            users_review_count = sum([users_review_attitude[key] for key in users_review_attitude])
            print('='*50)
            print(f'users_review_count error with {response.url}')
            print('='*50)

        

        item = SwitchgameItem()
        item['name'] = name
        item['developer'] = developer
        item['release_date'] = release_date
        item['other_platform'] = other_platform
        item['meta_score'] = meta_score
        item['user_score'] = user_score
        item['genre'] = genre
        item['num_of_player'] = num_of_player
        item['Rating'] = Rating
        item['rating_count'] = rating_count
        item['critic_review_count'] = critic_review_count
        item['users_review_count'] = users_review_count
        item['critic_review_attitude'] = critic_review_attitude
        item['users_review_attitude'] = users_review_attitude

        yield item

