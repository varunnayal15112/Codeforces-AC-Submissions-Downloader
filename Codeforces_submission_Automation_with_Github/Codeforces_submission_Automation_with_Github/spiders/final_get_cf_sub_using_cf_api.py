#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 20:06:03 2018

@author: vicky
"""

import requests
import scrapy
from urllib.request import urlopen
import os.path

class CodeforcesSpider(scrapy.Spider):
    #spider name
    name = 'final_cf_submissions'
    user_submissions_data = []
    total_count=0
    
    def start_requests(self):
        username = input("Enter a CF User Handle : ")
        response = requests.get("http://codeforces.com/api/user.info?handles=" + username)
        user_info = response.json()
        print (user_info['status'])
        if(user_info['status']=="FAILED"):
            print ("Status : < User with given handle does not exists >")
        else:
            response = requests.get("http://codeforces.com/api/user.status?handle=" + username)
            user_submission_info = response.json()
            if(user_submission_info['status']!="OK"):
                print ("Status : < No Submissions to retrieve >")
            else:
                total_count_of_submission = len(user_submission_info['result'])
                print (total_count_of_submission)
                
                start_urls = []
                for i in range(0,total_count_of_submission):
                    data = []
                    
                    submissionId = user_submission_info['result'][i]['id']
                    data.append(submissionId)
                    
                    contestId = user_submission_info['result'][i]['contestId']
                    data.append(contestId)
                    
                    index = user_submission_info['result'][i]['problem']['index']
                    data.append(index)
                    
                    problemName = user_submission_info['result'][i]['problem']['name']
                    data.append(problemName)
                    
                    problemTags = user_submission_info['result'][i]['problem']['tags']
                    data.append(problemTags)
                    
                    programmingLanguage = user_submission_info['result'][i]['programmingLanguage']
                    data.append(programmingLanguage)
                    
                    verdict = user_submission_info['result'][i]['verdict']
                    data.append(verdict)
                   
                    self.user_submissions_data.append(data)
                    
                    if(problemTags!=[] and verdict=="OK"):
                        url = "http://codeforces.com/contest/"+str(contestId)+"/submission/"+str(submissionId)
                        start_urls.append(url)
                        
                print (start_urls)
                for url in start_urls:
                    yield scrapy.Request(url=url,meta={'dont_redirect': True,"handle_httpstatus_list": [302,[301]]},callback=self.parse_userSubmission_info,dont_filter=True)
                print (self.user_submissions_data)
                             
    def parse_userSubmission_info(self,response):
        self.total_count+=1
        code = response.xpath('.//*[@id="pageContent"]/div[3]/pre/text()').extract_first()
        submissionId = response.xpath('.//*[@id="pageContent"]//td/text()').extract_first()
        print (code)
        print (self.total_count)
        for data in self.user_submissions_data:
            if str(submissionId) == str(data[0]):
                file_name=str(data[1])+str(data[2])+".txt"
                if(os.path.isfile("/home/vicky/Desktop/Desktop_mera/Codeforces_submission_Automation_with_Github/Codeforces/AC_SUBMISSIONS/"+file_name)==False):
                    print("file created")
                    with open("/home/vicky/Desktop/Desktop_mera/Codeforces_submission_Automation_with_Github/Codeforces/AC_SUBMISSIONS/"+file_name,'a') as f:
                        header = "/*\n\tSubmissionId\t:\t"+str(data[0])+"\n\tContestId\t:\t"+str(data[1])+"\n\tIndex\t:\t"+str(data[2])+"\n\tProblemName\t:\t"+str(data[3])+"\n\tProblemTags\t:\t"+str(data[4])+"\n\tProgrammingLanguage\t:\t"+str(data[5])+"\n\tVerdict\t:\t"+str(data[6])+"\n*/\n\n"
                        f.write(header)
                        f.write(code)
                
