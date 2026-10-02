# CONQUER PLANNER

## Guía personal del proyecto

Este archivo es mi guía personal para entender cómo he construido Conquer Planner.

La aplicación empezó como un planificador académico sencillo ejecutado desde la terminal.

La idea es ir evolucionándola poco a poco hasta convertirla en una aplicación más completa y, si finalmente lo decido, utilizarla también desde el móvil.

---

# 1. ¿QUÉ ES CONQUER PLANNER?

Conquer Planner es mi aplicación personal de planificación académica.

Su objetivo es ayudarme a:

- crear tareas;
- ponerles una fecha límite;
- asignarles una prioridad;
- clasificarlas por categorías;
- marcarlas como completadas;
- eliminarlas;
- consultar mi progreso;
- definir un objetivo;
- indicar cuántas horas necesito;
- indicar cuánto tiempo tengo disponible cada día;
- calcular si tengo suficiente tiempo disponible para alcanzar mi objetivo.

Actualmente funciona desde la terminal.

---

# 2. ESTRUCTURA DEL PROYECTO

Actualmente el proyecto tiene aproximadamente esta estructura:

conquer-planner/
│
├── main.py
├── tareas.py
├── utilidades.py
├── tareas.json
├── planificacion.json
├── README.md
├── requirements.txt
├── GUIA_PROYECTO.md
├── tests/
│ └── test_tareas.py
│
├── .gitignore
├── .git/
└── .venv/

Cada elemento tiene una función diferente.

---

# 3. main.py

main.py es el archivo principal de la aplicación.

Es el archivo que inicia el programa.

Se encarga principalmente de:

- mostrar el menú;
- recibir la opción que selecciono;
- cargar las tareas;
- cargar la planificación;
- llamar a las funciones correspondientes;
- mantener funcionando el programa hasta que elijo salir.

En otras palabras:

main.py = CONTROL DE LA APLICACIÓN

No debería contener toda la lógica del programa.

Por eso muchas funciones están separadas en otros archivos.

---

# 4. tareas.py

tareas.py contiene la lógica relacionada con las tareas.

Aquí tenemos funciones como:

- cargar_tareas()
- guardar_tareas()
- pedir_numero_tarea()
- pedir_prioridad()
- añadir_tarea()
- mostrar_tareas()
- completar_tarea()
- eliminar_tarea()
- mostrar_progreso()

La idea es separar la lógica de las tareas del menú principal.

Por ejemplo:

main.py pregunta:

"¿Qué quieres hacer?"

Si selecciono "Añadir tarea", main.py llama a:

añadir_tarea()

La función añadir_tarea() está definida en tareas.py.

---

# 5. utilidades.py

utilidades.py contiene funciones auxiliares.

Son funciones que pueden ser útiles para distintas partes del programa.

Por ejemplo:

- validar fechas;
- calcular horas hasta un objetivo.

La idea es evitar meter toda la lógica en main.py.

---

# 6. tareas.json

tareas.json es donde se guardan las tareas.

JSON es un formato utilizado para almacenar datos.

Por ejemplo, una tarea puede tener una estructura parecida a:

{
"nombre": "Estudiar Python",
"fecha_limite": "10/10/2026",
"prioridad": "Alta",
"categoria": "Python",
"completada": false
}

Esto significa:

nombre:
nombre de la tarea.

fecha_limite:
fecha en la que quiero terminarla.

prioridad:
Alta, Media o Baja.

categoria:
categoría a la que pertenece.

completada:
indica si la tarea está terminada.

false significa que no está terminada.

true significa que está terminada.

---

# 7. planificacion.json

planificacion.json guarda la información general de mi planificación.

Puede contener:

- fecha objetivo;
- horas estimadas necesarias;
- horas disponibles cada día de la semana.

Por ejemplo:

{
"fecha_objetivo": "31/03/2027",
"horas_estimadas": 100.0,
"disponibilidad": {
"Lunes": 2.0,
"Martes": 2.0,
"Miércoles": 2.0,
"Jueves": 2.0,
"Viernes": 2.0,
"Sábado": 4.0,
"Domingo": 4.0
}
}

---

# 8. ¿QUÉ ES UNA FUNCIÓN?

Una función es un bloque de código que realiza una tarea concreta.

Por ejemplo:

def mostrar_tareas(tareas):

    ...

La palabra "def" significa que estamos definiendo una función.

"mostrar_tareas" es el nombre de la función.

"(tareas)" significa que la función recibe información llamada tareas.

Una función permite evitar repetir código.

