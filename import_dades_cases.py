# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 21:01:25 2022

@author: joanp
"""

from pymongo import MongoClient
import json
import pandas as pd
#from options import Options

################################## PARAMETRES DE CONNEXIÓ ###################################
# mongoUser = ''
# mongoPassword = ''
# mongoDB = ''

# """
# 1.  Actualitzeu els paràmetres del script NoSQLfromPython.py per poder establir la connexió amb el MongoDB del vostre PC.
# """
# # En execució remota
# Host = 'localhost' 
# Port = 27017

# ###################################### CONNEXIÓ ##############################################

# DSN = "mongodb://{}:{}".format(Host,Port)
# conn = MongoClient(DSN)

# ############################# TRANSFERÈNCIA DE DADES AMB MONGO ##############################
# #Selecciona la base de dades a utilitzar 
# bd = conn['s10']

# # Creació d'una col·lecció
# c = bd.create_collection('transactions')

# Inserció documents a una col·lecció


#-----------------llegida correcte 1--------------------------
from xlrd import open_workbook

wb = open_workbook('Dades.xlsx')
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)
dic_linies = {}
linia1 = []
ll_json = []

for i in range(1):
    for j in range(sheet.ncols):
        linia1.append(sheet.cell_value(i, j))
print(linia1)
        
for i in range(1,118):
    l_aux = []
    for j in range(sheet.ncols):
        l_aux.append(sheet.cell_value(i, j))
        
    for pos,el in enumerate(l_aux):
        dic_linies[linia1[pos]] = el
    ll_json.append(dic_linies)

           
# for x in llista_json:
#     c.insert_one(x)

# # Tanquem les connexions i el tunel
# conn.close()


#https://programmerclick.com/article/9740120496/