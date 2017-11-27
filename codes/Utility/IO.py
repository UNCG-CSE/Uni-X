"""
Please share useful function in this file.
"""
import matplotlib
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

"""
The function clean_and_prepare handle a few things as listed below:
(1) merge dataset from different year;
(2) prepare the variables of repayment rate (response variable) as well as other variables (explanatory variables);
(3) drop the empty column and row;
(4) save the final dataset to local .csv file and return the dataset.

Example:
clean_and_prepare()
# after creating .csv file, we can obtain data from file directly
sc= pd.read_csv("../data/sc_final.csv")
"""
def clean_and_prepare():
    # Load csv file into dataframe
    sc96 = pd.read_csv("../data/CollegeScorecard_Raw_Data/MERGED1996_97_PP.csv")
    sc97 = pd.read_csv("../data/CollegeScorecard_Raw_Data/MERGED1997_98_PP.csv")
    sc98 = pd.read_csv("../data/CollegeScorecard_Raw_Data/MERGED1998_99_PP.csv")
    sc99 = pd.read_csv("../data/CollegeScorecard_Raw_Data/MERGED1999_00_PP.csv")
    sc00 = pd.read_csv("../data/CollegeScorecard_Raw_Data/MERGED2000_01_PP.csv")
    sc01 = pd.read_csv("../data/CollegeScorecard_Raw_Data/MERGED2001_02_PP.csv")
    sc02 = pd.read_csv("../data/CollegeScorecard_Raw_Data/MERGED2002_03_PP.csv")
    sc03 = pd.read_csv("../data/CollegeScorecard_Raw_Data/MERGED2003_04_PP.csv")
    sc04 = pd.read_csv("../data/CollegeScorecard_Raw_Data/MERGED2004_05_PP.csv")
    sc05 = pd.read_csv("../data/CollegeScorecard_Raw_Data/MERGED2005_06_PP.csv")
    sc06 = pd.read_csv("../data/CollegeScorecard_Raw_Data/MERGED2006_07_PP.csv")
    sc07 = pd.read_csv("../data/CollegeScorecard_Raw_Data/MERGED2007_08_PP.csv")
    sc08 = pd.read_csv("../data/CollegeScorecard_Raw_Data/MERGED2008_09_PP.csv")
    sc09 = pd.read_csv("../data/CollegeScorecard_Raw_Data/MERGED2009_10_PP.csv")
    sc10 = pd.read_csv("../data/CollegeScorecard_Raw_Data/MERGED2010_11_PP.csv")
    sc11 = pd.read_csv("../data/CollegeScorecard_Raw_Data/MERGED2011_12_PP.csv")
    sc12 = pd.read_csv("../data/CollegeScorecard_Raw_Data/MERGED2012_13_PP.csv")
    sc13 = pd.read_csv("../data/CollegeScorecard_Raw_Data/MERGED2013_14_PP.csv")
    sc14 = pd.read_csv("../data/CollegeScorecard_Raw_Data/MERGED2014_15_PP.csv")
    
    # Load Dictionary
    dic_file=pd.ExcelFile("../data/CollegeScorecardDataDictionary.xlsx")
    dic_init = dic_file.parse("data_dictionary")
    
    # Clean Dictionary
    dic=dic_init.ix[dic_init['VARIABLE NAME'].notnull()]
    
    sc_init=[sc96,sc97,sc98,sc99,sc00,sc01,sc02,sc03,sc04,sc05,sc06,sc07,sc08,sc09,sc10,sc11,sc12,sc13,sc14]
    
    # Add year variable
    for i in range(len(sc_init)):
        sc_init[i]['Year']=i+1996
    
    # Merge dataset with valid repayment information (2007-2014)
    sc_merge=pd.concat(sc_init[11:19])
    
    # Pick x and y variables
    scx_merge=sc_merge.loc[:,dic['VARIABLE NAME'][dic["dev-category"]!="repayment"]]
    scy_merge=sc_merge.loc[:,['RPY_1YR_RT','RPY_3YR_RT','RPY_5YR_RT', 'RPY_7YR_RT'] ]
    
    # Combine x and y variables
    sc=pd.concat([scy_merge,scx_merge,sc_merge['Year']],axis=1)
    
    # Drop empty row and column
    sc_drop=sc.dropna(how="all",axis=1)
    sc_drop=sc_drop.dropna(how="all",axis=0)
    
    # Save it to local file
    sc_drop.to_csv('../data/sc_final.csv')
    
    return sc_drop

def load_dictionary():
    # Load Dictionary
    dic_file=pd.ExcelFile("../data/CollegeScorecardDataDictionary.xlsx")
    dic_init = dic_file.parse("data_dictionary")
    dic=dic_init.loc[dic_init['VARIABLE NAME'].notnull()]
    dic=dic[(dic['API data type']=='integer') | (dic['API data type']=='float')]
    dic=dic[['NAME OF DATA ELEMENT','dev-category','VARIABLE NAME']]
    dic.columns = ['desc', 'category','name']
    return dic

def get_rpyrt_by_class(y=1):
    index={'1':1,'3':2,'5':3,'7':4}
    sc= pd.read_csv("../data/sc_final.csv")
    yname='RPY_'+ str(y) +'YR_RT'
    sc_sub=sc.iloc[:,[index[str(y)]]+range(5,sc.shape[1])]
    sc_sub=sc_sub.convert_objects(convert_numeric=True)
    sc_sub=sc_sub.dropna(subset=[yname])
    pro=0.3
    sc_sub=sc_sub.dropna(axis=0,how='all')
    sc_sub=sc_sub.dropna(axis=1,thresh=np.ceil(sc_sub.shape[1]*(1-pro)))
    sc_sub=sc_sub.drop('SEPAR_DT_MDN',axis=1)
    sc_sub=sc_sub.replace(to_replace='PrivacySuppressed',value=np.NaN)
    return sc_sub

def prescreening_by_class(df, y=1, nobs=500):
    yname='RPY_'+ str(y) +'YR_RT'
    cor=df.corr()
    corr=abs(cor).sort_values([yname],ascending=0)[yname]
    return corr.index[1:(nobs+1)]