# SQLItimebased
Script en Python para automatizar un dump de la información de un SQL Injection Time Based, es bastante sencillo el funcionamiento y utilizarlo.

Únicamente hay que descargar el .py cambiar un par de cosas del código y a probarlo, a continuación explicaré que cosas hay que cambiar. El funcionamiento del script es simplemente enviar un payload con la inyección SQL y comprobar el tiempo de respuesta del servidor para por fuerza bruta sacar:

  - Nombre de la base de datos
  - Tablas
  - Columnas
  - Datos

# DATOS A CAMBIAR

# "DICCIONARIO y URL"

![image](https://user-images.githubusercontent.com/92856868/138082909-0c9f87e5-9e5a-4218-8f55-8cb9ee659dc3.png)

Debéis cambiar la url por la que estéis inyectando en ese momento.

Aquí también vemos que tenemos la variable scompleto y sbasico; Los números que veis es debido a que la búsqueda se realiza en ASCII, el básico es únicamente con minúsculas y números, el completo tiene minúsculas, mayúsculas, números y caracteres especiales. Dependiendo cual queráis usar únicamente tenéis que cambiarlo despues de s =

¿Por qué están desordenados los números de ASCII?

Porque están en un orden muy concreto, os explico el completo y entendéis perfectamente:

En primer lugar están las minúsculas ordenadas por porcentajes de aparición en textos de habla inglesa, a continuación los números, después las mayúsculas en el mismo orden que las minúsculas y por último los caracteres especiales.

Tras hacer algunas pruebas realizarlo en este orden me ahorra hasta la mitad de tiempo en la ejecución del script a la hora de buscar.

# TIEMPO

![image](https://user-images.githubusercontent.com/92856868/138083383-6f89d623-b0ae-4482-b834-24007c1d8474.png)

Poned la cantidad de segundos que se realizará la petición del servidor para confirmar si el caracter es el correcto, 2 segundos es lo mínimo que me ha funcionado, pero si el servidor va lento puede dar falsos positivos y es preferible aumentarlo.

# POST

![image](https://user-images.githubusercontent.com/92856868/138083622-ac7d3e63-94bb-43c4-9e16-3f2062486704.png)

En data_post tendremos que cambiar username y password por la petición que se realiza al servidor concretamente, podéis mirarlo a través de Burpsuite o herramientas del desarrollador de los distintos navegadores. En este caso era un formulario de login.

