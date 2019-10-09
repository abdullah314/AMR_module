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

def import_file1(directory,file,sheet1):
    import os
    # Change directory 
    os.chdir(directory)
    # Load spreadsheet
    xl = pd.ExcelFile(file)
    # Load a sheet into a DataFrame by name: df1
    df1 = xl.parse(sheet1)
    return df1;




def date_to_number(all_dates,year_0):
        
    modified_all_dates=[]
    new_year_day = pd.Timestamp(year=year_0, month=1, day=1)
        
    for i in range(all_dates.size):
        date = pd.to_datetime(all_dates[i], format='%m/%d/%Y')
        modified_all_dates.append((date - new_year_day).days + 1)
    
    #change date column
    return modified_all_dates;


def AMR_Trend_year(df1,antibiotic_names, start_year=2005, end_year=2018, freq=True):
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

def AMR_Trend_month(df1,antibiotic_names, start_year=2005, end_year=2018, freq=True):
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
#specify to whether to sex are differentiated
# =============================================================================
# sex_differ=0
# 
# #import excel file 
# directory="/home/ahmed/lssd_home/Abdullah/antibiotic data/antibiotic september 2018"
# file = 'raw_extract.xlsx'
# sheet1='01.raw_extract-tokee'
# df1=import_file1(directory,file,sheet1)
# 
# os.chdir('/home/ahmed/lssd_home/Abdullah/antibiotic data/antibiotic september 2018/July_2019')
# antibiotic_names=list(df1)[11:]
# start_year=2005
# end_year=2018
# org_list=['Escherichia coli','Salmonella group D']
# 
# all_dates=df1['Date']
# modified_all_dates=date_to_number(all_dates,start_year)
# df1['Date']=modified_all_dates
# 
# #S1,R1,_=AMR_Trend(df1,['003Chloramphenicol'],start_year=2005, end_year=2018, interval=30.42) 
# 
# plot_AMR(df1,antibiotic_names,start_year,end_year)
# 
# =============================================================================

#%%
# =============================================================================
# Vibrio_list=[ 'Vibrio cholerae O1 El Tor Inaba', 'Vibrio cholerae O1 El Tor Ogawa']
# df4_0=select_organism(df3,[Vibrio_list[0]])
# df4_1=select_organism(df3,[Vibrio_list[1]])
# 
# S1_0,R1_0,_=AMR_Trend(df4_0,['001Tetracycline'],start_year=2005, end_year=2019, interval=30.42) 
# S1_1,R1_1,_=AMR_Trend(df4_1,['001Tetracycline'],start_year=2005, end_year=2019, interval=30.42) 
# 
# R=pd.DataFrame()
# R[Vibrio_list[0]]=list(100*R1_0['001Tetracycline'])
# R[Vibrio_list[1]]=list(100*R1_1['001Tetracycline'])
# start=2005
# end=2019
# #d=dict(zip(list(range(end-start)),list(range(start,end))))
# #A=A.rename(index=d)
# #%%
# fig,ax=plt.subplots(nrows=1,ncols=1)
# x = np.arange(10)
# r=[1,0,0,1]
# b=[0,0,1,1]
# g=[0,1,0,1]
# colors=np.array([r,b,g])
# 
# plt.gca().set_prop_cycle(plt.cycler('color', colors))
# ax.plot(R,'-',linewidth=2)
# 
# ax.set_xlabel('Year')
# ax.set_ylabel('Percent resistance')
# ax.set_xticks(np.array(np.arange(min(A.index), max(A.index)+1, 12.0)))
# #ax.xaxis.set_ticks_position(np.arange(min(A.index), max(A.index)+1, 12.0))
# ax.xaxis.set_ticklabels(list(range(start,end)))
# fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
# yticks = mtick.FormatStrFormatter(fmt)
# ax.yaxis.set_major_formatter(yticks)
# fig.set_size_inches(30, 10)
# # Shrink current axis by 20%
# #ax = plt.subplot(111)
# box = ax.get_position(0)
# ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
# # Put a legend to the right of the current axis
# ax.legend(labels=list(R),loc='center left', bbox_to_anchor=(1, .5))
# plt.title('Vibrio Cholerae O1 Tetracycline')
# #plt.show()
# plt.savefig('/home/ahmed/vibrio_manuscript/Tet_resistance.eps',format='eps', dpi=1000)
# =============================================================================
# =============================================================================

# 
# =============================================================================

#%%


# =============================================================================
# 
#     timestamp = datetime.datetime.fromtimestamp(N)
#     return timestamp.strftime('%d-%m-%Y')
# df1=import_file1(directory,file,sheet1)
# 
# file = 'Resistant_14.xlsx'
# sheet1='Sheet1'
# Resistant_df1=import_file1(directory,file,sheet1)
# 
# #Change Date format (to number)
# 
# 
# #import excel file2 
# directory="/home/lssd/Abdullah/antibiotic data/antibiotic september 2018"
# file = 'Microbiology_Data_2018.xlsx'
# sheet1='Sheet1'
# df2=import_file1(directory,file,sheet1)
# df2['Date']=df2['Date']+4748
# df3=pd.concat([df1,df2],axis=0,sort=False,ignore_index=True)
# 
# 
# 
# 
# df4=select_organism(df3,['Salmonella Typhi'])
# 
# def day_year(N,start_year):
#     a=str(int(((N%365.25)%30.42)+1))+'/'+str(int(((N%365.25)//30.42)+1))+'/'+ str(start_year+int(N//365.25))
#     return a
# 
# new_date=[]
# for i in df4['Date']:
#     new_date.append(day_year(i,2005))
# 
# df4['Date']=new_date
# import os
# os.chdir('..')
# os.getcwd()
# os.chdir('..')
# os.getcwd()
# df4.to_excel('Salmonella Typhi 2005-2019.xlsx')
# 
# 
# =============================================================================