En lugar de escribir diez veces cómo mostrar las tareas, lo escribimos una vez dentro de mostrar_tareas() y después llamamos a esa función cuando la necesitamos.

---

# 9. ¿QUÉ HACE cargar_tareas()?

cargar_tareas() lee el archivo tareas.json.

Primero comprueba si el archivo existe.

Si no existe:

    devuelve []

Los corchetes vacíos representan una lista vacía.

Después intenta abrir el archivo.

Utiliza JSON para convertir la información guardada en Python.

También comprueba que los datos tengan un formato correcto.

Esto es importante porque un archivo puede estar:

- vacío;
- corrupto;
- escrito con un formato inesperado;
- utilizando un formato antiguo.

La función intenta corregir algunos datos antes de devolverlos.

---

# 10. ¿QUÉ HACE guardar_tareas()?

guardar_tareas() hace lo contrario que cargar_tareas().

cargar_tareas():

    JSON -> Python

guardar_tareas():

    Python -> JSON

Cuando añado, completo o elimino una tarea, los cambios tienen que guardarse en tareas.json.

Así no se pierden cuando cierro el programa.

---

# 11. ¿POR QUÉ UTILIZAMOS JSON?

Porque es una forma sencilla de guardar información.

Para esta primera versión de la aplicación no necesitamos todavía una base de datos.

JSON es fácil de:

- leer;
- modificar;
- guardar;
- cargar;
- utilizar desde Python.

Más adelante, si la aplicación crece, podremos estudiar otras opciones.

---

# 12. ¿QUÉ ES pytest?

pytest es una herramienta para realizar pruebas automáticas en Python.

En nuestro proyecto lo instalamos porque queremos comprobar automáticamente que determinadas partes del programa funcionan correctamente.

Lo instalamos dentro del entorno virtual.

La versión que dejamos fijada inicialmente es:

pytest==8.4.2

Está indicada en:

requirements.txt

---

# 13. ¿QUÉ ES requirements.txt?

requirements.txt contiene las dependencias de Python que necesita el proyecto.

Actualmente contiene:

pytest==8.4.2

Esto permite saber qué versión de pytest utilizamos.

Si otra persona descarga el proyecto, puede instalar las dependencias utilizando:

python3 -m pip install -r requirements.txt

---

# 14. ¿QUÉ ES tests/test_tareas.py?

Es el archivo donde escribimos las pruebas automáticas de las tareas.

El archivo está dentro de:

tests/

Por convención, pytest busca archivos que empiezan por:

test\_

y funciones que empiezan por:

test\_

---

# 15. ¿QUÉ SIGNIFICA tmp_path?

En nuestras pruebas utilizamos:

tmp_path

tmp_path es una funcionalidad de pytest.

Nos proporciona una carpeta temporal para hacer pruebas.

Esto es importante porque no queremos que las pruebas modifiquen mi verdadero:

tareas.json

En lugar de eso, cada prueba crea temporalmente su propio archivo.

---

# 16. PRIMER TEST

Tenemos una prueba llamada:

test_cargar_tareas_con_formato_antiguo()

Esta prueba comprueba que cargar_tareas() puede trabajar con información antigua.

Por ejemplo, una tarea antigua puede aparecer simplemente como:

"Estudiar Python"

Mientras que una tarea nueva utiliza un diccionario con varios campos.

La función cargar_tareas() convierte la tarea antigua a un formato completo.

Por ejemplo:

"Estudiar Python"

se transforma en algo parecido a:

{
"nombre": "Estudiar Python",
"fecha_limite": "",
"prioridad": "Media",
"categoria": "General",
"completada": False
}

El test comprueba que esto ocurre correctamente.

---

# 17. SEGUNDO TEST

Tenemos:

test_cargar_tareas_corrige_datos_invalidos()

Esta prueba comprueba qué ocurre cuando hay datos incorrectos.

Por ejemplo:

prioridad:

"Urgente"

Pero las prioridades permitidas son:

- Alta
- Media
- Baja

Por eso se espera que el programa sustituya:

"Urgente"

por:

"Media"

También comprobamos que una tarea sin nombre se descarte.

Esto hace que el programa sea más resistente frente a datos incorrectos.

---

# 18. TERCER TEST

Tenemos:

test_cargar_tareas_con_json_no_lista()

Esta prueba comprueba qué ocurre si tareas.json contiene algo que no es una lista.

Por ejemplo:

{
"tarea": "Estudiar"
}

No es el formato esperado.

El programa devuelve:

[]

Es decir:

una lista vacía.

---

# 19. ¿QUÉ SIGNIFICA assert?

En los tests utilizamos:

