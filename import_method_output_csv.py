

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

    {'Method_ID: metode1'
    FeatDescriptor': 'PyRadiomics', 
    'FeatSelection': 'PCA', 
    'Classifier': 'NN', 
    'Train': 80
    'Repetitions': [
       { Repetition: 1,
        'BenignPrec': 41.18, 
        'BenignRec': 17.07, 
        'MalignPrec': 66.0, 
        'MalignRec': 86.84},
       {Repetition: 2,
        'BenignPrec': 41.18, 
        'BenignRec': 17.07, 
        'MalignPrec': 66.0, 
        'MalignRec': 86.84
        }
       ]}
mètode2:{
    ...
    }
    
'''
if args.fileName is not None:
    with open(args.fileName) as fitxer:
        llista_json = []
        dic = {}
        ll_rep = []
        dic_rep = {}
        linia1 = fitxer.readline()[3:-1].split(';')

        #print(linia1)
        for line in fitxer:
            line = line[:-1].split(';')
            #print(line)
            for i,el in enumerate(line):
                
                if linia1[i] == 'MethodID' and el in list(dic.values()):
                    metode_trobat = True
                    
                
                elif linia1[i] == 'MethodID' and el not in list(dic.values()):
                    dic = {}
                    dic['_id'] = el
                    metode_trobat = False

                    
                if linia1[i] == 'BenignPrec' or linia1[i] == 'BenignRec' or linia1[i] == 'MalignPrec' or linia1[i] == 'MalignRec':
                    el = float(el.replace(",","."))
                    dic_rep[linia1[i]] = el
                    
                elif linia1[i] == 'Repetition':
                    el = int(el) 
                    dic_rep[linia1[i]] = el
                    
                elif linia1[i] == 'Train':
                    el = int(el) 
                    dic[linia1[i]] = el
                
                elif i!=0:
                    dic[linia1[i]] = el
            
                
            
            if metode_trobat == False:
                 dic['Repeticions'] = [dic_rep]
                 llista_json.append(dic)
                 
                
            else: 
                llista_json[-1]['Repeticions'].append(dic_rep) 
            
            dic_rep = {}               
                
        print(llista_json)
        
        
        #llista_json.reverse()# perquè en el mongoDB surtin els mètodes en ordre 
for x in llista_json:
    c.insert_one(x)
# Tanquem les connexions i el tunel
conn.close()



'''
if args.fileName is not None:
    with open(args.fileName) as fitxer:
        llista_json = []
        dic = {}
        linia1 = fitxer.readline()[3:-1].split(';')
        #print(linia1)
        for line in fitxer:
            line = line[:-1].split(';')
            trobat = False
            #print(line)
            for i,el in enumerate(line):
                if i == 0 and el not in list(dic.values()):
                    dic = {}
                    dic['_id'] = el
                    trobat = True
                
                if trobat == True and i!= 0:
                    if linia1[i] == 'BenignPrec' or linia1[i] == 'BenignRec' or linia1[i] == 'MalignPrec' or linia1[i] == 'MalignRec':
                        el = float(el.replace(",","."))
                    elif linia1[i] == 'Repetition' or linia1[i] == 'Train':
                        el = int(el)
                    
                    dic[linia1[i]] = el
                  
                
                elif linia1[i] == 'Repetition':
                    llista_json[-1][linia1[i]] = int(llista_json[-1][linia1[i]]) 
                    llista_json[-1][linia1[i]] += 1
                    
                    
                elif linia1[i] == 'BenignPrec' or linia1[i] == 'BenignRec' or linia1[i] == 'MalignPrec' or linia1[i] == 'MalignRec':
                    el = el.replace(",",".")
                    if type(llista_json[-1][linia1[i]]) != type(list()):
                        llista_json[-1][linia1[i]] = [llista_json[-1][linia1[i]]]
                    llista_json[-1][linia1[i]].append(float(el))        
            if trobat == True:
                llista_json.append(dic)
        
        print(llista_json)
        
        
        #llista_json.reverse()# perquè en el mongoDB surtin els mètodes en ordre 
        for x in llista_json:
            c.insert_one(x)
# Tanquem les connexions i el tunel
conn.close()
'''