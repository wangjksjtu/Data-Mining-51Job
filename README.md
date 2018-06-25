# Data-Mining-51Job
This repository is established to explore the data on [51Job website](https://www.51job.com/), where a number of companies poster their wanted positions, and at the same time employees could share their own profiles to boost their career development. Overall, the work in this repo could be summarized in following aspects: 

- Collect the job information using python crawler. 
- Preprocess the data (clean, discretize, match, normalize, etc).
- Conduct feature engineering to analyse the data.
- Design two tasks for real scenarios (salary and job type prediction).
- Apply various machine learning algorithms to our tasks.

## Requirements
- [scrapy](https://scrapy.org/) (web crawling)
- [numpy](http://www.numpy.org/) and [pandas](http://pandas.pydata.org/) (data preprocessing)
- [scikit-learn](http://scikit-learn.org/stable/index.html) (ML-algorithms)
- [matplotlib](https://matplotlib.org/) and [seaborn](https://seaborn.pydata.org/index.html) (data visualization)

## QuickStart
### Web Crawling
### Data Preprocessing
We use python libraries [pandas](http://pandas.pydata.org/) (using class dataframe) and re to preprocess the raw data. See /preprocess/preprocess.py for code.
You can find the preprocessed data in /data, where middleData.csv is the preprocessed data suitable for drawing pics,
 while quantityData.csv quantifies all data and fits further data analysis.

### Feature Engineering

See directory ```/pics```.
 We analyzed feature coorelation and feature distribution respectively. We found two some main features which affect salary level: education level requirements, work experience requirements and area location.

### Salary Prediction

| Model | Accuracy / % | time / s 
| :---- |:------------:| :----: |
| SVR | 123 | 123 |

### Job Area Prediction

| Model | Accuracy / % | time / s 
| :---- |:------------:| :----: |
| SVM (RBF) | 123 | 123 |
| KNN | 123 | 123 |
| XGBoost | 123 | 123 | 


The accuracy & time plot of the above models:

<figure class="half">
    <img src="./figures/acc.png" width="70%">
</figure>



## Team Members
- [Jingkang Wang](https://github.com/wangjksjtu)
- [Jilai Zheng](https://github.com/zhengjilai)
- [Qingzhao Zhang](https://github.com/zqzqz)
- [Lei Wang]()
- [Jinrui Sha]()
- [Zhongwei Chen]()

