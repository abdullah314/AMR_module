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
#%%
#AMR.AMR_Trend_month(df2,antibiotic_names, start_year=2017, end_year=2018, freq=True)


df4=AMR.remove_Hosp_Id(df3,col='Hosp_Id')    

antibiotic_names=list(df4)[11:]
antibiotic_names.remove('Patid')
antibiotic_names.remove('Patname')
#%%
genus_list=['Salmonella','Shigella', 'Vibrio', 'Escherichia', 'Aeromonas', 'Acinetobacter']
genus_plot1(df4, genus_list,  '/home/ahmed/new_plot/Enteric2')    
genus_plot2(df4, genus_list, 400,  '/home/ahmed/new_plot/Enteric2')     
genus_plot2(df4,genus_list, 1000,  '/home/ahmed/new_plot/Enteric2')
genus_plot2(df4, genus_list,10000,  '/home/ahmed/new_plot/Enteric2') 


genus_plot1(df3, ['Helicobacter pylori'],  '/home/ahmed/Helicobacter pylori') 
