<h1 align="center"> Manual de Usuario "Linea de comando" </h1>

## Tabla de Contenidos

- [Descripción](#descripción)
- [Uso](#uso)
- [Contribución](#contribución)

## Descripción

El programa desarrollado como proyecto final de la materia Sistemas Operativos de la Universidad del Valle
esta compuesto de 2 formas de ejecución.
La primera de ellas consiste en una GUI interactiva para el uso del usuario.
La segunda consiste en una aplicación de consola destinada al uso practico del programa, y
sobre la cual trataremos a continuación

## Uso

1. Debemos registrar nuestro en la aplicación de consola por medio de la palabra
   reservada "register", y posteriormente ingresamos los datos "name", "mail" y
   "password" en ese exacto orden.
   
   ```Consola
   register name mail password
   ```

2. Ahora debemos logearnos con los datos anteriormente ingresados, junto con la
   palabra "login" de la siguiente manera:

   ```Consola
   login mail password
   ```

3. Podemos usar la palabra "gete" para obtener todas las ejecuciones que ha hecho
   la persona.

4. Para ejecutar comandos de la propia terminal de linux usamos el comando "shell" junto al comando
   de Linux, o por otro lado tambien podemos usar "!" + el comando

5. Usamos el comando "exec" el cual solo puede ser ejecutado una vez el usuario ya se encuentre
   logueado en la app, este recibe 2 argumentos. Primero ejecuta el script donde tengamos los tiempos
   de cada uno de los procesos y el algoritmo que queremos usar "fcfs, rr, srn, etc", este nos imprimira
   los tiempos tomados para c/u de los comandos que hayamos ingresado.

6. "Aclaracion" El chiste aqui es que creemos por medio del comando shell nuestro .txt y en
   este hayamos agregado lo anteriormente mencionado, el comando y los tiempos de la siguiente forma:

         * comando,tiempo de inicio,tiempo estimado  salto de linea

   Es muy importante que siga esa estructura, con las comas incluidas, porque sino nos dará error

7. Antes de desloguearnos de la aplicación de consola, es importante que el usuario sepa acerca de unas
   funcionalidades adicionales:

   rept : Este comando repite una ejecucion en concreto con cualquier algoritmo que el usuario desee

         * rept <id de la ejecución> <algoritmo>

   clean : Limpia todas las ejecuciones que tenga un usuario

         * clean
   
   pro : muestra el nombre y correo del usuario

         * pro

   edit : Se le permite al usuario actualizar su nombre y el email registrados

         *  edit name <nuevo nombre> email <nuevo email>

8. Por ultimo, podemos deslogearnos de la App por medio de la palabra "logout"
9. Salimos de la App con "exit"


## Contribución

Aplicacion Creada Por:
- Juan Francesco García Vargas - 2310174
- Juan Jose Mafla Pacheco - 2126990
- Juan David Pinto Rodriguez - 2240440
- Juan Fernando Calle Sanchez - 2127464
- Jose Adrian Marin Ordoñez - 2126988