assert

Por ejemplo:

assert len(tareas) == 2

Esto significa:

"Comprueba que la cantidad de tareas sea exactamente 2."

Si la condición es verdadera:

la prueba continúa.

Si es falsa:

la prueba falla.

Otro ejemplo:

assert tareas[0]["prioridad"] == "Media"

Significa:

"Comprueba que la prioridad de la primera tarea sea Media."

---

# 20. ¿QUÉ SIGNIFICA python3 -m pytest?

Cuando escribo:

python3 -m pytest

estoy pidiendo a Python que ejecute pytest.

pytest busca automáticamente las pruebas del proyecto.

Si aparece algo como:

3 passed

significa que las tres pruebas han pasado correctamente.

Por ejemplo:

collected 3 items

tests/test_tareas.py ... [100%]

3 passed

Esto significa que tenemos tres pruebas y las tres han funcionado.

---

# 21. ¿QUÉ ES .venv?

.venv es el entorno virtual de Python del proyecto.

Es una especie de entorno independiente para instalar las herramientas y librerías que utiliza este proyecto.

En nuestro caso aparece al principio de la terminal:

(.venv)

Eso indica que el entorno virtual está activado.

Es recomendable trabajar con un entorno virtual para evitar mezclar las dependencias de diferentes proyectos.

---

# 22. ¿QUÉ ES Git?

Git es un sistema de control de versiones.

Sirve para guardar el historial de cambios del proyecto.

Gracias a Git podemos saber:

- qué cambiamos;
- cuándo lo cambiamos;
- qué archivos modificamos;
- volver a versiones anteriores si algo sale mal.

---

# 23. ¿QUÉ ES GitHub?

GitHub es donde tenemos almacenado el repositorio remoto del proyecto.

Nuestro proyecto está conectado a GitHub.

Por eso podemos utilizar:

git push

para enviar nuestros cambios desde el ordenador a GitHub.

---

# 24. git status

Cuando escribimos:

git status

Git nos dice qué está pasando en el proyecto.

Por ejemplo:

- qué archivos han cambiado;
- qué archivos son nuevos;
- qué archivos están preparados para un commit;
- si tenemos cambios pendientes.

Es uno de los comandos que utilizaremos con frecuencia.

---

# 25. git add

Cuando hacemos:

git add archivo.py

le estamos diciendo a Git:

"Quiero incluir este cambio en el próximo commit."

También podemos añadir varios archivos.

Por ejemplo:

git add requirements.txt tests/

---

# 26. git commit

Después hacemos un commit.

Por ejemplo:

git commit -m "Añadir pruebas para gestión de tareas"

Un commit es como una fotografía del estado del proyecto en ese momento.

El mensaje explica qué hemos cambiado.

---

# 27. git push

Después de hacer commit podemos hacer:

git push

Esto envía nuestros commits al repositorio de GitHub.

La secuencia habitual es:

1. modificar código;
2. probar;
3. git status;
4. git add;
5. git commit;
6. git push.

No debemos hacer commit y push automáticamente después de cualquier pequeño cambio sin comprobar antes que todo funciona.

---

# 28. IMPORTANTE: TERMINAL VS PYTHON

Hay dos cosas diferentes:

TERMINAL:

Aquí escribimos comandos como:

python3 -m pytest

git status

git add .

git commit -m "mensaje"

git push

PYTHON:

Aquí escribimos código como:

def mostrar_tareas(tareas):
...

No debemos pegar código Python directamente en la terminal esperando que zsh lo interprete.

Si queremos modificar Python, modificamos el archivo .py.

---

# 29. ¿QUÉ SIGNIFICA zsh: parse error near '('?

Si aparece:

zsh: parse error near '('

normalmente significa que hemos pegado código que la terminal no entiende como un comando.

Por ejemplo, pegar directamente:

def algo():
...

en la terminal.

La terminal utiliza zsh.

zsh NO es Python.

Por eso debemos distinguir siempre entre:

comandos de terminal

y

código Python.

---

# 30. ¿CÓMO ESTAMOS CONSTRUYENDO LA APLICACIÓN?

No estamos intentando hacer toda la aplicación de golpe.

La estamos construyendo por capas.

FASE 1:
Aplicación básica de terminal.

FASE 2:
Gestión de tareas.

FASE 3:
Guardado de datos.

FASE 4:
Planificación y disponibilidad.

FASE 5:
Tests automáticos.

FASE 6:
Mejorar la estructura y calidad del código.

FASE 7:
Crear una interfaz gráfica.

FASE 8:
Decidir si convertirla en aplicación de ordenador, móvil o ambas.

