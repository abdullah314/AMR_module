#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 12:21:53 2018

@author: lssd
"""
# FUNCTION DEFINITION

##=========================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib as mpl
import re
import os
import datetime

#import excel file
def import_file1(directory,file,sheet1):
    import os
    # Change directory 
    os.chdir(directory)
    # Load spreadsheet
    xl = pd.ExcelFile(file)
    # Load a sheet into a DataFrame by name: df1
    df1 = xl.parse(sheet1)
    return df1;



# Calculate how many days the date (all_dates) from a given year (year_0)
def date_to_number(all_dates,year_0):
        
    modified_all_dates=[]
    new_year_day = pd.Timestamp(year=year_0, month=1, day=1)
        
    for i in range(all_dates.size):
        date = pd.to_datetime(all_dates[i], format='%m/%d/%Y')
        modified_all_dates.append((date - new_year_day).days + 1)
    
    #change date column
    return modified_all_dates;

#calculate frequency and percentage of Resistance/Sensitivity
def AMR_Trend_year(df1,antibiotic_names, start_year=2005, end_year=2018, freq=False):
    """
    
    arguments
    =========
    df: DataFrame containing antibiotic resistance data
    antibiotic_names: list of antibiotics (should exist as columns in df)
    start_year: integer specifing the begining of temporal region of interest 
    end_year: integer specifing the end of temporal region of interest
    freq: logical True or False, if True  calculate frequency and if False calculate percent resistance
    returns
    =======
    if freq is True: Returns yearwise frequency of Resistance, Sensitive and Intermediate
    if freq is False: Returns yearwise percent Resistance, Sensitive and Intermediate
    
    """
    df1['Date']=pd.to_datetime(df1['Date'])

    
    Sensitive_by_Year=pd.DataFrame()
    Resistant_by_Year=pd.DataFrame()
    Intermediate_by_Year=pd.DataFrame()

    
    k_value=0
    
    for k in antibiotic_names:            
        
        S=[]
        R=[]
        I=[]
        k_value=k_value+1
        i_value=0
    
        for i in range(start_year,end_year):
            #selecting the rows for ith month temp_df1
            temp_df1=df1[(df1['Date']>=datetime.datetime( month=1, day=1, year=i)) & (df1['Date']<datetime.datetime(month=1, day=1, year=i+1))]
            if temp_df1[k].isnull().all():
                S.append(0)
                R.append(0)
                I.append(0)
                
            else:
                
                RSI_data=temp_df1.groupby(k).size()
                l=[z for z in RSI_data]
                if freq==False:
                    l_sum=sum(l)
                    RSI_data=RSI_data/l_sum
                if (RSI_data.index == 'S').any():
                    S.append(RSI_data['S'])
                else:
                    S.append(0)
            
                if (RSI_data.index == 'R').any():
                    R.append(RSI_data['R'])
                else:
                    R.append(0)
                    
                    
                if (RSI_data.index == 'I').any(): 
                    I.append(RSI_data['I'])
                else:
                    I.append(0)
                    
                
                i_value=i_value+1
                
    
        Sensitive_by_Year[k]=S
        Resistant_by_Year[k]=R
        Intermediate_by_Year[k]=I
        
        
    return Sensitive_by_Year, Resistant_by_Year, Intermediate_by_Year; 

#like AMR_Trend_year but if the an year matrix is empty (i.e number of cases =0 ) then we get nan for that year instead of 0  
def AMR_Trend_year_nan(df1,antibiotic_names, start_year=2005, end_year=2018, freq=False):
    """
    
    arguments
    =========
    df: DataFrame containing antibiotic resistance data
    antibiotic_names: list of antibiotics (should exist as columns in df)
    start_year: integer specifing the begining of temporal region of interest 
    end_year: integer specifing the end of temporal region of interest
    freq: logical True or False, if True  calculate frequency and if False calculate percent resistance
    returns
    =======
    if freq is True: Returns yearwise frequency of Resistance, Sensitive and Intermediate
    if freq is False: Returns yearwise percent Resistance, Sensitive and Intermediate
    
    """
    
    df1['Date']=pd.to_datetime(df1['Date'])

    
    Sensitive_by_Year=pd.DataFrame()
    Resistant_by_Year=pd.DataFrame()
    Intermediate_by_Year=pd.DataFrame()

    
    k_value=0
    
    for k in antibiotic_names:            
        
        S=[]
        R=[]
        I=[]
        k_value=k_value+1
        i_value=0
    
        for i in range(start_year,end_year):
            #selecting the rows for ith month temp_df1
            temp_df1=df1[(df1['Date']>=datetime.datetime( month=1, day=1, year=i)) & (df1['Date']<datetime.datetime(month=1, day=1, year=i+1))]
            if temp_df1[k].isnull().all():
                S.append(float('NAN'))
                R.append(float('NAN'))
                I.append(float('NAN'))
                
            else:
                
                RSI_data=temp_df1.groupby(k).size()
                l=[z for z in RSI_data]
                if freq==False:
                    l_sum=sum(l)
                    RSI_data=RSI_data/l_sum
                if (RSI_data.index == 'S').any():
                    S.append(RSI_data['S'])
                else:
                    S.append(0)
            
                if (RSI_data.index == 'R').any():
                    R.append(RSI_data['R'])
                else:
                    R.append(0)
                    
                    
                if (RSI_data.index == 'I').any(): 
                    I.append(RSI_data['I'])
                else:
                    I.append(0)
                    
                
                i_value=i_value+1
                
    
        Sensitive_by_Year[k]=S
        Resistant_by_Year[k]=R
        Intermediate_by_Year[k]=I
        
        
    return Sensitive_by_Year, Resistant_by_Year, Intermediate_by_Year; 

      
def AMR_Trend(df1,antibiotic_names, start_year=2005, end_year=2018, interval=365.25, freq=True):

    end_date=(end_year-start_year)*365.25
    del_t=interval
    
    Sensitive_by_Year=pd.DataFrame()
    Resistant_by_Year=pd.DataFrame()
    Intermediate_by_Year=pd.DataFrame()
    Year_i=np.arange(del_t,end_date,del_t)
    
    k_value=0
    
    for k in antibiotic_names:            
        
        S=[]
        R=[]
        I=[]
        k_value=k_value+1
        i_value=0
    
        for i in Year_i:
            #selecting the rows for ith month temp_df1
            temp_df1=df1.loc[(df1['Date'] >=(i-del_t)) & (df1['Date'] < i)]
            if temp_df1[k].isnull().all():
                S.append(0)
                R.append(0)
                I.append(0)
                
            else:
                
                RSI_data=temp_df1.groupby(k).size()
                l=[z for z in RSI_data]
                if freq==True:
                    l_sum=sum(l)
                    RSI_data=RSI_data/l_sum
                if (RSI_data.index == 'S').any():
                    S.append(RSI_data['S'])
                else:
                    S.append(0)
            
                if (RSI_data.index == 'R').any():
                    R.append(RSI_data['R'])
                else:
                    R.append(0)
                    
                    
                if (RSI_data.index == 'I').any(): 
                    I.append(RSI_data['I'])
                else:
                    I.append(0)
                    
                
                i_value=i_value+1
                
    
        Sensitive_by_Year[k]=S
        Resistant_by_Year[k]=R
        Intermediate_by_Year[k]=I
        
        
    return Sensitive_by_Year, Resistant_by_Year, Intermediate_by_Year; 
#like AMR
def AMR_Trend_month(df1,antibiotic_names, start_year=2005, end_year=2018, freq=False):
    """
    Calculate AMR trend on monthly interval 
    arguments
    =========
    df: DataFrame containing antibiotic resistance data
    antibiotic_names: list of antibiotics (should exist as columns in df)
    start_year: integer specifing the begining of temporal region of interest 
    end_year: integer specifing the end of temporal region of interest
    freq: logical True or False, if True  calculate frequency and if False calculate percent resistance
    returns
    =======
    if freq is True: Returns yearwise frequency of Resistance, Sensitive and Intermediate
    if freq is False: Returns yearwise percent Resistance, Sensitive and Intermediate
    
    """
    df1['Date']=pd.to_datetime(df1['Date'])
    total_months=(end_year-start_year)*12
    
    Sensitive_by_Year=pd.DataFrame()
    Resistant_by_Year=pd.DataFrame()
    Intermediate_by_Year=pd.DataFrame()

    
    k_value=0
    
    for k in antibiotic_names:            
        
        S=[]
        R=[]
        I=[]
        k_value=k_value+1
        i_value=0
    
        for i in range(0,total_months):
            y1=i//12
            y2=(i+1)//12
            m1=i%12+1
            m2=(i+1)%12+1
            
            #selecting the rows for ith month temp_df1
            temp_df1=df1[(df1['Date']>=datetime.datetime( month=m1, day=1, year=start_year+y1)) & (df1['Date']<datetime.datetime(month=m2, day=1, year=start_year+y2))]
            if temp_df1[k].isnull().all():
                S.append(0)
                R.append(0)
                I.append(0)
                
            else:
                
                RSI_data=temp_df1.groupby(k).size()
                l=[z for z in RSI_data]
                if freq==False:
                    l_sum=sum(l)
                    RSI_data=RSI_data/l_sum
                if (RSI_data.index == 'S').any():
                    S.append(RSI_data['S'])
                else:
                    S.append(0)
            
                if (RSI_data.index == 'R').any():
                    R.append(RSI_data['R'])
                else:
                    R.append(0)
                    
                    
                if (RSI_data.index == 'I').any(): 
                    I.append(RSI_data['I'])
                else:
                    I.append(0)
                    
                
                i_value=i_value+1
                
    
        Sensitive_by_Year[k]=S
        Resistant_by_Year[k]=R
        Intermediate_by_Year[k]=I
        
        
    return Sensitive_by_Year, Resistant_by_Year, Intermediate_by_Year; 

def integer_to_date(N):
    timestamp = datetime.datetime.fromtimestamp(N)
    return timestamp.strftime('%d-%m-%Y')

def search_organism(orgid,search_list):
    '''you can provide a list of organism'''
    output_list=[]
    for m in search_list:
        for n in orgid:
            if re.match(m,n,re.IGNORECASE):
                output_list.append(n)
    return output_list


def select_organism(df1,org_list):
    '''you can provide a list of organism'''
    set_org=set()
    for o in org_list:
        df2=df1.loc[df1['Orgid']==o]
        set_1=set(df2.index)
        set_org=set_org.union(set_1)
        
    L_org=list(set_org)
    L_org.sort()
       
    df3=df1.loc[L_org,:]
    return df3

def month_year(N,start_year):
    """
    Nth month from start_year is converted to month/year format
    """
    return str(N%12+1)+'/'+str(start_year+N//12)

def plot_AMR(df1,antibiotic_names,start_year,end_year,org_name='',interval=365.25):
   
    if org_name:
        df1=select_organism(df1,org_name)
    else:
        org_name='all'
    
    writer=pd.ExcelWriter('yearwise_antibiotic_resistance.xlsx',engine='xlsxwriter')
    for ab in antibiotic_names:
        S1,R1,_=AMR_Trend(df1,[ab],start_year=start_year, end_year=end_year) 
        R=100*R1[ab]
        fig,ax=plt.subplots(nrows=1,ncols=1)
        mpl.rcParams["font.size"] = 18
        x=range(len(R))
        ax.plot(x,R,linewidth=2)
        ax.set_xlabel('year')
        ax.set_ylabel('percent resistance')
        if interval==30.42:
            ax.set_xticks(np.array(np.arange(0, len(R), 12.0)))
        elif interval==365.25:
            ax.set_xticks(np.array(np.arange(0, len(R), 1)))
        else:
            ax.set_xticks(np.array(np.arange(0, len(R), 365.25/interval)))
        
        print('start year: ' +str(start_year))
        print('end_year: '+str(end_year))
        #ax.xaxis.set_ticks_position(np.arange(min(A.index), max(A.index)+1, 12.0))
        ax.xaxis.set_ticklabels(list(range(start_year,end_year)))
        
        fig.set_size_inches(20, 10)
        # Shrink current axis by 20%
        #ax = plt.subplot(111)
     
        fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
        yticks = mtick.FormatStrFormatter(fmt)
        ax.yaxis.set_major_formatter(yticks)
        regex=re.compile('.*/')
        
        if re.match(regex,ab):
            aa=ab.split('/')
            ab=' or '.join(aa)   
            
        combine_name=''.join(org_name)
        name=combine_name+' '+ab[3:]
        plt.title(name)
        plt.savefig(name+'.png')
        plt.clf()
        R_df=pd.DataFrame()
        R_df['Sensitive']=S1[list(S1)[0]]
        R_df['Resistance']=R1[list(R1)[0]]
        
        if interval==30.42:
            ind=[]
            for ii in R_df.index:
                ind.append(month_year(ii,start_year))
    
            dict_ind=dict(zip(R_df.index,ind))
            R_df=R_df.rename(index=dict_ind)
            
        R_df.to_excel(writer,ab,startrow=0)
        sheet1=writer.sheets[ab]
        sheet1.insert_image('A'+str(len(S1)+5),name+'.png',{'x_scale': 0.5, 'y_scale': 0.5})
        plt.close()
    writer.save()

def plot_AMR_year(df1,antibiotic_names,start_year,end_year,org_name=''):
   
    if org_name:
        df1=select_organism(df1,org_name)
    else:
        org_name='all'
    
    writer=pd.ExcelWriter('yearwise_antibiotic_resistance.xlsx',engine='xlsxwriter')
    for ab in antibiotic_names:
        S1,R1,_=AMR_Trend_year(df1,[ab],start_year=start_year, end_year=end_year) 
        R=100*R1[ab]
        fig,ax=plt.subplots(nrows=1,ncols=1)
        mpl.rcParams["font.size"] = 18
        x=range(len(R))
        ax.plot(x,R,linewidth=2)
        ax.set_xlabel('year')
        ax.set_ylabel('percent resistance')
        ax.set_xticks(np.array(np.arange(0, len(R), 1)))

        
        print('start year: ' +str(start_year))
        print('end_year: '+str(end_year))
        #ax.xaxis.set_ticks_position(np.arange(min(A.index), max(A.index)+1, 12.0))
        ax.xaxis.set_ticklabels(list(range(start_year,end_year)))
        
        fig.set_size_inches(20, 10)
        # Shrink current axis by 20%
        #ax = plt.subplot(111)
     
        fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
        yticks = mtick.FormatStrFormatter(fmt)
        ax.yaxis.set_major_formatter(yticks)
        regex=re.compile('.*/')
        
        if re.match(regex,ab):
            aa=ab.split('/')
            ab=' or '.join(aa)   
            
        combine_name=''.join(org_name)
        name=combine_name+' '+ab[3:]
        plt.title(name)
        plt.savefig(name+'.png')
        plt.clf()
        R_df=pd.DataFrame()
        R_df['Sensitive']=S1[list(S1)[0]]
        R_df['Resistance']=R1[list(R1)[0]]
        
           
        R_df.to_excel(writer,ab,startrow=0)
        sheet1=writer.sheets[ab]
        sheet1.insert_image('A'+str(len(S1)+5),name+'.png',{'x_scale': 0.5, 'y_scale': 0.5})
        plt.close()
    writer.save()
    
def remove_Hosp_Id(df3,col='Hosp_Id'):
    a=df3[col].copy()
    a=a.dropna()
    df4=df3.drop(index=a.index,axis=0)
    return df4

def ordinal_to_date_1(date_data, base_time='2018-01-01'): 
    from datetime import datetime
    d = datetime.strptime(base_time, '%Y-%m-%d').date()
    start_0 = d.toordinal()-1
    all_dates=date_data.copy()
    modified_all_dates=[]
    for ind in all_dates.index:
        dt = datetime.fromordinal(start_0+all_dates.loc[ind])
        new_date='%s/%s/%s' %(dt.month,dt.day,dt.year)
        modified_all_dates.append(new_date)
    
    return modified_all_dates

def plot_AMR_year2(df1,antibiotic_names,start_year,end_year,org_name='',Sex=True):
   
    if org_name:
        df1=select_organism(df1,org_name)
    else:
        org_name='all'
    if Sex:
        df1_m=df1[df1['Sex']=='M']
        df1_f=df1[df1['Sex']=='F']

    if not Sex:
        writer=pd.ExcelWriter('yearwise_antibiotic_resistance.xlsx',engine='xlsxwriter')
        
        
    for ab in antibiotic_names:
        if Sex:
            S1_m,R1_m,_=AMR_Trend_year(df1_m,[ab],start_year=start_year, end_year=end_year) 
            R_m=100*R1_m[ab]      
            S1_f,R1_f,_=AMR_Trend_year(df1_f,[ab],start_year=start_year, end_year=end_year) 
            R_f=100*R1_f[ab]
        else:
            S1,R1,_=AMR_Trend_year(df1,[ab],start_year=start_year, end_year=end_year) 
            R=100*R1[ab]            
            

        fig,ax=plt.subplots(nrows=1,ncols=1)
        mpl.rcParams["font.size"] = 18
        if Sex:
            month_n=len(R_m)
            x=range(month_n)
        else:
            month_n=len(R)
            x=range(len(month_n))
            
        if Sex:
            M_hdle, = ax.plot(x,R_m,linewidth=2, label= 'Male')
            F_hdle, = ax.plot(x,R_f,linewidth=2, label= 'Female')
        else:
            ax.plot(x,R,linewidth=2)
            
            
        
        ax.set_xlabel('year')
        ax.set_ylabel('percent resistance')
        ax.set_xticks(np.array(np.arange(0, month_n, 1)))

        
        print('start year: ' +str(start_year))
        print('end_year: '+str(end_year))
        #ax.xaxis.set_ticks_position(np.arange(min(A.index), max(A.index)+1, 12.0))
        ax.xaxis.set_ticklabels(list(range(start_year,end_year)))
        
        fig.set_size_inches(20, 10)
        # Shrink current axis by 20%
        #ax = plt.subplot(111)
     
        fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
        yticks = mtick.FormatStrFormatter(fmt)
        ax.yaxis.set_major_formatter(yticks)
        regex=re.compile('.*/')
        
        if re.match(regex,ab):
            aa=ab.split('/')
            ab=' or '.join(aa)   
            
        #combine_name=''.join(org_name)
        #name=combine_name+' '+ab[3:]
        name=ab[3:]
        ax.legend(handles=[M_hdle,F_hdle])
        plt.title(name)
        plt.savefig(name+'.png')
        plt.clf()
        if not Sex:
            R_df=pd.DataFrame()
            R_df['Sensitive']=S1[list(S1)[0]]
            R_df['Resistance']=R1[list(R1)[0]]
            
               
            R_df.to_excel(writer,ab,startrow=0)
            sheet1=writer.sheets[ab]
            sheet1.insert_image('A'+str(len(S1)+5),name+'.png',{'x_scale': 0.5, 'y_scale': 0.5})
        plt.close()
    if not Sex:
        writer.save()
