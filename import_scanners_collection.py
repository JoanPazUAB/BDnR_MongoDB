# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 16:48:58 2022

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
bd.drop_collection('scanners')

"""
2.	Creeu una col·lecció Prova dins la base de dades test e inseriu 100 documents amb un camp a (a=1 ... a=100).
"""
# Creació d'una col·lecció
c = bd.create_collection('scanners')

"""
Carregar les dades des d'unfitxer CSV
"""
#Obrir Fitxer CSV

# Parse options
opts = Options()
args = opts.parse()

if args.fileName is not None:
    with open(args.fileName) as fitxer:
        scanners = []

        linia1 = fitxer.readline()[3:-1].split(';')[-6:]
        
        for line in fitxer:
            dic_scan = {}
            line = line[:-1].split(';')[-6:]
            if line[0] not in scanners:
                    line[3] = float(line[3].replace(",","."))
                    line[4] = int(line[4])
                    line[5] = int(line[5])
                    
                    dic_scan = {'_id': line[0], linia1[1]: line[1], linia1[2]: line[2], 
                                'Resolution': [{linia1[3][-1]: line[3]}, {linia1[4][-2:]: line[4]}, {linia1[5][-2:]: line[5]}]}
                    
                    c.insert_one(dic_scan) 
                    scanners.append(line[0])
                

            
            


    
