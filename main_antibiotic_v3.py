#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 12:21:53 2018

@author: Ahmed Abdullah
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
directory="path/to/directory"
file = 'File1.xlsx'
sheet1='Sheet1'
df3=AMR.import_file1(directory,file,sheet1)

#%%
#AMR.AMR_Trend_month(df2,antibiotic_names, start_year=2017, end_year=2018, freq=True)


df4=AMR.remove_Hosp_Id(df3,col='Hosp_Id')    


#%% Plot percent resistance for some enteric bacteria
genus_list=['Salmonella','Shigella', 'Vibrio', 'Escherichia', 'Aeromonas', 'Acinetobacter']
genus_plot1(df4, genus_list,  '/path/to/output1')    
genus_plot2(df4, genus_list, 400,  '/path/to/output1')     
genus_plot2(df4,genus_list, 1000,  '/path/to/output1')
genus_plot2(df4, genus_list,10000,  '/path/to/output1') 

#%% 

