

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 12:40:34 2022

@author: joanp
"""

from pymongo import MongoClient
import json
from options import Options

################################## PARAMETRES DE CONNEXIÓ ###################################
mongoUser = ''
mongoPassword = ''
mongoDB = ''

"""
1.  Actualitzeu els paràmetres del script NoSQLfromPython.py per poder establir la connexió amb el MongoDB del vostre PC.
"""
# En execució remota
Host = 'localhost' 
Port = 27017


###################################### CONNEXIÓ ##############################################

DSN = "mongodb://{}:{}".format(Host,Port)
conn = MongoClient(DSN)

#Eliminem la base de dades si ja està creada


############################# TRANSFERÈNCIA DE DADES AMB MONGO ##############################

#Selecciona la base de dades a utilitzar
bd = conn['projecte_BDnR']
bd.drop_collection('method_OutPut')

"""
2.	Creeu una col·lecció Prova dins la base de dades test e inseriu 100 documents amb un camp a (a=1 ... a=100).
"""
# Creació d'una col·lecció
c = bd.create_collection('method_OutPut')

"""
Carregar les dades des d'unfitxer CSV
"""
#Obrir Fitxer CSV

# Parse options
opts = Options()
args = opts.parse()

'''
FORMAT 

    {'_id': 'Method20', 
    'FeatDescriptor': 'CNN', 
    'FeatSelection': 'PCA', 
    'Classifier': 'SVM', 
    'Experiments': [
    {'Repetition': 1, 'Train': 60, 'BenignPrec': 34.48, 'BenignRec': 97.56, 'MalignPrec': 0.0, 'MalignRec': 0.0}, 
    {'Repetition': 2, 'Train': 60, 'BenignPrec': 38.64, 'BenignRec': 82.93, 'MalignPrec': 75.86, 'MalignRec': 28.95}, 
    {'Repetition': 3, 'Train': 60, 'BenignPrec': 27.5, 'BenignRec': 26.83, 'MalignPrec': 61.04, 'MalignRec': 61.84}, 
    {'Repetition': 4, 'Train': 60, 'BenignPrec': 34.15, 'BenignRec': 34.15, 'MalignPrec': 64.47, 'MalignRec': 64.47}]}
    
'''
if args.fileName is not None:
    with open(args.fileName) as fitxer:
        ll_metodes_json = []
        methods_visitats = []
        linia1 = fitxer.readline()[3:-1].split(';')

        #print(linia1)
        for line in fitxer:
            line = line[:-1].split(';')

            line[6] = float(line[6].replace(",","."))
            line[7] = float(line[7].replace(",","."))
            line[8] = float(line[8].replace(",","."))
            line[9] = float(line[9].replace(",","."))
            line[5] = int(line[5])
            line[4] = int(line[4])
                    
            if line[0] not in methods_visitats:
                    dic_methods = {}
                    
                    
                    dic_methods = {'_id': line[0], linia1[1]: line[1], linia1[2]: line[2], linia1[3]: line[3],
                                'Experiments': [{linia1[4]:line[4], linia1[5]:line[5], linia1[6]:line[6], linia1[7]:line[7], 
                                                 linia1[8]:line[8], linia1[9]:line[9]}]}

                    methods_visitats.append(line[0])
                    ll_metodes_json.append(dic_methods)
            
            else: 
                ll_metodes_json[-1]['Experiments'].append({linia1[4]:line[4], linia1[5]:line[5], linia1[6]:line[6], linia1[7]:line[7], 
                                                 linia1[8]:line[8], linia1[9]:line[9]})
                
        

for x in ll_metodes_json:
    c.insert_one(x)
# Tanquem les connexions i el tunel
conn.close()



