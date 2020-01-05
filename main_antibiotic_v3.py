#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 12:21:53 2018

@author: Ahmed Abdullah

It uses AMR module (AMR.py) and make plots

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

def genus_plot1(df, species_list, Directory  ):
    '''
    Provide dataframe containing antibiotic resistance data , list of species you are interested in and and an output
    directory to save the images
    arguments
    =========
    df: dataframe containing antibiotic resistance data
    species_list:  list of species
    Directory: provide string as directory name
    
    returns
    =======
    images in Directory folder
    
    '''
    species_name_list=AMR.search_organism(df['Orgid'].unique(),species_list)
    df_species_name=AMR.select_organism(df,species_name_list)
    os.chdir(Directory)
    os.mkdir('all')
    os.chdir('all')
    AMR.plot_AMR_year(df_species_name, antibiotic_names, 2005,2018, org_name='')
    

def genus_plot2(df4, species_list, occurence, Directory):
    '''
    same as function genus_plot1 but filters antibiotic based on occurence. If antibiotic occurs less frequently than the
    specified number than that antibiotic is ommitted. 
    
    Provide dataframe containing antibiotic resistance data , list of species you are interested in and and an output
    directory to save the images
    arguments
    =========
    df: dataframe containing antibiotic resistance data
    species_list:  list of species
    occurence: integer, minimum number of occurence of an antibiotic for inclusion 
    Directory: provide string as directory name
    
    returns
    =======
    images in Directory folder
    
    '''
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


#%% Plot percent resistance for some enteric bacteria
genus_list=['Salmonella','Shigella', 'Vibrio', 'Escherichia', 'Aeromonas', 'Acinetobacter']
genus_plot1(df4, genus_list,  '/path/to/output1')    
genus_plot2(df4, genus_list, 400,  '/path/to/output1')     
genus_plot2(df4,genus_list, 1000,  '/path/to/output1')
genus_plot2(df4, genus_list,10000,  '/path/to/output1') 

#%% 

