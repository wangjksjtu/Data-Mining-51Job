import pandas as pd
import re
import numpy as np
import sklearn as sk
from sklearn.model_selection import train_test_split
from sklearn import metrics
import time
import pickle as pickle
from scipy import interp
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve

# read data from csv and do some pre-processing
def readData():
    dataFrame = pd.read_csv('data/data-full.csv')
    newDataFrame = pd.DataFrame()


    # area preprocess, cluster into areas such as Beijing, Shanghai, etc
    area = []
    # the city list for matching
    areaMatchList = ["上海","北京","深圳","香港","广州","东莞","杭州","宁波","武汉","天津",
                 "广东","佛山","国外","合肥","惠州","嘉兴","昆山","珠海","无锡","西安"]
    for i in range(len(dataFrame['area'])):
        endTag = False
        for item in areaMatchList:
            if re.compile(item).search(dataFrame['area'][i]): # if matches a city
                area.append(item)
                endTag = True
                break
        if not endTag: # if no city is matched
            area.append("其他")
    # append result in newDF
    newDataFrame.insert(loc=len(newDataFrame.columns), column="area", value=area)


    # detail area preprocess, another col only for Beijing,Shanghai,Guangzhou Hangzhou, and Shenzhen
    detailAreaMatchList = ["上海","北京","广州","深圳","杭州"]
    detailArea = []
    for i in range(len(dataFrame['area'])):
        endTag = False
        for item in detailAreaMatchList:
            if re.compile(item).search(dataFrame['area'][i]): # if matches a city
                if re.compile("-").search(dataFrame['area'][i]):
                    # append the detailed district area of the area
                    detailArea.append(dataFrame['area'][i].split("-")[1])
                else:
                    detailArea.append("no detail")
                endTag = True
                break
        if endTag == False: # if no city is matched
            detailArea.append("null")
    # append result in newDF
    newDataFrame.insert(loc=len(newDataFrame.columns), column="area_detail", value=detailArea)


    # append the company scale in newDF
    newDataFrame.insert(loc=len(newDataFrame.columns), column="company_people", value=dataFrame['company_people'])
    

    # company service, with two rows
    companyService1 = []
    companyService2 = []
    for i in range(len(dataFrame['company_service'])):
        if re.compile(",").search(dataFrame['company_service'][i]): # if company has two types
            # split the service into two cols
            tmp = dataFrame['company_service'][i].split(",")
            companyService1.append(tmp[0])
            companyService2.append(tmp[1])
        else: # if company has only one service
            companyService1.append(dataFrame['company_service'][i])
            companyService2.append("null")
    # add two cols into newDF
    newDataFrame.insert(loc=len(newDataFrame.columns), column="company_service_1", value=companyService1)
    newDataFrame.insert(loc=len(newDataFrame.columns), column="company_service_2", value=companyService2)
    

    # append the company type in newDF
    newDataFrame.insert(loc=len(newDataFrame.columns), column="company_type", value=dataFrame['company_type'])


    # append the education in newDF
    newDataFrame.insert(loc=len(newDataFrame.columns), column="education", value=dataFrame['education'])


    # recuit people, with two rows
    recuit = []
    for i in range(len(dataFrame['hire_num'])):
        if dataFrame['hire_num'][i] == "招若干人": # no detail data
            recuit.append(999)
        else: # has people limit
            tmp = dataFrame['hire_num'][i]
            recuit.append(int(tmp[tmp.find("招")+ 1 : tmp.find("人") ]))

    # append the hire_num in newDF
    newDataFrame.insert(loc=len(newDataFrame.columns), column="hire_num", value=recuit)
    

    # job_work_type with two rows
    job1 = []
    job2 = []
    for i in range(len(dataFrame['job_work_type'])):
        if re.compile(",").search(dataFrame['job_work_type'][i]):  # if company has two types
            # split job type into two cols
            tmp = dataFrame['job_work_type'][i].split(",")
            job1.append(tmp[0])
            job2.append(tmp[1])
        else:  # if the job has two types
            job1.append(dataFrame['job_work_type'][i])
            job2.append("null")
    # add two cols into newDF
    newDataFrame.insert(loc=len(newDataFrame.columns), column="job_work_type_1", value=job1)
    newDataFrame.insert(loc=len(newDataFrame.columns), column="job_work_type_2", value=job2)
    

    # language preprocess, cluster into language requirements, etc
    language1 = []
    language2 = []
    # the language list for matching
    languageMatchList = ["普通话","无","德语","英语","日语","西班牙语","法语","粤语"]
    for i in range(len(dataFrame['language'])):
        tmp = dataFrame['language'][i].split()
        add = []
        for j in range(len(tmp)):
            endTag = False
            for item in languageMatchList:
                if re.compile(item).search(tmp[j]):  # if matches a language
                    add.append(item)
                    endTag = True
                    break
            if not endTag:  # if no language is matched
                add.append("其他语言")
        if len(add) == 1:  # one language
            language1.append(add[0])
            language2.append("无")
        else: # two languages
            language1.append(add[0])
            language2.append(add[1])
    # append language preprocess result in newDF
    newDataFrame.insert(loc=len(newDataFrame.columns), column="language_1", value=language1)
    newDataFrame.insert(loc=len(newDataFrame.columns), column="language_2", value=language2)
    

    # append the work_experience in newDF
    newDataFrame.insert(loc=len(newDataFrame.columns), column="work_experience", value=dataFrame['work_experience'])

    # append the welfare in newDF
    newDataFrame.insert(loc=len(newDataFrame.columns), column="welfare", value=dataFrame['welfare'])

    # append the maximum salary per year and minimum salary per year
    minimum = []
    maximum = []
    for i in range(len(dataFrame['salary'])):
        tmp = dataFrame['salary'][i]
        if re.compile('年').search(tmp):
            yearTag = 1    # year salary
        elif re.compile('天').search(tmp):
            yearTag = 300    # day salary
        else:
            yearTag = 12   # month salary

        if re.compile('千').search(tmp):
            multiTag = 1000   # count as 1000
        elif re.compile('元').search(tmp):
            multiTag = 1   # count as 1
        else:
            multiTag = 10000   # count as 10000

        numberIndex = max(tmp.find("千"), tmp.find("元"), tmp.find("万"))
        numberString = tmp[0:numberIndex]
        numberList = numberString.split("-")
        if len(numberList) == 1:
            minimum.append(int(float(numberList[0]) * multiTag * yearTag))
            maximum.append(int(float(numberList[0]) * multiTag * yearTag))
        else:
            minimum.append(int( float(numberList[0]) * multiTag * yearTag))
            maximum.append(int( float(numberList[1]) * multiTag * yearTag))
     # append the maxinum and minimum salary in newDF
    newDataFrame.insert(loc=len(newDataFrame.columns), column="salary_max", value=maximum)
    newDataFrame.insert(loc=len(newDataFrame.columns), column="salary_min", value=minimum)

    newDataFrame.to_csv("data/middleData.csv",index = False,encoding='gbk')


