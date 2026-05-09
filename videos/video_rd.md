Con este boom que ha tenido la
inteligencia artificial en los últimos
años, creo que todos hemos escuchado
hablar de que este modelo o este otro
fue entrenado con miles de millones de
datos y que por eso ha aprendido a
interpretar texto o a interpretar
imágenes. Pero vale la pena preguntarnos
qué significa realmente que una red
neuronal sea entrenada y qué es lo que
en última se está aprendiendo. Es decir,
en el fondo, cómo logramos que a partir
de los datos y con un sistema de
cómputo, estos modelos logren realizar
tareas como comprender el texto o
comprender el contenido de las imágenes.
Pues en este video les voy a explicar
precisamente de forma intuitiva qué es
el entrenamiento de una red neuronal,
cómo se lleva a cabo este entrenamiento
y a qué nos referimos cuando decimos que
estos modelos o estas redes están
aprendiendo algo de los datos. Así que
si están incursionando hasta ahora a
este mundo de la inteligencia artificial
y de las redes neuronales, pues este
video es ideal porque les va a permitir
tener una idea bastante precisa de cómo
es que se construyen estos modelos para
implementar una amplia variedad de
aplicaciones. Y recuerden también que si
les gusta este tipo de contenido, desde
ya los invito a darle un pulgar hacia
arriba de me gusta a este video y a que
lo compartan con todos sus amigos y
conocidos, pues esto me va a ayudar un
montón a seguir llevando este contenido
cada vez a más y más personas. Y si aún
no lo han hecho, los invito a
suscribirse al canal y activar la
campanita para que YouTube les notifique
cada vez que publique un nuevo video.
Pero antes de comenzar, los invito a
visitar codificandobits.com
en donde encontrarán la academia online
con cursos de inteligencia artificial,
ciencia de datos y machine learning que
les permitirán construir su carrera en
estas áreas y todo por una suscripción
mensual de tan solo $10. Además, se
podrán poner en contacto conmigo si
están interesados en asesorías para el
desarrollo de proyectos o cursos de
formación personalizada. Así que listo,
comencemos.
Supongamos un problema hipotético.
Supongamos que tenemos una persona
experta en predecir la probabilidad de
lluvia con base en cierta información.
Entonces esa persona tiene muchos años
de experiencia y simplemente con
analizar variables como, por ejemplo, la
temperatura, la humedad del ambiente o
la velocidad del viento, logra predecir
con bastante precisión la probabilidad
de lluvia. Entonces, por ejemplo, si la
temperatura es de 10ºC, la humedad es
del 80% y la velocidad del viento es de
20 km/h, esa persona predice que la
probabilidad de lluvia es del 98%. Y
supongamos que lo que queremos es
construir un sistema computacional que
sea capaz de entregar resultados
similares a los que entrega este
experto. Es decir, tendremos acá un
sistema que no sabemos qué
características tendrá, pero que si
introducimos una temperatura de 10ºC,
una humedad del 80% y un valor de la
velocidad del viento de 20 km/h, a la
salida debería entregarnos una
probabilidad de lluvia predicha del 99%.
Y acá es importante resaltar el término
predicha. porque no es el valor real,
porque vamos a tomar como referencia de
ese valor real la probabilidad que
estima el experto que tiene muchos años
de experiencia que es del 98%. Entonces,
probablemente este sistema computacional
va a arrojarnos un valor que no va a ser
exactamente el mismo del experto, pero
que idealmente debería estar muy cerca.
Y para entender qué características
tendría este sistema computacional,
vamos a simplificar un poco las cosas.
Entonces, acá tenemos nuestro problema
de predicción, la predicción que va a
realizar el experto en meteorología y lo
que vamos a hacer es darle un nombre a
esas variables de entrada. Entonces, a
la temperatura la vamos a llamar la
variable x1, tiene un valor de 10. La
humedad la vamos a llamar x2, pero en
lugar de colocar un porcentaje, vamos a
escribir como un valor entre 0 y 1. Es
decir, una humedad del 80% sería
equivalente a un valor de 0.8. y la
velocidad del viento, la variable x3,
tendría un valor de 20. Y el valor que
se predice, la probabilidad de lluvia,
entonces en lugar de escribirlo como 98%
lo escribimos como 0,98. Estas variables
de entrada se conocen precisamente como
características o variables del
problema. Y la probabilidad de lluvia en
nuestro caso la vamos a llamar la
variable Y, que es la variable a
predecir. De igual forma, entonces, si
tenemos nuestro sistema, que tiene estas
tres variables de entrada y que intenta
predecir la probabilidad de lluvia, pues
usando esa misma anotación tendremos las
variables x1, x2 y x3, que también se
conocen como características. Y la
salida de ese sistema la vamos a llamar
la predicción. Y para diferenciarla de
la y que usamos en el valor de
referencia, en el valor real, le vamos a
poner un gorro. La vamos a llamar y
gorro y es la predicción que haría ese
sistema. Entonces, habiendo aclarado
esto, veamos un sistema muy simple que
se podría implementar en este problema
hipotético. Ese sistema es básicamente
una neurona artificial. De las neuronas
artificiales ya les hablo en un video
que les dejo por acá enlazado, pero
básicamente tiene una serie de
elementos. A esa neurona artificial
entran las variables X1, X2 y X3. Esas
variables pasan o son procesadas por una
serie de parámetros que están acá en
rojo. Esos parámetros son elementos
claves de los cuales vamos a hablar a lo
largo de todo el video, pero por ahora
pensemos que son simplemente cantidades
numéricas, unos coeficientes. Y esos
coeficientes se combinan con las
variables de entrada y pasan por un
bloque que vamos a llamar transformación
y después de eso pasan por algo que se
conoce como una función de activación. y
a la salida tenemos la predicción.
Entonces, esto en términos generales una
neurona artificial.
Y entonces entendamos con un sencillo
ejemplo cómo es que una neurona
artificial genera una predicción a
partir de unas variables de entrada.
Supongamos que tenemos las variables de
entrada de nuestro problema. X1, la
temperatura 10ºC.
X2, la humedad del ambiente, 80% o 0.8.
y X3, la velocidad del viento, 20 km/h.
Cada una de esas variables pasa por
estos parámetros y vamos a suponer que
estos parámetros tienen unos ciertos
valores. Por ahora no nos interesa
entender cómo encontraremos estos
valores, pero simplemente asumamos que
los valores son ω3
y el parámetro B es de 0.3. ¿Cómo se
combinan esas variables de entrada con
estos parámetros de la neurona
artificial? pues a través de la
transformación. Y en esa transformación
básicamente lo que se hace es calcular
una cantidad numérica Z, que es el
resultado de combinar linealmente las
variables de entrada. Es decir, la
variable de entrada x1 temperatura se
multiplica por omega1. A eso se le suma
la variable de entrada x2, la humedad
multiplicada por omega2. A eso se le
suma la variable 3, velocidad del viento
multiplicada por óega3 y a ese resultado
se le suma b que es 0.3. 3. Y si hacemos
esas operaciones, tendríamos 0.3 * 10 +
0.4 * 08 + 03 * 20 + 0.3. Y eso sería 3
+ 0.32 + 6 +.3. Y esto sumado nos da una
cantidad numérica que es 962. Y esa
cantidad numérica es, digamos, como una
representación compacta de los datos de
entrada. Y ese valor de Z se lleva a lo
que se conoce como una función de
activación. De las funciones de
activación. Yo les hablo también en otro
video, pero en esencia, por ejemplo, en
esta neurona artificial podemos usar una
función que se conoce como la función
sigmoidal, que matemáticamente obedece a
esta expresión, donde esa e es una
función exponencial. Y entonces si
reemplazamos el valor de z en esta
función del lado derecho, pues tendremos
que la predicción y gorro va a ser 1
sobre 1 + la exponencial con el
exponente -962. Y si hacemos ese cálculo
nos da un valor de 0,99. ¿Cómo
interpretamos esta predicción sencilla?
Pues básicamente lo que nos estaría
diciendo esta neurona artificial es que
si la temperatura de entrada son 10ºC,
la humedad es del 80% y la velocidad del
viento es 20 km/h, con esos parámetros
que están en color rojo, con esos
valores específicos, tendríamos una
probabilidad de lluvia predicha del 99%.
Y acá con este sencillo ejemplo podemos
entender algo clave que va a resultar
esencial para entender posteriormente
qué es esto del entrenamiento y el
aprendizaje en las redes neuronales. Y
es que esa predicción que acabamos de
obtener de 0,99 depende de los
parámetros de la neurona artificial. Es
decir, acá tenemos las mismas entradas
10, 08 y 20. Si los parámetros de la
neurona son 03, 04, 03 y 03, la
predicción es 0,99.
Pero si cambiamos esos parámetros
ligeramente, por ejemplo, si 1 es -.1, ω
-.2, ω3 es punto 1 y b = -05, la
predicción ahora es 0,58.
Mientras que si ahora
es -01, ω 1,3 es 02 y b -0.2, la
predicción ahora es 0,94. Esto quiere
decir que los parámetros no se escogen
de forma arbitraria, sino que debe
existir alguna forma de determinar los
valores ideales de esos parámetros para
que la predicción se acerque al valor
real. Y entonces en este punto vale la
pena hacernos esta pregunta, ¿cómo saber
si las predicciones son buenas o malas?
Es decir, si lo que predice la neurona
artificial se acerca lo suficientemente
o no a ese valor real. Y entonces
volvamos a nuestro ejemplo. El experto,
digamos, es el que nos define ese valor
real y el experto está prediciendo que
para esos valores de entrada existe un
98% de probabilidad de lluvia. Y
entonces acabamos de ver que con una
primera neurona, con ese set de
parámetros que tenemos, la predicción es
de 0,99. Es decir, para esa neurona, con
esos parámetros, la predicción está muy
cerca del valor real. El valor real es
08, la predicción es 0,99. Pero si
cambiamos esos parámetros en la neurona
2, la predicción ya baja a 0,58 y por
tanto ya está muy lejos de ese valor
real. Mientras que si tenemos una
tercera neurona con otro set de
parámetros, la predicción es 0,94, que
está relativamente cerca del valor real.
Y entonces si comparamos las tres
situaciones, neurona 1, una predicción
de 099, neurona 2, 058, neurona 3, 094,
¿cómo podemos responder a la pregunta de
cómo determinamos qué tan buenas son las
predicciones? Pues acá es donde aparece
un concepto clave que es la pérdida. Y
la pérdida, cuando estamos hablando de
una neurona artificial, es algo que nos
permite cuantificar, es decir, ponerle
números, ¿a qué tanto se acercan las
predicciones? Al valor real.
Entre más pequeña sea esa perdida, mejor
va a hacer la predicción. Es decir,
entre más cerca esté una predicción del
valor real, la pérdida va a ser más
pequeña y por tanto tendremos mejores
predicciones. Y acá podemos, para el
caso de este ejemplo, definir una
pérdida muy sencilla. En la práctica, la
ecuación matemática que se usa
convencionalmente es más compleja, se
conoce como la entropía cruzada, de la
cual les hablo en un video que les dejo
acá enlazado. Pero para el propósito de
este video, vamos a suponer que la
pérdida es simplemente el valor real y
menos el valor predicho. Y gorro. Y
entonces calculemos esa pérdida para
cada una de las tres neuronas que
tenemos en la parte de arriba. En el
primer caso tendríamos 098 - 099, es
decir, esa pérdida es de -0.01.
En el segundo caso tendríamos 0,98 - 058
04 y en el tercer caso, 098 - 094, es
decir 0.04.
De esas tres pérdidas que calculamos, si
analizamos solo la magnitud, si nos
olvidamos de los signos negativos, pues
podríamos decir que la neurona 1 tiene
la pérdida más pequeña de 0.01 en
magnitud.
La tercera neurona tiene la segunda
pérdida más pequeña, 0.04 y la tercera
neurona, la tercera pérdida más pequeña,
es decir, un valor de 04. Es decir, que
de estas tres neuronas que tenemos acá,
la que tiene el mejor desempeño, es
decir, la que genera mejores
predicciones es la neurona 1, porque
tiene una pérdida pequeña y por tanto
esa predicción 099 se acerca bastante al
valor real, 08.
Así que teniendo claro esto, ahora lo
que nos interesa es ver de forma clara
cuál es la relación que hay entre los
parámetros de la neurona y el valor de
la pérdida. Entonces, acá tenemos
nuevamente nuestros tres modelos y lo
que podemos preguntarnos en este punto
es, ¿qué hace que una neurona genere
mejores o peores predicciones? Y la
respuesta a esto está precisamente en
los parámetros de la neurona. Así que lo
que podemos decir es que dependiendo del
valor que tengan esos parámetros, la
pérdida va a ser más grande o más
pequeña. Pero además de eso, dependiendo
del valor de los parámetros, vamos a
tener peores o mejores predicciones.
Así que en este punto ya estamos listos
para definir qué es el entrenamiento y
qué es el aprendizaje en el caso de una
neurona. Entonces, acá tenemos una
neurona y vamos a suponer que tiene
cuatro parámetros:1, ω, ω.
Vamos a asumir que esos parámetros son
como perillas que podemos girar de un
lado o del otro y que dependiendo de la
posición que tengan esas perillas o de
los valores de los parámetros, tendremos
mejores o peores predicciones. Es decir,
tendremos pérdidas más pequeñas, mejores
predicciones, o pérdidas más grandes,
peores predicciones. Y entonces, la
pregunta que nos podemos plantear acá
es, ¿cómo encontrar automáticamente el
valor de los parámetros para que la
pérdida sea mínima? Y automáticamente
quiere decir que nosotros no tenemos que
fijar esos valores, sino que algún tipo
de algoritmo computacional debería
encontrarlos por sí solo. Esto es
equivalente a preguntarnos cómo
encontrar automáticamente esa posición
de las perillas para generar las mejores
predicciones. Y la respuesta a estas
preguntas es precisamente entrenando la
neurona. Entonces, entendamos qué es el
entrenamiento. Para hacer el
entrenamiento, ya no basta con tener un
único dato. Si volvemos a nuestro
problema de predecir la probabilidad de
lluvia con base en la temperatura X1, en
la humedad X2 y en la velocidad del
viento, X3. Con un solo dato no es
suficiente porque probablemente esas
variables van a cambiar continuamente y
tenemos que tener una neurona que sea
capaz de capturar todos esos patrones en
esas variables para predecir de la forma
más precisa posible la probabilidad de
lluvia. Entonces, lo que vamos a tener
es un conjunto de datos. Acá tenemos una
tabla de datos donde cada fila es una
tripleta de temperatura, humedad y
velocidad del viento. Entonces,
recolectamos una gran cantidad de
características de datos y por cada una
de esas tripletas recolectamos los
valores reales de probabilidad de lluvia
que nos entrega el experto. Y esto es lo
que conocemos como nuestro set de
entrenamiento. Teniendo este set de
entrenamiento, ya tenemos el insumo
principal con el cual vamos a poder
entrenar la neurona. ¿Cómo es este
proceso de entrenamiento? Entonces,
inicialmente, como no sabemos cuáles son
los valores ideales de esos parámetros o
las posiciones ideales de esas perillas,
pues vamos a asignarles valores o
posiciones aleatorias. Y el primer paso
entonces es presentarle a esa neurona
todos los datos de entrenamiento, las
características y por cada una de esas
filas de características que tenemos se
genera una predicción. Entonces, lo que
tenemos es un y gorro, que son todas las
predicciones. La idea ahora entonces es
comparar esas predicciones, lo que está
en y gorro con los valores reales, que
es el arreglo y ahí calculamos una
pérdida, pero una pérdida promedio
porque ya no tenemos un único dato, sino
que tenemos una gran cantidad de datos y
lo que nos interesa es tener una
cantidad global, la pérdida promedio que
nos mida en promedio qué tan buenas son
las predicciones con respecto a esos
valores reales. Entonces calculamos esa
pérdida promedio que es esencialmente un
número y ese número se lleva a un
elemento central en este proceso de
entrenamiento donde ese elemento se
encarga de decirle al modelo, ajusta los
parámetros para que la pérdida se siga
reduciendo, es decir, mueve las perillas
en una cierta dirección para que esa
pérdida siga siendo cada vez más
pequeña. Ese elemento central del
proceso de entrenamiento se conoce como
el algoritmo de optimización y uno de
los algoritmos más usados es el
algoritmo del gradiente descendente, del
cual les hablo en un video que les dejo
por acá enlazado. Entonces ese algoritmo
de optimización le indica a la neurona
cómo debe mover las perillas para tratar
de reducir la pérdida. Entonces, esas
perillas se mueven ligeramente y en este
punto tenemos lo que se conoce como una
iteración de entrenamiento y la idea es
que esto se repita una y otra vez.
Entonces, en la segunda iteración de
entrenamiento, por ejemplo, tenemos los
mismos datos de entrenamiento, pero las
perillas ya están en posiciones
ligeramente diferentes a las que
teníamos inicialmente. Ya no son
totalmente aleatorias. Con esas perillas
en esa posición generamos una
predicción. Comparamos esa predicción
con los valores reales a través de la
pérdida promedio. Llevamos eso al
algoritmo de optimización que le dice al
modelo que ajuste los parámetros para
que la pérdida se siga reduciendo. Esos
parámetros se ajustan ligeramente, se
mueven ligeramente las perillas y ahí
completamos una segunda iteración de
entrenamiento. Si vamos a una tercera
iteración, usamos el mismo set de
entrenamiento, las perillas están en esa
posición ya un poco más cercana de ese
punto ideal que en la iteración
anterior. se generan predicciones, se
calcula la pérdida promedio, se lleva al
algoritmo de optimización que le indica
al modelo cómo ajustar los parámetros y
esta sería una tercera iteración. Y esto
se repite una cierta cantidad de veces.
Nosotros definimos cuántas iteraciones
de entrenamiento habrá y al final,
idealmente, tendremos las perillas, los
parámetros en sus posiciones ideales, de
manera tal que la pérdida será lo más
pequeña posible. Así que ya teniendo
claro cómo es este proceso de
entrenamiento, ya podemos definir lo que
es el aprendizaje. El aprendizaje
consiste en que mediante un algoritmo de
entrenamiento se encuentran de forma
automática los parámetros que minimizan
la pérdida. Entonces, acá es importante
resaltar que tenemos un algoritmo de
entrenamiento que le indica a las
perillas en qué dirección moverse para
seguir reduciendo la pérdida. Ese
movimiento de las perillas se da de
forma automática. Eso lo hace el
algoritmo por sí solo y la idea es que a
medida que avanzan las iteraciones, la
pérdida se vaya haciendo lo más pequeña
posible. En esto consiste el aprendizaje
de una neurona. Y entonces en este caso
decimos que la neurona aprende sus
parámetros a través del proceso de
entrenamiento. Y para resumir podemos
decir que en cada iteración de
entrenamiento primero lo que hacemos es
generar las predicciones. Esto se conoce
como propagación hacia delante. Tomamos
los datos de entrenamiento, llevamos los
datos al modelo, generamos la
predicción. En el segundo paso, teniendo
la predicción, se calcula la pérdida
promedio y en el tercer paso se
actualizan esos parámetros. Ese paso se
conoce como la propagación hacia atrás y
esa propagación hacia atrás permite
mover esas perillas en la dirección
adecuada y esto se repite una y otra vez
durante el proceso de entrenamiento. Y
en este punto, teniendo claro cómo es el
proceso de entrenamiento y aprendizaje
de una neurona, ya podemos llevar esas
mismas ideas a las redes neuronales. Acá
tenemos una red neuronal. ¿Qué es una
red neuronal? Pues básicamente una red
neuronal es el resultado de
interconectar múltiples neuronas
artificiales y entonces esa red neuronal
puede tener cientos, miles, cientos de
miles, millones o miles de millones de
parámetros, pero en esencia es la
interconexión de múltiples neuronas
artificiales. Y teniendo en cuenta que
una red neuronal nace de la conexión de
múltiples neuronas artificiales, pues
podemos entrenarla siguiendo la misma
lógica que usamos para una neurona
artificial. ¿Qué quiere decir esto? Que
en primer lugar tenemos que preparar el
set de entrenamiento con las
características de entrada, los valores
reales que queremos que la red neuronal
aprenda a predecir y en cada iteración
de entrenamiento que hacemos lo mismo
que hacíamos con la neurona artificial.
Es decir, en primer lugar se generan las
predicciones, hacemos propagación hacia
delante, tomamos las características, se
las presentamos a la red neuronal. Acá
la diferencia es que ya no tenemos
cuatro o cinco parámetros, sino que
tenemos cientos miles o miles de
millones incluso de parámetros, pero la
lógica va a ser la misma. Con esos
parámetros inicializados aleatoriamente
en la primera iteración se genera una
predicción. Esa predicción se compara
con el valor real para calcular la
pérdida promedio. Con esa pérdida
promedio que hemos calculado, en el paso
tres se actualizan los parámetros en la
propagación hacia atrás, es decir, se
mueven todas esas perillas de la red
neuronal y el procedimiento se repite
una y otra vez y al final del
entrenamiento, la red neuronal habrá
aprendido de forma automática los
parámetros que minimizan la pérdida. Es
decir, la lógica es la misma que el
proceso de entrenamiento de una neurona
artificial, con la diferencia de que acá
ya tenemos muchísimos más parámetros,
pero la idea básica va a ser exactamente
la misma. Muy bien, acabamos de ver qué
es y en qué consiste el proceso de
entrenamiento de una red neuronal y a
qué nos referimos específicamente con el
término aprendizaje. En esencia, este
entrenamiento se lleva a cabo de forma
iterativa siguiendo estos pasos. En
primer lugar, lo que hacemos es
inicializar los parámetros del modelo de
forma totalmente aleatoria, conformar un
set de entrenamiento y luego se repiten
una y otra vez los pasos de generar
predicciones, que se conoce como
propagación hacia delante, forward
propagation, calcular la pérdida, es
decir, la diferencia numérica que existe
entre las predicciones que genera el
modelo y los valores reales esperados a
la salida. Y luego esos datos se
retroalimentan al modelo a través del
algoritmo de optimización, lo cual
permite ajustar esos parámetros en cada
iteración y ese proceso se repite una y
otra vez por el número de iteraciones
que nosotros hayamos definido. Y lo
interesante de todo esto es que este
procedimiento paso a paso se puede
aplicar a un modelo tan simple como es
una neurona artificial o a modelos mucho
más complejos como las redes neuronales,
las redes convolucionales que se usan
para procesar imágenes, las redes LSM
que se usan para procesar secuencias e
incluso modelos gigantescos como los
grandes modelos de lenguaje basados en
las redes transformer. Y en últimas,
después de todo este proceso de
entrenamiento, lo que podemos decir es
que la red aprende los parámetros que le
permiten generar las mejores
predicciones posibles. A eso nos
referimos con ese proceso de
aprendizaje. Así que espero que con lo
que acabamos de ver en este video tenga
ya una idea mucho más clara de lo que
ocurre realmente cuando escuchamos
hablar de que un modelo ha sido
entrenado o de que ha llevado a cabo un
proceso de aprendizaje. Y si quieren
aprender todos estos conceptos de manera
mucho más rigurosa y de manera mucho más
aplicada, de forma práctica para
resolver diferentes tipos de problemas,
pues los invito a darle una mirada al
curso de fundamentos de Deep Learning
con Python que tengo en la Academia
online, donde vemos todos estos
elementos de forma mucho más detallada.
Y recuerden que si tienen alguna duda de
lo que acabamos de ver en este video,
pues me la pueden dejar abajo en los
comentarios. Así que por ahora esto es
todo. Les envío un saludo y nos vemos en
el próximo