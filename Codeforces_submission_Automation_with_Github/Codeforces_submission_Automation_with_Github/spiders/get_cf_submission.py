#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 10:00:32 2018

@author: vicky
"""
import requests
import scrapy
from urllib.request import urlopen
from scrapy import log

#import mysql.connector
##database connection
#config = {
#    'user': 'root',
#    'password': 'aitpune411015',
#    'host': '127.0.0.1',
#    'database': 'Ali_Final',
#    'raise_on_warnings': True,
# }
#
#cnx = mysql.connector.connect(**config)
#cursor = cnx.cursor()
#cnx.close()

#from scrapy import log
#
#somedata = response.xpath(my_supper_dupper_xpath)
## we know that this should have captured
## something, so we check
#if not somedata:
#    log.msg("This should never happen, XPath's are all wrong, OMG!", level=log.CRITICAL)
#else:
#    # do your actual parsing of the captured data, 
#    # that we now know exists  

class CodeforcesSpider(scrapy.Spider):
    #spider name
    name = 'cf_submissions'
    username = ""
    
    def start_requests(self):
        #url formed as per user defined category
        global username
        username = self.category
        #user_info = urlopen("http://codeforces.com/api/user.info?handles=" + username)
        response = requests.get("http://codeforces.com/api/user.info?handles=" + username)
        user_info = response.json()
        print (user_info['status'])
        if(user_info['status']=="OK"):
            yield scrapy.Request('http://codeforces.com/submissions/%s' % self.category,callback=self.parse,dont_filter = True)
        else:
            info = {
                    'Status' : '< User with given handle does not exists >'
                    }
            yield info
        
    def parse(self,response):
        
        #Extracting the content using css or xpath selectors
        #username = str(response.xpath('.//*[@class="second-level-menu-list"]/li[1]/a/text()').extract_first())
        token = str(response.xpath('.//*[@class="pagination"]/ul/li[6]/span/a/text()').extract_first())
#        print (token)
        if token=="None":
            no_of_pages = 0
        else:
            no_of_pages = int(token)
        #no_of_pages = response.xpath('.//*[@class="pagination"]/ul/li[6]/span/a/text()').extract_first()
#        print (username,no_of_pages)
        
#        for page in range(1,no_of_pages+1):
#            #calling parse function as per url to scrap information related to the submission page link
#            url = 'http://codeforces.com/submissions/' + username + '/page/' + str(page)
#            print (url)
#            yield scrapy.Request(url=url, callback=self.parse_submission_table,dont_filter = True)  
        url = 'http://codeforces.com/submissions/' + username + '/page/1'
        yield scrapy.Request(url=url, callback=self.parse_submission_table,dont_filter = True)  
     
    def parse_submission_table(self,response):
        submission_id_list = response.xpath('.//*[@class="view-source"]/text()').extract()
        submission_link_list = response.xpath('.//*[@class="view-source"]/@href').extract()
        submission_info = dict()
        value=0
        for key in submission_id_list:
            submission_info[key] = submission_link_list[value]
            value = value+1
#        print (submission_info)
        AC_submission_url = []
        for submission_id in submission_id_list:
            submission_verdict = response.xpath('.//*[@submissionid='+submission_id+']/span/span/text()').extract_first()
            if submission_verdict=="Accepted":
                print (submission_info[submission_id])
                url = "codeforces.com" + submission_info[submission_id]
                AC_submission_url.append(url)
#                print (url)
        for url in AC_submission_url:
            yield scrapy.Request(url=url,callback=self.parse_submission_info,dont_filter = True)
        
    def parse_submission_info(self,response):
        code = response.xpath('.//*[@id="pageContent"]/div[3]/pre/text()').extract_first()
        print (code)
        info={
            'Task' : '< Successfully Done >'
          }
        yield info
        
                
                
                
            
        #response.xpath('.//*[@class="submissionVerdictWrapper"]//span/text()').extract()
        
#        submission_verdict = response.xpath('.//*[@submissionid="33587760"]/span/span/text()').extract_first()
        
#        submission_verdict = response.xpath('.//*[@id="pageContent"]/div[4]/div[6]/table/tbody/tr[3]/td[6]/span/span/text()').extract_first()
#        submission_id = response.xpath('.//*[@class="status-frame-datatable"]/div[6]/table/tbody/tr[3]/td[1]/a/text()').extract_first()
#        print (submission_verdict)
#        print (submission_verdict,submission_id)
#    def parse_product_info(self, response):
#        
#        #Extracting the content using css or xpath selectors
#        url=str(response.xpath('/html/head/meta[7]/@content').extract_first())
#        currency=str(response.xpath('.//*[@class="p-symbol"]/text()').extract_first())
#        price=str(response.xpath('//*[@class="p-price"]/text()').extract_first())
#        if price==' - ':
#            price=str(response.xpath('.//*[@class="p-price"]/span/text()').extract_first())+"-"+str(response.xpath('.//*[@class="p-price"]/span[2]/text()').extract_first())
#        price=currency+price
#        discount_price=str(response.xpath('//*[@id="j-sku-discount-price"]/text()').extract_first())
#        title=str(response.css("title::text").extract_first())
#        product_rating=str(response.xpath('//*[@id="j-customer-reviews-trigger"]/span[2]/text()').extract_first())
#        product_rating_count=str(response.xpath('//*[@id="j-customer-reviews-trigger"]/span[3]/text()').extract_first())             
#        item_specifics=str(response.css(".ui-box.product-property-main span::text").extract())
#        seller_name=str(response.xpath('//*[@id="j-store-info-wrap"]/dl/dd[1]/a/text()').extract_first())
#        
#        print ('URL :',url)
#        #print('CURRENCY :',currency)
#        print ('Price :',price)
#        print ('D_Price :',discount_price)
#        print ('Title :',title)
#        print ('P_Rating :',product_rating)
#        print ('P_R_Count :',product_rating_count)
#        print ('Item_Specifics :',item_specifics)
#        print ('Seller_Name :',seller_name)
#        
#         
#        cursor.execute("""INSERT INTO AliExpress VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""" , (url,price,discount_price,title,product_rating,product_rating_count,item_specifics,seller_name))
#        print ("%d rows were inserted" % cursor.rowcount)        
#        cnx.commit()
#        
#        #create a dictionary to store the scraped info
#        scraped_info = {
#
#            'url' : url,
#            'price' : price,
#            'discount_price' : discount_price,
#            'title' : title,
#            'product_rating' : product_rating,
#            'product_rating_count' : product_rating_count,
#            'item_specifics' : item_specifics,
#            'seller_name' : seller_name,
#        }
#            
#        #yield or give the scraped info to scrapy
#        yield scraped_info