# precess the middleData
def processMiddleData():
    dataFrame = pd.read_csv('data/middleData.csv',encoding = "gbk")
    newDataFrame = pd.DataFrame()


    # process company people
    newDataFrame.insert(loc=len(newDataFrame.columns), column="company_people", value=dataFrame['company_people'])
    # list to be replaced
    replaced = ["少于50人","50-150人","150-500人","500-1000人","1000-5000人","5000-10000人","10000人以上"]
    # list to replace
    replacing = [0,50,150,500,1000,5000,10000]
    for i in range(len(replaced)):
        newDataFrame['company_people'].loc[newDataFrame['company_people'] == replaced[i]] = replacing[i]


    # process education
    newDataFrame.insert(loc=len(newDataFrame.columns), column="education", value=dataFrame['education'])
    # list to be replaced
    replaced = ["无", "初中及以下", "中技", "中专", "高中", "大专", "本科","硕士","博士"]
    # list to replace
    replacing = [3, 0, 1, 1, 2, 2, 4, 6, 9]
    for i in range(len(replaced)):
        newDataFrame['education'].loc[newDataFrame['education'] == replaced[i]] = replacing[i]


    # process experience
    newDataFrame.insert(loc=len(newDataFrame.columns), column="work_experience", value=dataFrame['work_experience'])
    # list to be replaced
    replaced = ["无工作经验", "1年经验", "2年经验", "3-4年经验", "5-7年经验", "8-9年经验", "10年以上经验"]
    # list to replace
    replacing = [0, 1, 2, 3.5, 6, 8.5, 11]
    for i in range(len(replaced)):
        newDataFrame['work_experience'].loc[newDataFrame['work_experience'] == replaced[i]] = replacing[i]
    

    # process hire num
    newDataFrame.insert(loc=len(newDataFrame.columns), column="hire_num", value=dataFrame['hire_num'])
    newDataFrame['hire_num'].loc[ newDataFrame['hire_num'] == 999 ] = 1


    # process salary
    newDataFrame.insert(loc=len(newDataFrame.columns), column="salary_min", value=dataFrame['salary_min'])
    newDataFrame.insert(loc=len(newDataFrame.columns), column="salary_max", value=dataFrame['salary_max'])


    # one-hot cols
    onehotCols = ["area","area_detail","company_type"]
    for col in onehotCols:
        newDataFrame.insert(loc=len(newDataFrame.columns), column=col, value=dataFrame[col])
    newDataFrame = pd.get_dummies(newDataFrame, columns=onehotCols)
    

    # process welfare types
    welfare = []   # name of all welfares
    welfareNum = []  # number of all welfares
    for i in range(len(dataFrame['welfare'])):
        if not isinstance(dataFrame['welfare'][i],str): # some no-str welfare should be processed
            continue
        tmp = dataFrame['welfare'][i].split(",")
        for item in tmp:
            if item not in welfare: # not in list, append
                welfare.append(item)
                welfareNum.append(1)
            else:
                welfareNum[welfare.index(item)] += 1 # already in list, number++

    finalWelfareList = []  # the final remaining welfare list
    for i in range(len(welfare)):
        if welfareNum[i] > 100:  # remain only welfare that shows up greater than 100
            finalWelfareList.append(welfare[i])

    welfareCollist = [] # the cols of welfares(one-hot)
    for i in range(len(finalWelfareList)):
        welfareCollist.append(len(dataFrame['welfare']) * [0]) # all zero at first
    for i in range(len(dataFrame['welfare'])):
        if not isinstance(dataFrame['welfare'][i],str):
            # some no-str welfare should be processed
            continue
        tmp = dataFrame['welfare'][i].split(",")
        for item in tmp:
            if item in finalWelfareList:
                welfareCollist[finalWelfareList.index(item)][i] = 1 # a welfare exists, add 1
    # add in newDataFrame
    for i in range(len(welfareCollist)):
        newDataFrame.insert(loc=len(newDataFrame.columns), column="welfare_" + finalWelfareList[i],
                            value=welfareCollist[i])
    

    # precess language requirements
    languageMatchList = ["普通话", "德语", "英语", "日语", "西班牙语", "法语", "粤语"]
    languageCollist = []  # the cols of languages(one-hot)
    for i in range(len(languageMatchList)):
        languageCollist.append(len(dataFrame['language_1']) * [0])  # all zero at first
    for i in range(len(dataFrame['language_1'])):
        if dataFrame['language_1'][i] in languageMatchList:
            languageCollist[languageMatchList.index(dataFrame['language_1'][i])][i] = 1
    for i in range(len(dataFrame['language_2'])):
        if dataFrame['language_2'][i] in languageMatchList:
            languageCollist[languageMatchList.index(dataFrame['language_2'][i])][i] = 1
    # add in newDataFrame
    for i in range(len(languageCollist)):
        newDataFrame.insert(loc=len(newDataFrame.columns), column="language_" + languageMatchList[i],
                            value=languageCollist[i])
    

    # process company service
    companyService = [] # all tags of company services
    for i in range(len(dataFrame['company_service_1'])):
        if dataFrame["company_service_1"][i] not in companyService and \
        dataFrame["company_service_1"][i] != "null" and \
        isinstance(dataFrame['company_service_1'][i], str):  # reject the effect of null and nan
            companyService.append(dataFrame['company_service_1'][i])
    for i in range(len(dataFrame['company_service_2'])):
        if dataFrame["company_service_2"][i] not in companyService and \
        dataFrame["company_service_2"][i] != "null" and \
        isinstance(dataFrame['company_service_2'][i], str):  # reject the effect of null and nan
            companyService.append(dataFrame['company_service_2'][i])
    print(companyService)
    print(len(companyService))
    companyServiceCollist = []  # the cols of languages(one-hot)
    for i in range(len(companyService)):
        companyServiceCollist.append(len(dataFrame['company_service_1']) * [0])  # all zero at first
    for i in range(len(dataFrame['company_service_1'])):
        # match services
        tmp = dataFrame['company_service_1'][i]
        if not isinstance(tmp, str):  # reject nan
            continue
        companyServiceCollist[companyService.index(tmp)][i] = 1
        tmp = dataFrame['company_service_2'][i]
        if not isinstance(tmp, str):   # reject nan
            continue
        companyServiceCollist[companyService.index(tmp)][i] = 1
    # add into newDataFrame
    for i in range(len(companyService)):
        newDataFrame.insert(loc=len(newDataFrame.columns), column="company_service_" + companyService[i],
                            value=companyServiceCollist[i])


    # process job_work_type
    filterKeyWords = ['设计','经理','总监','技术','实习','开发',"编辑",'产品','工程','电子','商务',
                      '销售','硬件','软件',"助理","文员","主管","算法","其他","推广","美工","网络","网站",
                      "系统","项目","医","测试","翻译","运营","首席","前端","SEO"]
    jobWorkTypeColist = []
    for i in range(len(filterKeyWords)):
        jobWorkTypeColist.append(len(dataFrame['job_work_type_1']) * [0])  # all zero at first
    for i in range(len(dataFrame['job_work_type_1'])):
        for j in range(len(filterKeyWords)):
            if re.compile(filterKeyWords[j]).search(dataFrame['job_work_type_1'][i]):
                jobWorkTypeColist[j][i] = 1
            if isinstance(dataFrame['job_work_type_2'][i],str) and \
                    re.compile(filterKeyWords[j]).search(dataFrame['job_work_type_2'][i]):
                jobWorkTypeColist[j][i] = 1
    # add into newDataFrame
    for i in range(len(filterKeyWords)):
        newDataFrame.insert(loc=len(newDataFrame.columns), column="job_work_type_" + filterKeyWords[i],
                                value=jobWorkTypeColist[i])

    newDataFrame.to_csv("data/quantityData.csv", index=False, encoding='gbk')



def main():
    #readData()
    processMiddleData()


main()
