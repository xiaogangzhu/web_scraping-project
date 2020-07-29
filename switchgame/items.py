# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SwitchgameItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    developer = scrapy.Field()
    release_date = scrapy.Field()
    other_platform = scrapy.Field()
    meta_score = scrapy.Field()
    user_score = scrapy.Field()
    genre = scrapy.Field()
    num_of_player = scrapy.Field()
    Rating = scrapy.Field()
    rating_count = scrapy.Field()
    critic_review_count = scrapy.Field()
    users_review_count = scrapy.Field()
    critic_review_attitude = scrapy.Field()
    users_review_attitude = scrapy.Field()