"""
    This process is in charge of reading the database filled by db_filler.py and tweet according to the information contained
    in the database.
    After tweeting, it deletes the row contained in the database.
    To prevent it from spamming, it should tweet only every X (need to define X) minutes.
    It stores the first 5 rows of the data base and tweets them in order. 
"""

from modules.bot_api import twitterBot, read_credential
from modules.sqlite_api import licitacionDataBase
from time import sleep

dataBaseName = "basicDB.db"
basicTable = "tablaBasica"
tablaConvocatoria = "tablaConvocatoria"

maxCharLimit = 280
MIN_MONTO_TUITEAR = 25000000 #monto minimo que deben de pasar las licitaciones para que sean tuiteadas

def format_number(number):
    """
    Formats a number for human readability by adding commas between thousands.
    """
    formatted_number = "{:,}".format(number)
    return formatted_number

def tweet_licitacion(bot, client, item, status):
    """
    Parses the information in a row of the database and creates three tweets, then tweets them.
    Params:
    bot: pointer to object of type twitterBot
    api: pointer to api object
    item: database individual row
    """

    if item[2] < MIN_MONTO_TUITEAR:
        print("Monto de la licitacion bajo: ", format_number(item[2]))
        return False
    
    if status == "ADJ":
        monto = format_number(item[2])
        ID = item[0]
        nombre = item[1]
        institucion = item[3]
        proveedores = item[4]
        link = item[6]

        tweet_1 = "Nombre: " + nombre + ". ID: " + ID + ". Monto[PYG]: " + monto
        if len(tweet_1) > maxCharLimit:
            tweet_1 = "ID: " + ID + ". Monto[PYG]: " + monto
        tweet_2 = "Institucion: " + institucion + ". Proveedor/es: " + proveedores
        tweet_3 = "URL: " + link	

    elif status == "CONV":
        monto = format_number(item[2])
        ID = item[0]
        nombre = item[1]
        institucion = item[3]
        link = item[4]
        tweet_1 = "Se lanza convocatoria: " + nombre + ". ID: " + ID + ". Monto[PYG]: " + monto
        if len(tweet_1) > maxCharLimit:
            tweet_1 = "Se lanza convocatoria ID: " + ID + ". Monto[PYG]: " + monto
        tweet_2 = "Institucion: " + institucion
        tweet_3 = "URL: " + link
    
    listaTweets = [tweet_1, tweet_2, tweet_3]

    id = 0
    for tweet in listaTweets:
        print("Tuiteando: ", tweet)
        id = bot.tweet(client, tweet, id)

def main():
    
    ''' Create db object and read its contents '''

    #tabla ADJ
    print("Leyendo tabla ADJ...")
    db = licitacionDataBase(dataBaseName, basicTable)
    firtsFiveRows = db.get_first_5_rows(dataBaseName, basicTable)
    if firtsFiveRows == False:
        print("Tabla Vacia, no se tuitea")
    else:
        print("Las primeras 5 filas son: ")
        print(firtsFiveRows)
        print("Deleting the first 5 rows of the table ADJ...")
        db.delete_first_5_rows(dataBaseName, basicTable)

    #tabla CONV
    print("Leyendo tabla CONV...")
    db = licitacionDataBase(dataBaseName, tablaConvocatoria)
    firtsFiveRowsCONV = db.get_first_5_rows(dataBaseName, tablaConvocatoria)
    if firtsFiveRowsCONV == False:
        print("Tabla Vacia, no se tuitea")
    else:
        print("Las primeras 5 filas son: ")
        print(firtsFiveRowsCONV)
        print("Deleting the first 5 rows of the table CONV...")
        db.delete_first_5_rows(dataBaseName, tablaConvocatoria)


    if firtsFiveRows == False and firtsFiveRowsCONV == False:
        print("Tablas vacias, cerrando programa")
        exit(1)

    ''' Create twitterBot object and authenticate '''

    credentialPath = "../credentials/twitter.json"

    consumerKey = read_credential(credentialPath, "consumer-key")
    consumerSecret = read_credential(credentialPath, "consumer-secret")
    accessToken = read_credential(credentialPath, "access-token")
    accessTokenSecret = read_credential(credentialPath, "access-token-secret")
    bearerToken = read_credential(credentialPath, "bearer-token")
    
    print("consumerKey", consumerKey)
    print("consumerSecret", consumerSecret)
    print("accessToken", accessToken)
    print("accessTokenSecret", accessTokenSecret)
    print("bearerToken: ", bearerToken)

    twBot = twitterBot(consumerKey, consumerSecret, accessToken, accessTokenSecret, bearerToken)
    cliente = twBot.oauth()
    
    ''' Tweet tenders AD '''

    if firtsFiveRows != False:
        for item in firtsFiveRows:
            tweet_licitacion(twBot, cliente, item, "ADJ")
            sleep(60)

    ''' Tweet tenders CONV'''
    if firtsFiveRowsCONV != False:
        for item in firtsFiveRowsCONV:
            tweet_licitacion(twBot, cliente, item, "CONV")
            sleep(60)

if __name__ == "__main__":
    main()