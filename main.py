
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

############################# TRANSFERÈNCIA DE DADES AMB MONGO ##############################

#Selecciona la base de dades a utilitzar
bd = conn['projecte_BDnR']

#Eliminem la base de dades si ja està creada
bd.drop_collection('Training')

# creem la colecció Training
col_training = bd.create_collection('Training')

"""
Carregar les dades des d'unfitxer CSV
"""
#Obrir Fitxer CSV

# Parse options
opts = Options()
args = opts.parse()

archivo = "training.csv"

#if args.fileName is not None:
training_dict = {}
with open(archivo,"r") as fitxer:
    cabecera = fitxer.readline()[:-1].split(",")
    for line in fitxer:
            line = line[:-1].split(",")
            if line[0] not in training_dict:
                training_dict[line[0]] = { line[1] : { line[2] : { "Rep" + line[3] : { cabecera[4] : line[4], cabecera[5] : line[5] } } } }    
            
            else:
                if line[1] in training_dict[line[0]]:#si está el tumor
                    if line[2] in training_dict[line[0]][line[1]]: #si está el método
                        #añadimos la nueva repetición sin comprovar ya que no se repiten las repeticiones por metodo.
                        training_dict[line[0]][line[1]][line[2]]["Rep" + line[3]] = { cabecera[4] : line[4], cabecera[5] : line[5] } 

                    else:#está el tumor pero no el método
                        training_dict[line[0]][line[1]][line[2]] = { "Rep" + line[3] : { cabecera[4] : line[4], cabecera[5] : line[5] } }
                
                else: # no está el tumor
                    training_dict[line[0]][line[1]] = { line[2] : { "Rep" + line[3] : { cabecera[4] : line[4], cabecera[5] : line[5] } } }

for x in training_dict:    
    training_dict[x].update({cabecera[0]:x})
    col_training.insert_one(training_dict[x])
# Tanquem les connexions i el tunel
conn.close()