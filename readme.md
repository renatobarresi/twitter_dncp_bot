# Bot description 
## Generated by ChatGPT (will create a human mande when I have time)

El patrón arquitectónico productor-consumidor se refiere a la forma en que dos procesos pueden comunicarse y colaborar entre sí para lograr un objetivo común.

En este caso, tenemos dos procesos: "db_filler.py" y "twitter_bot.py".

El proceso "db_filler.py" se encarga de detectar los cambios en el CSV de la DNCP y cargar la base de datos con la información de las licitaciones que cambiaron de estado. Este proceso actúa como productor, ya que genera y alimenta la base de datos con información.

Por otro lado, el proceso "twitter_bot.py" se encarga de consumir la información almacenada en la base de datos y procesarla para publicar tweets en Twitter. Este proceso actúa como consumidor, ya que obtiene y procesa la información generada por el productor.

La comunicación entre estos dos procesos se realiza a través de la base de datos, que actúa como una cola de mensajes o un buffer compartido entre ellos. El productor escribe en la base de datos y el consumidor lee la información almacenada y la procesa para su uso.

La arquitectura productor-consumidor es útil cuando se necesita un procesamiento en paralelo o asincrónico de datos y también es útil para equilibrar la carga de trabajo entre diferentes procesos. En este caso, el proceso "db_filler.py" se encarga de la tarea pesada de detectar y procesar los cambios en el CSV de la DNCP, mientras que el proceso "consumer.py" se encarga de publicar los tweets de manera más rápida y eficiente.

En resumen, la arquitectura productor-consumidor permite a dos procesos trabajar en conjunto de manera eficiente y equilibrada para lograr un objetivo común, a través de la comunicación y el intercambio de información a través de una base de datos o buffer compartido.