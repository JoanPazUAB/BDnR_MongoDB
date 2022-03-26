# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 01:16:31 2022

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


if args.fileName is not None:
    with open(args.fileName) as fitxer:
        ll_metodes_json = []
        methods_visitats = []
        linia1 = fitxer.readline()[3:-1].split(';')

        #print(linia1)
        for line in fitxer:
            line = line[:-1].split(';')

            
            
            if line[0] not in methods_visitats:
                    dic_methods = {}
                    line[6] = float(line[6].replace(",","."))
                    line[7] = float(line[7].replace(",","."))
                    line[8] = float(line[8].replace(",","."))
                    line[9] = float(line[9].replace(",","."))
                    line[5] = int(line[5])
                    
                    dic_methods = {'_id': line[0], linia1[1]: line[1], linia1[2]: line[2], linia1[3]: line[3],
                                'Experiments': [line[4]]}

                    methods_visitats.append(line[0])
                    ll_metodes_json.append(dic_methods)
            
            else: 
                ll_metodes_json[-1]['Experiments'].append(line[4])
                
        print(ll_metodes_json)
        

for x in ll_metodes_json:
    c.insert_one(x)
# Tanquem les connexions i el tunel
conn.close()