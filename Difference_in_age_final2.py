#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 12:21:53 2018

@author: lssd
"""
import AMR
import pandas as pd
import numpy as np
import os
def filter_antibiotic(df_enteric, antibiotic_names, occurence ): 
    ab_a=[]
    
    for antibiotics in antibiotic_names:
        temp=df_enteric[antibiotics].copy()
        temp=temp.dropna()
        if (temp.shape)[0]>occurence:
            ab_a.append(antibiotics)
    return ab_a

def genus_plot1(df4, species_list, Directory  ):
    species_name_list=AMR.search_organism(df4['Orgid'].unique(),species_list)
    df_species_name=AMR.select_organism(df4,species_name_list)
    os.chdir(Directory)
    os.mkdir('all')
    os.chdir('all')
    AMR.plot_AMR_year(df_species_name, antibiotic_names, 2005,2018, org_name='')
    

def genus_plot2(df4, species_list, occurence, Directory):
    species_name_list=AMR.search_organism(df4['Orgid'].unique(),species_list)
    df_species_name=AMR.select_organism(df4,species_name_list)
    os.chdir(Directory)
    os.mkdir('>'+str(occurence))
    os.chdir('>'+str(occurence))
    AMR.plot_AMR_year(df_species_name, filter_antibiotic(df_species_name, antibiotic_names, occurence ), 2005,2018, org_name='')
#specify to whether to sex are differentiated
sex_differ=0

#import excel file 
directory="/home/ahmed/lssd_home/Abdullah/antibiotic data/antibiotic september 2018"
file = 'raw_extract.xlsx'
sheet1='01.raw_extract-tokee'
df1=AMR.import_file1(directory,file,sheet1)
directory="/home/ahmed/lssd_home/Abdullah/antibiotic data/antibiotic september 2018"
file = 'Microbiology_Data_2018.xlsx'
sheet1='Sheet1'
df2=AMR.import_file1(directory,file,sheet1)

df2['Date']=AMR.ordinal_to_date_1(date_data=df2['Date'])
df3=pd.concat([df1,df2],axis=0,sort=False,ignore_index=True)

df4=AMR.remove_Hosp_Id(df3,col='Hosp_Id')    

antibiotic_names=list(df4)[11:]
antibiotic_names.remove('Patid')
antibiotic_names.remove('Patname')

x_age=[]
age=list(df4['Age'])
fake_guys=[]
for i in range(len(age)):
    if isinstance(age[i], str):
        age[i]=0
        fake_guys.append(i)


agem=list(df4['Agem']/12)
aged=list(df4['Aged']/365)
for index in range(len(age)):
    a=age[index]+agem[index]+aged[index]
    x_age.append(a)
    
df4['Age_md']=x_age


f=open('/home/ahmed/AMR_age_based_plot0/Folder_for_sabiha/my_ab.txt','r')
f_r=f.read()
f_l=f_r.split('\n')
f_l.remove('')

import re

ab_list=[]

for ab in f_l:
    for i in antibiotic_names:
        if re.match('.*'+ab,i):
            ab_list.append(i)
            

import matplotlib.ticker as mtick
import matplotlib as mpl
st=type('s')
ind=[]
for i in df4['Age'].index:
    if type(df4.loc[i,'Age'])==st:
        ind.append(i)
        
A0_15_df4=df4.loc[(df4['Age_md'] >=0) & (df4['Age_md'] <15) ]
A15_25_df4=df4.loc[(df4['Age_md'] >=15) & (df4['Age_md'] <25)]
A25_45_df4=df4.loc[(df4['Age_md'] >=25) & (df4['Age_md'] <45)]
A45_65_df4=df4.loc[(df4['Age_md'] >=45) & (df4['Age_md'] <65)]
A65_plus_df4=df4.loc[(df4['Age_md'] >=65)]


A0_15_S,  A0_15_R, A0_15_I= AMR.AMR_Trend_year(A0_15_df4,antibiotic_names, start_year=2005, end_year=2019, freq=True) 
A15_25_S,  A15_25_R, A15_25_I= AMR.AMR_Trend_year(A15_25_df4,antibiotic_names,start_year=2005, end_year=2019, freq=True) 
A25_45_S,  A25_45_R, A25_45_I= AMR.AMR_Trend_year(A25_45_df4,antibiotic_names,start_year=2005, end_year=2019, freq=True) 
A45_65_S,  A45_65_R, A45_65_I= AMR.AMR_Trend_year(A45_65_df4,antibiotic_names,start_year=2005, end_year=2019, freq=True) 
A65_plus_S,  A65_plus_R, A65_plus_I= AMR.AMR_Trend_year(A65_plus_df4,antibiotic_names,start_year=2005, end_year=2019, freq=True)  
        
        

import re
import os
import string
import shutil
abcd=list(string.ascii_uppercase)

new_folder='/home/ahmed/AMR_age_based_plot3'

if os.path.exists(new_folder):
    pass
else:
    os.makedirs(new_folder)

os.chdir('/home/ahmed/AMR_age_based_plot3')
 
x=list(range(2005,2019))
import matplotlib.pyplot as plt
counter=0
for i in ab_list:
    fig,ax=plt.subplots(nrows=1,ncols=1)
 
    y=A0_15_R[i]*100
    
    A0_15_plot,=ax.plot(x,y, label = '0 -15 ')
      
    y=A15_25_R[i]*100
    A15_25_plot,= ax.plot(x,y, label = '15 -25')
    
   
    y=A25_45_R[i]*100
    A25_45_plot,= ax.plot(x,y, label = '25 -45')
    
    y=A45_65_R[i]*100
    A45_65_plot,= ax.plot(x,y, label = '45 -65')
    
    y=A65_plus_R[i]*100
    A65_plus_plot,= ax.plot(x,y, label = '65 plus')

    #fig.set_size_inches(20, 10)
    # Shrink current axis by 20%
    #ax = plt.subplot(111)
 
    fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
    yticks = mtick.FormatStrFormatter(fmt)
    ax.yaxis.set_major_formatter(yticks)
    regex=re.compile('.*/')
    
    if re.match(regex,i):
        aa=i.split('/')
        i=' or '.join(aa)   
        
    
    name=i[3:]
    plt.title(name)
  
    all_handles=[A0_15_plot, A15_25_plot, A25_45_plot, A45_65_plot,  A65_plus_plot ];
    
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])    
    ax.legend(handles=all_handles,loc='center left', bbox_to_anchor=(1, .5))
    ax.set_xlabel('Year')
    ax.set_ylabel('Percentage of Resistance calculated')
    fig.text(0.05,0.95, abcd[counter],  fontsize=20)
    plt.savefig(name+'.png',dpi=300)
    plt.clf()
    counter=counter+1
    
   


A0_15_R.index=list(range(2005,2019))
A15_25_R.index=list(range(2005,2019))
A25_45_R.index=list(range(2005,2019))
A45_65_R.index=list(range(2005,2019))
A65_plus_R.index=list(range(2005,2019))

writer=pd.ExcelWriter('/home/ahmed/AMR_age_based_plot3/AMR_Age.xlsx', engine='xlsxwriter')
A0_15_R.to_excel(writer,'0-15')
A15_25_R.to_excel(writer,'15-25')
A25_45_R.to_excel(writer,'25-45')
A45_65_R.to_excel(writer,'45-65')
A65_plus_R.to_excel(writer,'65+')
writer.save()