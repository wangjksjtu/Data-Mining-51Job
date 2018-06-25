# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Job51SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job = scrapy.Field()
    area = scrapy.Field()
    company = scrapy.Field()
    company_type = scrapy.Field()
    company_people = scrapy.Field()
    company_service = scrapy.Field()
    salary = scrapy.Field()
    welfare = scrapy.Field()

    # <span class="sp4"><em class="i1"></em>1年经验</span>
    # <span class="sp4"><em class="i2"></em>大专</span>
	# <span class="sp4"><em class="i3"></em>招5人</span>
	# <span class="sp4"><em class="i4"></em>06-19发布</span>
    work_experience = scrapy.Field() #i1
    education = scrapy.Field() #i2
    hire_num = scrapy.Field() #i3
    put_time = scrapy.Field() #i4

    # <span class="sp2" title="英语一般"><em class="i5"></em>英语一般</span>
    language = scrapy.Field()

    #<span class="sp2" title="行政管理 人力资源管理"><em class="i6"></em>行政管理 人力资源管理</span>
    demand_profession = scrapy.Field()

    job_info = scrapy.Field()
    job_work_type = scrapy.Field()
    job_keyword = scrapy.Field()