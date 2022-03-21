# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 12:40:34 2022

@author: joanp
"""


with open("methodOutPut.csv", "r") as fitxer:
    llista_json = []
    dic = {}
    linia1 = fitxer.readline()[3:-1].split(';')
    print(linia1)
    for line in fitxer:
        line = line[:-1].split(';')
        print(line)
        
        for i,el in enumerate(line):
            dic[linia1[i]] = el
        llista_json.append(dic)

print(llista_json) 