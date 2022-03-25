from pymongo import MongoClient
import json
from options import Options
import openpyxl

################################## PARAMETRES DE CONNEXIÓ ###################################
mongoUser = ''
mongoPassword = ''
mongoDB = ''


Host = 'localhost' 
Port = 27017

DSN = "mongodb://{}:{}".format(Host,Port)

conn = MongoClient(DSN)
archivo = "cases.csv"
bd = conn['proyectoBD']
bd.drop_collection('Casos')

"""
csvs = openpyxl.load_workbook(archivo)
sheets = csvs.get_sheet_names() 
cases = csvs.get_sheet_by_name(sheets[0])
training = csvs.get_sheet_by_name(sheets[1])
methodoutput = csvs.get_sheet_by_name(sheets[2])
for row in cases.rows:
    for cell in row:
        print(cell.value,end=" ")
    print("\n")
    """
casos_dict = {}
col_cases = bd.create_collection("Casos")
with open(archivo,"r") as dades:
    cabecera = dades.readline()[:-1].split(";") 
    for line in dades: 
        line = line.replace(",",";")
        print(line)
        line = line[:-1].split(';')
        print(line,len(line))

        if line[0] not in casos_dict:
            casos_dict[line[0]] = {
                cabecera[1]:line[1],
                cabecera[2]:line[2],
                cabecera[3]:int(line[3]),
                cabecera[4]:line[4],
                cabecera[5]:line[5],
                cabecera[6]:line[6],
                cabecera[7]:line[7],
                cabecera[8]:line[8],
                cabecera[9]:line[9],
                cabecera[10]:line[10],
                cabecera[11]:line[11],
                cabecera[12]:line[12],
                cabecera[13]:line[13],
                cabecera[14]:line[14],
                }
            try:
                casos_dict[line[0]][cabecera[15]] = [line[15],line[16],line[17]]
            except IndexError: 
                casos_dict[line[0]][cabecera[15]] = [line[15],line[16]]

        else: 
            if casos_dict[line[0]][cabecera[3]] == 1: 
                for i in range(5,11):
                    casos_dict[line[0]][cabecera[i]] = [casos_dict[line[0]][cabecera[i]], line[i]]

            elif casos_dict[line[0]][cabecera[3]] >= 2:
                for i in range(5,11):
                    casos_dict[line[0]][cabecera[i]].append(line[i]) 

            casos_dict[line[0]][cabecera[3]] = int(line[3])

for caso in casos_dict: 
    casos_dict[caso].update({cabecera[0]:caso})
    col_cases.insert_one(casos_dict[caso])

