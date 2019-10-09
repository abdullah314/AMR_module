#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 14:40:49 2019

@author: ahmed
"""
#run fix_age.py
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

new_folder='/home/ahmed/AMR_age_based_plot3

if os.path.exists(new_folder):
    pass
else:
    os.makedirs(new_folder)

os.chdir('/home/ahmed/AMR_age_based_plot3')
 
x=list(range(2005,2019))
import matplotlib.pyplot as plt
counter=0
for i in antibiotic_names:
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
    plt.savefig(name+'.png')


    
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
    
   

