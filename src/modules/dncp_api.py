"""
    This module contains functions that interact with the API of the National Public Procurement System (DNCP) in Paraguay.
    The API allows users to obtain information about public tenders, including the list of tenders and details about each tender.
    The module provides functions to obtain request and access tokens from the API, and to download a CSV file with information about tenders and convert it into a Pandas dataframe.
    Additionally, the module contains a function to obtain a list of awarded suppliers for a given tender using the API V2 (which will be deprecated in June 2023).
"""
import json
import requests
import pandas
from bs4 import BeautifulSoup as bs

apiV3EndPoint = "https://www.contrataciones.gov.py/datos/api/v3/doc/"   #link de la api V3
apiV2EndPoint = "https://www.contrataciones.gov.py:443/datos/api/v2/"   #link de la api V2 (solo utilizado para obtner lista de proveedores adjudicados)
accessTokenURL_V3 = apiV3EndPoint + "oauth/token"   #endporint de la api v3 para obtener el access token
accessTokenURL_V2 = apiV2EndPoint + "oauth/token"   #endporint de la api v2 para obtener el access token
tenderInfoEndPoint_V3 = apiV3EndPoint + "tender/"   #endpoint de la api V3 para obtener la informacion de la licitacion
tenderAdjudicadosEndPint_V2 = apiV2EndPoint + "doc/adjudicaciones/" #endpoint de la api v2 para obtener lista de proveedores adjudicados
linkLicitacionGenerico = "https://www.contrataciones.gov.py/licitaciones/adjudicacion/" #link para generar el url de una licitacion
linkLicitacionCONV = "https://www.contrataciones.gov.py/licitaciones/convocatoria/"

tenderQuery = "?sections=title%2C%20value%2C%20procuringEntity" #query que se le pasa al endpoint de la api v3 "/tender"

def obtain_request_token(path):
    """
    Returns request token stored in json file at specified path.
    :param path: Path to the file that contains the request token.
    :return: Request token stored in the specified file.
    """

    f = open(path)
    data = json.load(f)
    f.close()
    return data["request-token"]
    
def obtain_access_token_dncp_V3(requestToken):
    """
    Returns access token if operation was successful, otherwise returns False.
    :param requestToken: Request token provided by DNCP.
    :return: Access token if successful, False otherwise.
    """

    head ={"accept":"application/json",
        "Content-Type":"application/json"
    }
    body = {
        "request_token":requestToken
    }
    response = requests.post(accessTokenURL_V3, data=json.dumps(body), headers = head)
    if response.status_code == 200:
        accessToken = response.json()["access_token"]
        return accessToken
    else:
        print(response.request.body)
        print(response.status_code) 
        return False

def obtain_access_token_dncp_V2(requestToken):
    """
    Returns access token if operation was successful, otherwise returns False.
    :param requestToken: Request token provided by DNCP.
    :return: Access token if successful, False otherwise.
    """
    
    headers ={"Authorization":"Basic " + requestToken}
    response = requests.post(accessTokenURL_V2, headers = headers)
    if response.status_code == 200:
        accessToken = response.json()["access_token"]
        return accessToken
    else:
        print(response.request.body)
        print(response.status_code) 
        return False

def download_csv_dncp(url):
    """
    Downloads a CSV file from the given URL (https://contrataciones.gov.py/buscador/licitaciones.html) and returns a Pandas dataframe of the CSV.

    Parameters:
    url (str): The URL of the CSV file to download.

    Returns:
    Pandas dataframe: A dataframe of the CSV file.
    """

    print("Descargando html...")

    page = requests.get(url)

    if page.status_code == 200:
        print("Descarga exitosa!")
    else:
        print("Error (?) al descargar html, status code: ", page.status_code)
    
    soup = bs(page.content, "html.parser")
    container = soup.find_all("div", {"class":"downloadTool"})
    link = "https://www.contrataciones.gov.py" + container[0].a['href']

    df = pandas.read_csv(link, on_bad_lines='skip', delimiter = ";")
    return df

