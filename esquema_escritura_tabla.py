import requests
import pandas as pd
from IPython.core.display import HTML
import os
# 
# written by Guillermo Matas (TFG)
# oedb
oep_url= 'https://openenergy-platform.org/'

# token
your_token = '0171836f1d4a687084e1703c9ad9641ecff34b09'


def tableCreate(datos_geonica):
# create table
    schema = 'model_draft'
    data = { "query": 
                { "columns": [{ "name":"id", "data_type": "bigserial", "is_nullable": "NO" },
                              { "name":"yyyy_mm_dd", "data_type": "varchar", "character_maximum_length": "20" },
                              { "name":"hh_mm", "data_type": "varchar", "character_maximum_length": "10" },
                              { "name":"V_Viento", "data_type": "decimal" },
                              { "name":"D_Viento", "data_type": "decimal" },
                              { "name":"Temp_Air", "data_type": "decimal" },
                              { "name":"Rad_Dir", "data_type": "decimal" },
                              { "name":"Ele_Sol", "data_type": "varchar", "character_maximum_length": "20"  },
                              { "name":"Ori_Sol", "data_type": "decimal" },
                              { "name":"Top", "data_type": "decimal" },
                              { "name":"Mid", "data_type": "decimal" },
                              { "name":"Bot", "data_type": "decimal" },
                              { "name":"Cal_Top", "data_type": "decimal" },
                              { "name":"Cal_Mid", "data_type": "decimal" },
                              { "name":"Cal_Bot", "data_type": "decimal" },
                              { "name":"Pres_Aire", "data_type": "decimal" }],
                 "constraints": [ { "constraint_type": "PRIMARY KEY", "constraint_parameter": "id" } ] 
                } }
        
    for i in range(len(datos_geonica)):
        table = datos_geonica[i][0][0].strip('.txt')
        print(requests.put(oep_url+'/api/v0/schema/'+schema+'/tables/'+table+'/',
             json=data, headers={'Authorization': 'Token %s'%your_token} ))

def deleteTable(datos_geonica):
    schema = 'model_draft'
    for i in range(len(datos_geonica)):
        table = datos_geonica[i][0][0].strip('.txt')
        print(requests.delete(oep_url+'/api/v0/schema/'+schema+'/tables/'+table+'/'
                              , headers={'Authorization': 'Token %s'%your_token} ))

def addData(datos_geonica):
     schema = 'model_draft'
     for i in range(len(datos_geonica)):
         table = datos_geonica[i][0][0].strip('.txt')
         for j in range(1, len(datos_geonica[i][0])):
             data = {"query": 
                     {
                      "yyyy_mm_dd": datos_geonica[i][0][j][0], 
                      "hh_mm": datos_geonica[i][0][j][1],
                      "V_Viento":   datos_geonica[i][0][j][2],
                      "D_Viento":   datos_geonica[i][0][j][3],
                      "Temp_Air":   datos_geonica[i][0][j][4],
                      "Rad_Dir":    datos_geonica[i][0][j][5], 
                      "Ele_Sol":    datos_geonica[i][0][j][6],
                      "Ori_Sol":    datos_geonica[i][0][j][7],
                      "Top":        datos_geonica[i][0][j][8],
                      "Mid":        datos_geonica[i][0][j][9],
                      "Bot":        datos_geonica[i][0][j][10], 
                      "Cal_Top":    datos_geonica[i][0][j][11],
                      "Cal_Mid":    datos_geonica[i][0][j][12],
                      "Cal_Bot":    datos_geonica[i][0][j][13],
                      "Pres_Aire":  datos_geonica[i][0][j][14]
                     }}
             print(requests.post(oep_url+'/api/v0/schema/'+schema+'/tables/'+table+'/rows/new', 
                                json=data, headers={'Authorization': 'Token %s'%your_token} ))
             


def leerArchivotxt(ruta_fichero):
    data=[]
    fichero_geonica=open(ruta_fichero)
    
    for line in fichero_geonica.readlines(): 
        if (line.startswith('yy')):
            continue
        
        line=line.strip('\n')
        data.append(line.split('\t'))
        
    fichero_geonica.close()
    return data


def bucleGeonica(directorio_ficheros_geonica):
    datos_ficheros=[]
    i=0
    
    for fichero in os.listdir(directorio_ficheros_geonica):
        if (fichero.startswith('geonica')):
                datos_ficheros.append([])
                datos_ficheros[i].append([fichero]+leerArchivotxt(os.path.join(directorio_ficheros_geonica,fichero)))
                i+=1
     
    return datos_ficheros


datos_geonica=bucleGeonica(os.getcwd())
#deleteTable(datos_geonica)
tableCreate(datos_geonica)

addData(datos_geonica)
            
            

 
