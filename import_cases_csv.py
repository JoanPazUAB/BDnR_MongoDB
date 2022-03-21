# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 12:39:52 2022

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
        
        for i,el in enumerate(line):
            if i == 0 and el in list(dic.values()):
                for i in range(1,len(line)):
                    if 
            
            else: 
                dic[linia1[i]] = el
                llista_json.append(dic)
        
        

print(llista_json)       










