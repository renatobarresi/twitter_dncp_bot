"""
    Este proceso es utilizado para detectar los cambios en el CSV de la DNCP, y cargar la base de datos con la informacion
    de las licitaciones que cambiaron de estado al estado determinado por el usuario
"""

from modules.dncp_api import download_csv_dncp, licitaciones, obtain_request_token, obtain_access_token_dncp_V2, obtain_access_token_dncp_V3
from modules.sqlite_api import licitacionDataBase

dataBaseName = "basicDB.db"
basicTable = "tablaBasica"
keyValuesColumns_V_1 = "ID TEXT, Titulo TEXT, Costo INTEGER, Institucion TEXT, Adjudicados TEXT, Denuncias INTEGER, Link TEXT"
keyValues_V_1 = "ID, Titulo, Costo, Institucion, Adjudicados, Denuncias, Link"
credentialsPath = "../credentials/dncp.json"
accessTokenURL = "https://contrataciones.gov.py/datos/api/oauth/token"
CSVLink = "https://contrataciones.gov.py/buscador/licitaciones.html?nro_nombre_licitacion=&categorias%5B%5D=17&categorias%5B%5D=18&categorias%5B%5D=19&categorias%5B%5D=20&categorias%5B%5D=21&categorias%5B%5D=22&categorias%5B%5D=23&categorias%5B%5D=24&categorias%5B%5D=25&categorias%5B%5D=26&categorias%5B%5D=27&categorias%5B%5D=28&categorias%5B%5D=29&categorias%5B%5D=30&categorias%5B%5D=31&categorias%5B%5D=32&categorias%5B%5D=33&categorias%5B%5D=34&categorias%5B%5D=35&categorias%5B%5D=36&categorias%5B%5D=37&categorias%5B%5D=38&categorias%5B%5D=39&categorias%5B%5D=40&categorias%5B%5D=41&tipos_procedimiento%5B%5D=CD&tipos_procedimiento%5B%5D=CO&tipos_procedimiento%5B%5D=LPI&tipos_procedimiento%5B%5D=LPN&fecha_desde=01-12-2022&fecha_hasta=&tipo_fecha=EST&convocante_tipo=&convocante_nombre_codigo=&codigo_contratacion=&catalogo%5Bcodigos_catalogo_n4%5D=&page=1&order=&convocante_codigos=&convocante_tipo_codigo=&unidad_contratacion_codigo=&catalogo%5Bcodigos_catalogo_n4_label%5D="

def main():

    #get DNCP's API request token and access token
    requestToken = obtain_request_token(credentialsPath)
    accessToken_V3 = obtain_access_token_dncp_V3(requestToken)
    accessToken_V2 = obtain_access_token_dncp_V2(requestToken)

    if accessToken_V2 == False or accessToken_V3 == False:
        print("ERROR: Unable to obtain access token.")
        print("V3: ", accessToken_V3)
        print("V2: ", accessToken_V2)
        exit(1)
    else:
        print("V3: ", accessToken_V3)
        print("V2: ", accessToken_V2)

    #Create licitaciones object and obtain the list of all tenders that changed status to 'ADJ'
    allTenders = licitaciones("ADJ", CSVLink, accessToken_V2, accessToken_V3)
    listAllTendersADJ = allTenders.obtain_tenders_list()
    print("Licitaciones ADJ:\r\n", listAllTendersADJ)

    #fill the data base
    if listAllTendersADJ != []:
        basicDBTenders = licitacionDataBase(dataBaseName, basicTable, keyValuesColumns_V_1)
        for ID in listAllTendersADJ:
            value = allTenders.obtain_values(ID)           
            ##testDB.insert_values("db2.db", "tabla1", "ID, Titulo, Estado, Costo, Institucion, Adjudicados, Denuncias, Link", (2, "titulo2", "estado3", 12314412, "conacyt", "datasystem", "no", "www.reddit.com"))
            #value = (value["ID"], "\"" + value["Titulo"] + "\"", value["Costo"],  "\"" + value["Convocante"] + "\"" , "\"" + value["Adjudicados"]  + "\"", value["Protestas"], "\"" +  value["Link"] + "\"" )
            value = (value["ID"], value["Titulo"], value["Costo"], value["Convocante"], value["Adjudicados"], value["Protestas"], value["Link"])
            print("Agregando a base de datos:\r\n", value)
            basicDBTenders.insert_values(dataBaseName, basicTable, keyValues_V_1, value)
        print("BASE DE DATOS\r\n\r\n", basicDBTenders.read_table(db_name=dataBaseName,table_name=basicTable))
    else:
        print("Nada para cargar en la base de datos")
    
if __name__ == "__main__":
    main()