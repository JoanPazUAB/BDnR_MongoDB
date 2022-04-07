

from pydoc import doc
from pymongo import MongoClient
import json
import options

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
bd.drop_collection('cases')

# creem la colecció Training
c = bd.create_collection('cases')

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

opts = Options()
args = opts.parse()

if args.fileName is not None:
     documents_patient = {}
     
     with open(args.fileName) as fitxer:
         fitxer.readline()
         for line in fitxer:
             line = line[:-1].split(';')
             line[1] = int(line[1])
             line[3] = int(line[3])
             line[6] = int(line[6])
             line[7] = int(line[7])
             line[8] = int(line[8])
             line[9] = float(line[9].replace(",","."))
             line[10] = int(line[10])
             if line[0] not in documents_patient:
                 documents_patient[line[0]] = [{'_id': line[0],'Age':line[1], 'Gender': line[2], 'Diagnosis_Patient': line[4], 'CTID': line[10]},
                                               'Nodules': [{
                                                   'NoduleID': line[3], 
                                                   'Diagnosis_nodul': line[5], 
                                                   'Position':{'x':line[6], 'y': line[7], 'z':line[8]},
                                                   'Diameter': line[9]
                                                   ] }, [line[3]]]
             else:
                 if line[3] not in documents_patient[line[0]][1]:
                     nodule = {
                         'NoduleID': line[3], 
                         'Diagnosis_nodul': line[5], 
                         'Position':{'x':line[6], 'y': line[7], 'z':line[8]},
                         'Diameter': line[9]
                         }
                     documents_patient[line[0]][0]['Nodules'].append(nodule)
                     documents_patient[line[0]][1].append(line[3])
                
print(documents_patient.values())                                                      
for x in documents_patient.values():    
    c.insert_one(x[0])
# Tanquem les connexions i el tunel
conn.close()

