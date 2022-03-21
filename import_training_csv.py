# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 12:40:08 2022

@author: joanp
"""

with open("cases.csv", "r") as fitxer:
    llista_json = []
    dic = {}
    linia1 = fitxer.readline()[3:-1].split(';')
    print(linia1)
    for line in fitxer:
        line = line[:-1].split(';')
        print(line)
        trobat = False
        for i,el in enumerate(line):
            if i == 0 and el not in list(dic.values()):
                dic = {}
                dic[linia1[i]] = el
                trobat = True
            
            if trobat == True:
                dic[linia1[i]] = el
            
            elif list(llista_json[-1].values())[i] != el:
                
                
            
                
            
            #if trobat == True
            
            
            
        llista_json.append(dic)

print(llista_json) 