---

# 31. ¿POR QUÉ NO HACEMOS TODO DE GOLPE?

Porque quiero entender lo que estoy construyendo.

Una aplicación grande puede funcionar, pero si no entiendo el código después será difícil:

- modificarla;
- detectar errores;
- añadir funcionalidades;
- mantenerla.

Por eso primero construimos una base sencilla y después la hacemos crecer.

---

# 32. ESTADO ACTUAL DEL PROYECTO

Actualmente ya tenemos:

- gestión de tareas;
- tareas completadas;
- prioridades;
- categorías;
- fechas;
- eliminación de tareas;
- progreso;
- planificación;
- disponibilidad semanal;
- cálculo de horas;
- almacenamiento en JSON;
- tests con pytest;
- requirements.txt;
- repositorio Git;
- repositorio GitHub.

Además, las pruebas actuales pasan correctamente.

Último resultado conocido:

3 passed

---

# 33. PRÓXIMOS PASOS

No debemos añadir funcionalidades al azar.

El siguiente objetivo es mejorar la aplicación de forma ordenada.

Primero:

- revisar la arquitectura;
- detectar posibles errores;
- mejorar los tests;
- evitar duplicación;
- preparar el código para una futura interfaz gráfica.

Después podremos empezar a construir la interfaz.

---

# 34. POSIBLE FUTURO: APLICACIÓN DE ORDENADOR

Podemos convertir Conquer Planner en una aplicación con ventanas.

En lugar de utilizar solamente:

1. Ver objetivo
2. Añadir tarea
3. Ver tareas

podríamos tener botones, listas, formularios, calendarios y gráficos.

---

# 35. POSIBLE FUTURO: APLICACIÓN MÓVIL

También podemos adaptar el proyecto para utilizarlo desde el móvil.

La lógica que ya hemos construido puede servir como base.

Pero una aplicación móvil necesita además:

- interfaz táctil;
- navegación;
- almacenamiento adecuado;
- adaptación a pantallas pequeñas;
- empaquetado para el sistema operativo;
- pruebas en móvil.

No tenemos que decidirlo todavía.

---

# 36. REGLA PERSONAL PARA ESTE PROYECTO

No quiero copiar código sin entenderlo.

Cada vez que añadamos algo nuevo debo saber:

1. Qué problema estamos solucionando.
2. En qué archivo lo hacemos.
3. Qué función estamos modificando o creando.
4. Qué hace el código.
5. Cómo lo comprobamos.
6. Cómo sabemos que no hemos roto lo anterior.
7. Si merece la pena guardar el cambio en Git.

---

# 37. REGLA PARA LOS CAMBIOS

Antes de cambiar código:

- entender qué queremos conseguir;
- comprobar cómo funciona actualmente;
- hacer el cambio mínimo necesario;
- ejecutar las pruebas;
- revisar el resultado;
- guardar el cambio en Git cuando tenga sentido.

No repetir pasos que ya están hechos.

No crear archivos duplicados.

No copiar varias veces la misma función.

No utilizar nano.

---

# 38. OBJETIVO FINAL

La meta no es solamente tener una aplicación que funcione.

La meta es:

CONSTRUIR UNA APLICACIÓN QUE YO ENTIENDA.

Quiero poder mirar el proyecto y entender:

- cómo funciona;
- dónde se guardan los datos;
- cómo se crean las tareas;
- cómo se calculan las horas;
- cómo funcionan los tests;
- cómo se organiza el código;
- cómo añadir nuevas funcionalidades.

Y posteriormente poder utilizar Conquer Planner como mi propio planificador personal.

---

# 39. COMANDOS BÁSICOS QUE DEBO RECORDAR

Comprobar archivos:

ls

Ver estructura:

find . -maxdepth 2 -type f | sort

Abrir un archivo en el terminal:

cat nombre_archivo

Ejecutar la aplicación:

python3 main.py

Ejecutar las pruebas:

python3 -m pytest

Ver estado de Git:

git status

Añadir cambios:

git add nombre_archivo

Crear commit:

git commit -m "Descripción del cambio"

Enviar a GitHub:

git push

---

# 40. IDEA PRINCIPAL

No necesito memorizar todos los comandos.

Necesito entender qué estoy haciendo.

La terminal es la herramienta.

Python es el lenguaje.

Git controla las versiones.

GitHub guarda el repositorio remoto.

pytest comprueba que el código funciona.

JSON guarda nuestros datos.

Los archivos .py contienen el programa.

Y Conquer Planner es el proyecto que estamos construyendo.
