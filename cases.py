

from pydoc import doc
from pymongo import MongoClient
import json

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

############################# TRANSFERÈNCIA DE DADES AMB MONGO ##############################

#Selecciona la base de dades a utilitzar
bd = conn['projecte_BDnR']

#Eliminem la base de dades si ja està creada
bd.drop_collection('Patient')

# creem la colecció Training
col_patient = bd.create_collection('Patient')

"""
Carregar les dades des d'unfitxer CSV
"""
#Obrir Fitxer CSV

'''
{PatiendID: ...,
 Age: ...,
Gender: ...,
DiagnosisPatient: ...,
Nodules: [
    {
NoduleID: 1,
    DiagnosisNodule: ...,
PositionX: ...,
PositionY: ...,
PositionZ: ...,
Diameter: ...
CTID: 1
},
{
NoduleID: 2,
    DiagnosisNodule: ...,
PositionX: ...,
PositionY: ...,
PositionZ: ...,
Diameter: ...
CTID: 1
}
]
}
'''

# Parse options


archivo = "cases.csv"

#if args.fileName is not None:
documents_patient = {}
with open(archivo,"r") as fitxer:
    fitxer.readline()
    for line in fitxer:
        line = line[:-1].split(';')
        if line[0] not in documents_patient:
            documents_patient[line[0]] = [{'PatientID': line[0],'Age':line[1], 'Gender': line[2], 'Diagnosis_Patient': line[4],
                                          'Nodules': [{
                                              'NoduleID': line[3], 
                                              'Diagnosis_nodul': line[5], 
                                              'Position':{'x':line[6], 'y': line[7], 'z':line[8]},
                                              'Diameter': line[9],
                                              'CTID': line[10]}] }, [line[3]]]
        else:
            if line[3] not in documents_patient[line[0]][1]:
                nodule = {
                    'NoduleID': line[3], 
                    'Diagnosis_nodul': line[5], 
                    'Position':{'x':line[6], 'y': line[7], 'z':line[8]},
                    'Diameter': line[9],
                    'CTID': line[10]}
                documents_patient[line[0]][0]['Nodules'].append(nodule)
                documents_patient[line[0]][1].append(line[3])
                
                                                      
for x in documents_patient.values():    
    col_patient.insert_one(x[0])
# Tanquem les connexions i el tunel
conn.close()