class licitaciones:
    def __init__(self, estado, link, nombreCSV, accessToken_V2, accessToken_V3):
        """
        Initializes a licitaciones object with the given category, state, and link.

        Parameters:
        estado (str): The state of the tenders to detect e.g 'adjudicada', 'en convocatoria'.
        link (str): link to https://contrataciones.gov.py/buscador/licitaciones.html but with the added filters.
        accessToken_V2: access token de la api v2
        accessToken_V3: access token de la api v3
        """
        self.estado = estado
        self.link = link
        self.accessToken_V2 = accessToken_V2
        self.accessToken_V3 = accessToken_V3
        self.nombreCSV = nombreCSV

    def __str__(self):
        """
        Returns a string representation of the licitaciones object.
        """
        return f", Estado: {self.estado}, Link: {self.link}"

    def obtain_tenders_list(self):
        """
        Compares two CSVs and returns a list with the IDs of the tenders that changed in category.

        Returns:
        list: A list containing the IDs of the tenders from a particular category that changed in category.
        """
        listIDs = []    #esta es la lista que se retorna, y contiene los IDs que cambiaron de estado a el estado definido por state

        ''' read base CSV, download if it does not exist '''
        try:
            baseDF = pandas.read_csv(self.nombreCSV, on_bad_lines='skip', delimiter = ";")
        except FileNotFoundError:
            print("TENES QUE DESCARGAR PRIMERO EL CSV BASE")
            exit(1)

        ''' download updated DNCP CSV '''
        updatedDF = download_csv_dncp(self.link)

        ''' compare the two CSVs '''
        licitacionesNew = dict(zip(updatedDF.convocatoria_slug, updatedDF._etapa_licitacion)) #convierte dataFrame a diccionario
        licitacionesOld = dict(zip(baseDF.convocatoria_slug, baseDF._etapa_licitacion))

        for id in licitacionesNew:
            if (id in licitacionesOld) == True:   # si el key (ID de la licitacion) no existe en licitacionesOld quiere decir que se agrego la licitacion al csv
                if licitacionesNew[id] != licitacionesOld[id]:
                    if self.estado == licitacionesNew[id]:
                        listIDs.append(id)
                        #print(id, licitacionesNew[id])

        ''' convertir el updatedDF a reporte.csv '''
        updatedDF.to_csv(self.nombreCSV, sep = ";")

        return listIDs

    def obtain_values(self, ID, status):
        """
        returns a dictionary with the values corresponding to an individual ID, using the V2 API (Will be deprecated in July of 2023)
        ID: id de la licitacion
        """

        if status == "ADJ":
            urlLicitacion = linkLicitacionGenerico + ID + "/resumen-adjudicacion.html" #link para licitacion adjudicada
        elif status == "CONV":
            urlLicitacion = linkLicitacionCONV + ID + ".html"

        dicValues = {"ID":"", "Titulo":"", "Costo":0, "Convocante":"", "Adjudicados":[], "Protestas":0, "Link":urlLicitacion}

        #Use API V3 to obtain Titulo, Estado, Costo, Institucion
        urlAPI = tenderInfoEndPoint_V3 + ID + tenderQuery
        response = self.__obtain_api_v3_tender(urlAPI)
        
        if response != False:
            dicValues["Titulo"] = response["tender"]["title"]
            dicValues["Convocante"] = response["tender"]["procuringEntity"]["name"]
            dicValues["Costo"] = response["tender"]["value"]["amount"]
            
        dicValues["ID"] = ID.split("-")[0]

        if status == "ADJ":
            urlAPI = tenderAdjudicadosEndPint_V2 + ID
            adjudicados = self.__obtain_api_v2_adjudicados(urlAPI)
            if adjudicados != False:
                dicValues["Adjudicados"] = ', '.join(adjudicados)
            else:
                print("ERROR obteniendo proveedores por medio de la api V2.")
                dicValues["Adjudicados"] = " "
        
        return dicValues

    def __obtain_api_v3_tender(self, urlAPI):
        """
            retorna un json con la informacion de la licitacion indicada por medio de urlAPI
            urlAPI: endpoint de la API v3 mas el parametro del ID de la licitacion 
        """
        head = {
            "accept":"application/json",
            "Authorization":self.accessToken_V3
        }
        response = requests.get(urlAPI, headers = head)
        if response.status_code == 200:
            return response.json()
        else:
            print("V3: ", response.request.body)
            print("V3: ", response.status_code) 
            return False
    
    def __obtain_api_v2_adjudicados(self, urlAPI):
        """
            Retorna una lista de los proveedores de una licitacion
            This implementation uses API V2 (will be deprecated in June 2023).
            urlAPI: endpoint de la API v2 mas el parametro del ID de la licitacion  
        """
        
        urlAPI = urlAPI + "/proveedores"
        listAdjudicados = []
        
        head = {
            "Authorization":"Bearer " + self.accessToken_V2 
        }

        response = requests.get(urlAPI, headers = head)
        
        if response.status_code != 200:
            print("V2: ", response.request.body)
            print("V2: ", response.status_code) 
            return False           

        data = response.json()
        data = data["@graph"][0]["contrato"]["list"]
        
        for item in data:
            listAdjudicados.append(item["proveedor"]["razon_social"])
        
        return listAdjudicados