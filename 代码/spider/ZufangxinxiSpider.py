# 数据爬取文件

import scrapy
import pymysql
import pymssql
from ..items import ZufangxinxiItem
import time
import re
import random
import platform
import json
import os
from urllib.parse import urlparse
import requests
import emoji

# 租房信息
class ZufangxinxiSpider(scrapy.Spider):
    name = 'zufangxinxiSpider'
    spiderUrl = 'https://bj.zu.anjuke.com/fangyuan/p{}'
    start_urls = spiderUrl.split(";")
    protocol = ''
    hostname = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start_requests(self):

        plat = platform.system().lower()
        if plat == 'linux' or plat == 'windows':
            connect = self.db_connect()
            cursor = connect.cursor()
            if self.table_exists(cursor, '85tlv_zufangxinxi') == 1:
                cursor.close()
                connect.close()
                self.temp_data()
                return

        pageNum = 1 + 1
        for url in self.start_urls:
            if '{}' in url:
                for page in range(1, pageNum):
                    next_link = url.format(page)
                    yield scrapy.Request(
                        url=next_link,
                        callback=self.parse
                    )
            else:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse
                )

    # 列表解析
    def parse(self, response):
        
        _url = urlparse(self.spiderUrl)
        self.protocol = _url.scheme
        self.hostname = _url.netloc
        plat = platform.system().lower()
        if plat == 'windows_bak':
            pass
        elif plat == 'linux' or plat == 'windows':
            connect = self.db_connect()
            cursor = connect.cursor()
            if self.table_exists(cursor, '85tlv_zufangxinxi') == 1:
                cursor.close()
                connect.close()
                self.temp_data()
                return

        list = response.css('div#list-content div.zu-itemmod')
        
        for item in list:

            fields = ZufangxinxiItem()



            fields["laiyuan"] = self.remove_html(item.css('a.img::attr(href)').extract_first())
            fields["fengmian"] = self.remove_html(item.css('img.thumbnail::attr(lazy_src)').extract_first())
            fields["biaoti"] = self.remove_html(item.css('div.zu-info h3 a b.strongbox::text').extract_first())

            detailUrlRule = item.css('a.img::attr(href)').extract_first()
            if self.protocol in detailUrlRule:
                pass
            elif detailUrlRule.startswith('//'):
                detailUrlRule = self.protocol + ':' + detailUrlRule
            else:
                detailUrlRule = self.protocol + '://' + self.hostname + detailUrlRule
                fields["laiyuan"] = detailUrlRule

            yield scrapy.Request(url=detailUrlRule, meta={'fields': fields},  callback=self.detail_parse)


    # 详情解析
    def detail_parse(self, response):
        fields = response.meta['fields']

        try:
            if '(.*?)' in '''span.price''':
                fields["yuezu"] = re.findall(r'''span.price''', response.text, re.S)[0].strip()
            else:
                if 'yuezu' != 'xiangqing' and 'yuezu' != 'detail' and 'yuezu' != 'pinglun' and 'yuezu' != 'zuofa':
                    fields["yuezu"] = self.remove_html(response.css('''span.price''').extract_first())
                else:
                    fields["yuezu"] = emoji.demojize(response.css('''span.price''').extract_first())
        except:
            pass


        try:
            if '(.*?)' in '''ul[class="house-info-zufang cf"] li:nth-child(2) span.info''':
                fields["huxing"] = re.findall(r'''ul[class="house-info-zufang cf"] li:nth-child(2) span.info''', response.text, re.S)[0].strip()
            else:
                if 'huxing' != 'xiangqing' and 'huxing' != 'detail' and 'huxing' != 'pinglun' and 'huxing' != 'zuofa':
                    fields["huxing"] = self.remove_html(response.css('''ul[class="house-info-zufang cf"] li:nth-child(2) span.info''').extract_first())
                else:
                    fields["huxing"] = emoji.demojize(response.css('''ul[class="house-info-zufang cf"] li:nth-child(2) span.info''').extract_first())
        except:
            pass


        try:
            if '(.*?)' in '''ul[class="house-info-zufang cf"] li:nth-child(5) span.info''':
                fields["louceng"] = re.findall(r'''ul[class="house-info-zufang cf"] li:nth-child(5) span.info''', response.text, re.S)[0].strip()
            else:
                if 'louceng' != 'xiangqing' and 'louceng' != 'detail' and 'louceng' != 'pinglun' and 'louceng' != 'zuofa':
                    fields["louceng"] = self.remove_html(response.css('''ul[class="house-info-zufang cf"] li:nth-child(5) span.info''').extract_first())
                else:
                    fields["louceng"] = emoji.demojize(response.css('''ul[class="house-info-zufang cf"] li:nth-child(5) span.info''').extract_first())
        except:
            pass


        try:
            if '(.*?)' in '''ul[class="house-info-zufang cf"] li:nth-child(3) span.info''':
                fields["mianji"] = re.findall(r'''ul[class="house-info-zufang cf"] li:nth-child(3) span.info''', response.text, re.S)[0].strip()
            else:
                if 'mianji' != 'xiangqing' and 'mianji' != 'detail' and 'mianji' != 'pinglun' and 'mianji' != 'zuofa':
                    fields["mianji"] = self.remove_html(response.css('''ul[class="house-info-zufang cf"] li:nth-child(3) span.info''').extract_first())
                else:
                    fields["mianji"] = emoji.demojize(response.css('''ul[class="house-info-zufang cf"] li:nth-child(3) span.info''').extract_first())
        except:
            pass


        try:
            if '(.*?)' in '''ul[class="house-info-zufang cf"] li:nth-child(6) span.info''':
                fields["zhuangxiu"] = re.findall(r'''ul[class="house-info-zufang cf"] li:nth-child(6) span.info''', response.text, re.S)[0].strip()
            else:
                if 'zhuangxiu' != 'xiangqing' and 'zhuangxiu' != 'detail' and 'zhuangxiu' != 'pinglun' and 'zhuangxiu' != 'zuofa':
                    fields["zhuangxiu"] = self.remove_html(response.css('''ul[class="house-info-zufang cf"] li:nth-child(6) span.info''').extract_first())
                else:
                    fields["zhuangxiu"] = emoji.demojize(response.css('''ul[class="house-info-zufang cf"] li:nth-child(6) span.info''').extract_first())
        except:
            pass


        try:
            if '(.*?)' in '''ul[class="house-info-zufang cf"] li:nth-child(4) span.info''':
                fields["chaoxiang"] = re.findall(r'''ul[class="house-info-zufang cf"] li:nth-child(4) span.info''', response.text, re.S)[0].strip()
            else:
                if 'chaoxiang' != 'xiangqing' and 'chaoxiang' != 'detail' and 'chaoxiang' != 'pinglun' and 'chaoxiang' != 'zuofa':
                    fields["chaoxiang"] = self.remove_html(response.css('''ul[class="house-info-zufang cf"] li:nth-child(4) span.info''').extract_first())
                else:
                    fields["chaoxiang"] = emoji.demojize(response.css('''ul[class="house-info-zufang cf"] li:nth-child(4) span.info''').extract_first())
        except:
            pass


        try:
            if '(.*?)' in '''ul[class="house-info-zufang cf"] li:nth-child(8)''':
                fields["xiaoqu"] = re.findall(r'''ul[class="house-info-zufang cf"] li:nth-child(8)''', response.text, re.S)[0].strip()
            else:
                if 'xiaoqu' != 'xiangqing' and 'xiaoqu' != 'detail' and 'xiaoqu' != 'pinglun' and 'xiaoqu' != 'zuofa':
                    fields["xiaoqu"] = self.remove_html(response.css('''ul[class="house-info-zufang cf"] li:nth-child(8)''').extract_first())
                else:
                    fields["xiaoqu"] = emoji.demojize(response.css('''ul[class="house-info-zufang cf"] li:nth-child(8)''').extract_first())
        except:
            pass


        try:
            if '(.*?)' in '''div.auto-general''':
                fields["xiangqing"] = re.findall(r'''div.auto-general''', response.text, re.S)[0].strip()
            else:
                if 'xiangqing' != 'xiangqing' and 'xiangqing' != 'detail' and 'xiangqing' != 'pinglun' and 'xiangqing' != 'zuofa':
                    fields["xiangqing"] = self.remove_html(response.css('''div.auto-general''').extract_first())
                else:
                    fields["xiangqing"] = emoji.demojize(response.css('''div.auto-general''').extract_first())
        except:
            pass




        return fields

    # 去除多余html标签
    def remove_html(self, html):
        if html == None:
            return ''
        pattern = re.compile(r'<[^>]+>', re.S)
        return pattern.sub('', html).strip()

    # 数据库连接
    def db_connect(self):
        type = self.settings.get('TYPE', 'mysql')
        host = self.settings.get('HOST', 'localhost')
        port = int(self.settings.get('PORT', 3306))
        user = self.settings.get('USER', 'root')
        password = self.settings.get('PASSWORD', '123456')

        try:
            database = self.databaseName
        except:
            database = self.settings.get('DATABASE', '')

        if type == 'mysql':
            connect = pymysql.connect(host=host, port=port, db=database, user=user, passwd=password, charset='utf8')
        else:
            connect = pymssql.connect(host=host, user=user, password=password, database=database)

        return connect

    # 断表是否存在
    def table_exists(self, cursor, table_name):
        cursor.execute("show tables;")
        tables = [cursor.fetchall()]
        table_list = re.findall('(\'.*?\')',str(tables))
        table_list = [re.sub("'",'',each) for each in table_list]

        if table_name in table_list:
            return 1
        else:
            return 0

    # 数据缓存源
    def temp_data(self):

        connect = self.db_connect()
        cursor = connect.cursor()
        sql = '''
            insert into zufangxinxi(
                laiyuan
                ,fengmian
                ,biaoti
                ,yuezu
                ,huxing
                ,louceng
                ,mianji
                ,zhuangxiu
                ,chaoxiang
                ,xiaoqu
                ,xiangqing
            )
            select
                laiyuan
                ,fengmian
                ,biaoti
                ,yuezu
                ,huxing
                ,louceng
                ,mianji
                ,zhuangxiu
                ,chaoxiang
                ,xiaoqu
                ,xiangqing
            from 85tlv_zufangxinxi
            where(not exists (select
                laiyuan
                ,fengmian
                ,biaoti
                ,yuezu
                ,huxing
                ,louceng
                ,mianji
                ,zhuangxiu
                ,chaoxiang
                ,xiaoqu
                ,xiangqing
            from zufangxinxi where
             zufangxinxi.laiyuan=85tlv_zufangxinxi.laiyuan
            and zufangxinxi.fengmian=85tlv_zufangxinxi.fengmian
            and zufangxinxi.biaoti=85tlv_zufangxinxi.biaoti
            and zufangxinxi.yuezu=85tlv_zufangxinxi.yuezu
            and zufangxinxi.huxing=85tlv_zufangxinxi.huxing
            and zufangxinxi.louceng=85tlv_zufangxinxi.louceng
            and zufangxinxi.mianji=85tlv_zufangxinxi.mianji
            and zufangxinxi.zhuangxiu=85tlv_zufangxinxi.zhuangxiu
            and zufangxinxi.chaoxiang=85tlv_zufangxinxi.chaoxiang
            and zufangxinxi.xiaoqu=85tlv_zufangxinxi.xiaoqu
            and zufangxinxi.xiangqing=85tlv_zufangxinxi.xiangqing
            ))
            limit {random.randint(20, 30)}
        '''

        cursor.execute(sql)
        connect.commit()

        connect.close()
