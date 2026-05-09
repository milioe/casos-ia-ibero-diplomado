una de las cosas más importantes al
trabajar con redes neuronales son las
funciones de activación y aquí veremos
para qué sirven Cómo y cuándo
utilizarlas y no quiero nada más ver las
tres o cuatro principales sino entrar
más a detalle de las funciones e incluso
ver algunas que son relativamente nuevas
y que prometen dar mejores resultados
Comencemos viendo para qué sirven y para
eso es útil pensar en las redes norales
como aproximadores de funciones muchos
problemas que resolvemos constantemente
con nuestro propio cerebro podemos
verlos como funciones con entradas y
salidas Por ejemplo si está estamos
viendo un animal y Queremos saber qué
animal es podemos ver este problema como
una función la entrada a la función es
la imagen que estamos viendo y la salida
nos dice Qué animal es de igual manera
cuando escuchamos una canción la entrada
a la función es la onda Sonora y la
salida nos dice qué canción Estamos
escuchando las redes neuronales no
trabajan con dos o tres dimensiones sino
con muchas Entonces es difícil
graficarlas sin embargo para fines
ilustrativos imaginemos que podemos
graficarlas en tres dimensiones digamos
por ejemplo que la función que usa
nuestro cerebro para identificar
animales es esta y la función que
utiliza para identificar canciones es
esta otra cuando nosotros creamos una
nueva red neuronal comienza inicializada
totalmente Ya sea en ceros o de manera
aleatoria durante el proceso de
entrenamiento ajustamos poco a poco los
parámetros de la red para aproximar lo
más posible a la función que queremos y
después poder hacer predicciones
precisas a esto nos referimos con
aproximador de funciones a algo que
podemos ajustar poco a poco hasta
adaptarse lo más posible a la función
que queremos una red neuronal sin
funciones de activación es muy limitada
recordemos que cada neurona de la red
recibe una suma ponderada de sus
entradas le suma un número llamado sesgo
y da el resultado a las siguientes capas
y esto se hace para cada neurona de la
red sin embargo esta operación es lineal
que si graficamos sería una línea para
dos dimensiones un plano para tres
dimensiones un hiperplano etcétera y no
importa Cuántas capas o Cuántas neuronas
agreguemos a la red la unión de todas
estas operaciones lineales tiene también
una salida lineal por lo que es lo mismo
que tener una sola capa los problemas
del mundo real son mucho más complejos
que una simple función lineal por lo que
una red así no podría aprender nada
interesante esto lo vimos en los
primeros dos videos de la lista de
reproducción en donde aprendemos
Inteligencia artificial desde cero si no
lo has visto te dejo por aquí la lista
de reproducción las funciones de
activación nos ayudan a salir de esa
cárcel lineal hacen muchas cosas pero su
trabajo principal es agregar componentes
no lineales a la red cada neurona además
de obtener una suma ponderada y agregar
un sesgo pasará el resultado por una
función que llamamos función de
activación y solo entonces dará el
resultado a las siguientes capas por
ejemplo aquí podemos ver una neurona sin
función de activación si cambiamos los
valores de la entrada la salida cambia
de manera constante por lo que forma una
línea pero si agregamos una función de
activación por ejemplo esta llamada
función logística y el resultado lo
pasamos por dicha función antes de darlo
a las siguientes capas podemos ver que
al cambiar los valores de la entrada la
salida ya no cambia de manera constante
formando una línea la forma en la que la
salida cambia según las entradas depende
de qué función de activación estamos
utilizando con este simple cambio de
agregar una función para que la salida
de cada neurona ya no sea lineal una red
neuronal con suf entes capas y neuronas
y suficiente entrenamiento podrá
ajustarse a funciones mucho más
complejas como entender imágenes sonido
texto etcétera otra forma de verlo es
con esta cobaya hace mucho frío y quiero
taparla con una red neuronal pero sin
funciones de activación solo puedo
taparla con esto es lineal por lo que no
puede tener dobleces ni curvas es un
simple plano y la cobaya se queda con
frío con las funciones de activación la
red ya no está limitada a un plano o
hiper mano y conforme agregamos capas y
neuronas nuestra red podrá crear
pliegues y dobleces cada vez más
precisos hasta adaptarse mejor a la
cobaya quizá Incluso logremos un ajuste
perfecto de igual manera nuestras redes
con suficientes capas y funciones de
activación pueden adaptarse a los
distintos problemas para los que las
usamos actualmente las funciones de
activación han estado en constante
investigación desde hace décadas y se
han ido descubriendo cada vez más y
mejores veamos algunas y veamos algunos
beneficios y problemas que tienen si
hablo de algún concepto que no conoces O
quieres que me meta más a detalle de
algo por favor déjame un comentario y si
el video te está gustando O al menos
crees que bobaya se lo ganó por favor
Regálame un me gusta Comencemos con lo
más simple la función de escalón o Step
function esta función regresa cero para
todos los valores negativos y cero o uno
para todos los positivos nos da el
componente no lineal que queremos sin
embargo no es apta para el aprendizaje
automático actual Por qué cuando creamos
una red neuronal necesitamos primero
entrenarla antes de poder hacer
predicciones durante el entrenamiento le
damos ejemplos que pasan por todas las
capas de la red una por una hacia
delante realizando las operaciones de
las neuronas y nos da un resultado al
final Después de varios ejemplos usamos
la función de costo para ver qué tan
bien o mal estuvo la red en sus
predicciones según qué tan mal le fue
ahora queremos ajustar los parámetros de
la red para mejorar los pesos y sesgos y
para saber Cómo ajustar los pesos y
sesgos calculamos la derivada o
gradiente de la función de costo
respecto a cada uno de los pesos y
sesgos de la red y lo hacemos capa por
capa hacia atrás una por una hasta
llegar al inicio este proceso es llamado
propagación hacia atrás o Back
propagation aquí Lo importante es que
usamos derivadas y necesitamos poder
calcular la derivada de las funciones de
activación que estamos usando en nuestra
red la función de escalón aquí tiene un
problema para la mayoría de sus valores
la derivada es cero y en el valor de
cero no no tiene derivada si te
confunden las derivadas piensa en la
derivada como la inclinación de la
función esta función no tiene
inclinación tiene solo líneas
horizontales si comparo la diferencia
entre x1 y x2 en ambos el valor de y es
1 es decir que no hay diferencia no hay
inclinación y por lo tanto la derivada
es cer0 lo mismo pasa para X3 x4 X5
etcétera para poder tener derivada
necesitamos una función que tenga
variación que no sea una línea
horizontal como esta otra forma de
decirlo es que necesitamos que las
funciones de activación que vamos a usar
sean diferenciables Por cierto si
quieres una introducción simple a las
derivadas te dejo este video en donde
las derivadas me dejan caer un huevo en
la cabeza pasemos ahora a las funciones
de activación sigmoides es decir que
tienen forma de s la primera es la
función logística que de hecho cuando
alguien habla de la función sigmoide o
sigmoide en redes neuronales Normalmente
se refiere a ella esta función similar
la función de escalón acota los
resultados entre 0 y 1 sin embargo esta
tiene una curva suave esta función sí es
diferenciable si medimos su valor en x1
y x2 hay una variación en el valor de la
y por lo cual sí podemos calcular una
derivada diferente a cer0 la fórmula de
la función logística es esta si no sabes
qué es esa e es una constante matemática
llamada el número de Euler que se
pronuncia eiler y su valor Es
aproximadamente dos pun
7182 este número lo veremos en todos
lados entonces si te interesa que hable
de dónde salió este número por favor
déjame un comentario para hacer un video
al respecto cualquier entrada que le
demos a esta función no importa qué tan
grande pequeña o negativa sea siempre
nos va a dar un resultado entre C y uno
hace algunos años era común utilizar
esta función en todas las capas ocultas
de la red sin embargo esta función tiene
algunos inconvenientes uno de los
principales es el desvanecimiento de
gradiente Si vemos nuestra función la
inclinación o derivada es bastante buena
en valores cercanos al cero sin embargo
si le damos entradas muy grandes o muy
pequeñas la Gráfica se hace casi
horizontal es decir la derivada se hace
muy muy pequeña en la propagación hacia
atrás conforme vamos pasando por las
capas si tenemos derivadas así de
pequeñas los ajustes a los pesos y
sesgos de la red se hará con cambios muy
pequeños por lo que la red aprenderá muy
despacio o simplemente dejará de
aprender en las primeras capas por eso
se dice que desvanece la gradiente es
decir la derivada se vuelve un valor muy
pequeño conforme avanzamos en el proceso
de propagación hacia atrás sin embargo
esta función sigue siendo muy utilizada
si tu red debe dar como salida una
probabilidad binaria esta función es
perfecta Por ejemplo si quieres saber si
una imagen tiene un perro o un gato o si
una imagen tiene un producto bueno o
defectuoso la capa de salida de tu red
puede tener una sola neurona con esta
función de activación asegurando Así que
la salida será entre cero y uno y
podemos considerar que cero es perro y
uno es gato o que cero es producto bueno
y uno es producto defectuoso ahora
veamos nuestra siguiente función la
tangente hiperbólica esta función es muy
similar a la logística sin embargo está
acotada a valores desde -1 hasta 1 la
función para calcularla es
esta en casi todo los casos esta función
es superior a la función logística para
empezar su derivada es mayor si
graficamos la derivada de la función
logística es esta pero si graficamos la
de la tangente hiperbólica es esta son
similares pero al tener una derivada
mayor el aprendizaje será más rápido con
eso creo que ya puedes hacerte la idea
de que buscamos que las funciones de
activación que estamos usando tengan
unas derivadas suficientemente grandes
para que los ajustes a la red sean
sustanciales por lo tanto la red aprenda
más rápido otro beneficio de esta
función es que está centrada en el cero
en la función logística siempre la
salida que nos da es positiva entre C y
uno esto genera un problema en la
propagación hacia atrás conforme vamos
actualizando los pesos y sesgos capa por
capa usar esta función limita las
actualizaciones que hacemos en cada capa
a que sean positivas o negativas y no
permite mezclar y esto limita mucho la
velocidad a la que puede aprender la red
como la tangente hiperbólica puede tener
valores positivos y negativos soluciona
este inconveniente por lo tanto para la
mayoría de los los casos está comprobado
que esta función es mucho mejor que la
anterior la función logística sigue
siendo buena idea en la neurona de
salida para resultados binarios sin
embargo la tangente hiperbólica tiene
problemas similares solo con ver la
Gráfica puedes imaginar que también
tiene el problema de desvanecimiento de
gradiente además son algo caras de
calcular ambas realizan exponenciacion
durante el cálculo entre las capas lo
cual tiene un alto costo computacional
hay varias otras funciones sigmoides que
podríamos ver como soft Sign que tiene
una mejor rente pero su derivada es más
compleja y comparte algunos
inconvenientes pero pasemos ahora a una
de las funciones más importantes y
contra las que todas se comparan
actualmente relo abreviación para
rectified linear unit o unidad lineal
rectificada podemos remontar el uso de
relo hace varias décadas pero fue hasta
2011 donde se comprobó que era mucho
mejor en la mayoría de los casos que la
mayoría de las funciones de activación
que se utilizaban en el momento y que la
propagación hacia adelante y hacia atrás
era hasta seis veces más rápido que la
tangente hiperbólica fue utilizada en
2012 para la Revolucionaria alexnet y en
2015 para resnet en 2018 fue considerada
la más utilizada y es todavía usada por
defecto hoy en día Qué tiene de especial
relu que le ganó a las otras funciones
veamos la
función como puedes ver Es excesivamente
simple no hay exponentes ni cálculos
complicados regresa lo que sea mayor 0 o
x si el número es menor a cer el
resultado será cer y si es mayor cero el
resultado es el mismo número de la
entrada eso genera esta gráfica la
función tiene un costo computacional muy
bajo y su derivada también es muy simple
cer0 para todos los números negativos y
uno para todos los positivos si me voy
muy a detalle la derivada en cer no
existe Pero es tan raro que tengas un
0.000 que se puede ignorar y usar ya sea
0 o uno esta función A diferencia de las
anteriores no está acotada las
anteriores solo podían dar resultados
entre cero y uno o entre os1 y uno relo
no está acotada para números positivos
lo cual da una gradiente constante y
genera una aprendizaje mucho más rápido
gracias a esto ha permitido entrenar de
manera eficiente redes cada vez más
profundas si bien relus la función base
que actualmente se utiliza también tiene
sus inconvenientes principalmente debido
a que relu regresa a cero para todos los
números negativos puede generar las
llamadas neuronas muertas las cuales
durante el entrenamiento comienzan
solamente a dar un valor de cero
entorpeciendo el aprendizaje sobre todo
si tenemos una tasa de aprendizaje muy
grande con lo cual es fácil que caigamos
en números negativos pasando las
neuronas de relu a cero y que ya no se
puedan recuperar debido a esto y otros
inconvenientes investigadores han estado
buscando incansablemente mejores
funciones de activación que no solo
arreglen el problema sino que tengan un
bajo costo computacional hablaré ahora
de ella sin embargo hoy en día relu
sigue siendo la función por defecto que
se utiliza en capas ocultas Y
seguramente la vas a usar en tus redes
ya después Si gustas puedes Probar con
otras para hacer comparaciones pasemos
ahora a otras funciones que se han
propuesto para mejorar arru liky relu O
lru la cual es muy similar pero en lugar
de dar cero para números negativos
multiplica el valor por un número muy
pequeño 0.01 generando una gráfica como
esta de esta manera ahora tenemos una
función no acotada simple de calcular y
evita las neuronas muertas sin embargo
como la derivada de números negativos es
muy pequeña es propensa al
desvanecimiento de gradiente Por lo cual
también se ha propuesto peru parametric
relu o relu parametrizable es
prácticamente lo mismo pero en lugar de
0.01 se utiliza un parámetro que puede
ajustarse También tenemos a gelu la cual
es muy similar sin embargo es más suave
y tiene una característica muy peculiar
e importante no es monotónica las
funciones que hemos visto hasta el
momento son monotónica en este caso
incrementan constantemente y pasan una
sola vez por el cero una función no
monotónica puede subir y después bajar
puede incluso pasar dos o más veces por
el cero y más adelante veremos algunas
funciones que quieren utilizar esta
propiedad para hacer que las neuronas
artificiales sean tan eficientes como
las cerebrales pero regresando a gelo
tiene esta pequeña curva es similar a
relo y es usada por bert gpt y otros
Transformers soft Plus es una versión
suave de relu de hecho un dato interes
an Es que su derivada es la función
logística en general no es muy usada si
bien puede dar mejores resultados que
relu es más cara computacionalmente Ian
goodfellow quien inventó las redes gun
trabajó para Google Brain y fue director
de Machine learning de Apple y de hecho
ahorita están las noticias porque
renunció cuando quisieron hacerlo
regresar a trabajar a la oficina dice
que Aunque parezca que tiene beneficios
sobre relu ya en la práctica los
beneficios realmente no son muy
tangibles sin embargo como todo te
invito a probarlo por ti mismo hay otras
funciones por ejemplo Max out el cual
tiene un poco mejores resultados pero Su
costo computacional es mucho más elevado
elu entre muchos otros que quizá mejoran
algunas cosas pero también tienen otros
inconvenientes y esto nos lleva a
funciones de activación propuestas más
recientemente Comencemos por switch esta
función de hecho fue obtenida por medio
de un proceso de aprendizaje por
refuerzo en una publicación de 2017 en
casi todas las tareas y pruebas es mejor
arrgo según palabras de Google sin
embargo Su costo computación es un poco
más alto la función es esta en donde
Beta es un parámetro modificable cuando
el parámetro se pone en uno es decir que
no se usa se llama esta función switch 1
su gráfica es suave no es monotónica y
es un buen candidato para reemplazar ar
relu curiosamente la función switch 1 ya
había aparecido en una publicación de
hecho en la publicación cuando se
propuso gelu pero bajo otro nombre silu
sin embargo switch puede tener otros
valores como Beta no solo uno ahora
veamos Mich propuesto en 2020 no es
monotónica y mejora los resultados de
relu swish en muchas tareas sobre todo
en visión computacional creo que puedes
ver que la mayoría de las mejoras
actualmente se están haciendo con
funciones no monotónica su función es
esta mantiene un poco de información
negativa evitando la muerte de neuronas
al igual que switch Su costo
computacional es un poco más elevado que
el de relu
ahora veamos otras funciones de
activación que usamos constantemente
aprovecho un momento para agradecer a
quienes me apoyan en patreon y en
YouTube ya que este video está aquí
gracias a ustedes si te gustaría también
apoyar al Canal te dejo la información
en la descripción del video Nuevamente
gracias veamos rápido la función de
identidad Esta es básicamente cuando no
se usa una función de activación y es
Útil para las redes de regresión que
deben dar como salida un número similar
a como hice en el video para transformar
grados celsus Fahrenheit O quizá una red
que calcula el precio de una casa
después está softmax esta función fue
descrita de alguna manera desde hace más
de un siglo pero se usa en aprendizaje
automático desde hace aproximadamente 30
años la usamos para redes de
clasificación por ejemplo para
clasificar qué número aparece en una
imagen o si se trata de una cuchara
tenedor o cuchillo similar a como lo
hice en videos anteriores básicamente si
tienes varias opciones y quieres que la
red nos dé una clasificación sofma
permite que la capa nos nos de una serie
de probabilidades y la suma de todas
esas probabilidades nos dará uno por
ejemplo si la entrada es este c escrito
y la capa de salida tiene neuronas para
que nos diga qué número es del 0 al nu
entonces Esperamos que la neurona que
representa el cinco tenga un valor mayor
algo que me han preguntado
frecuentemente con softmax es porque no
solamente tomamos una suma de todos los
valores y luego dividimos todos los
valores entre la suma veamos A qué nos
referimos imagina que tenemos cuatro
neuronas de salida y los resultados que
tenemos son
8.4 3 y
1.5 una forma de saber cuál es la
neurona ganadora sería obtener la suma
de todos 12.9 y dividir cada uno entre
la suma lo cual nos da estos valores
6203 pun 23 y pun 11 en general funciona
bien podemos ver que la primer neurona
con valor de 8o es la que mayor
porcentaje tiene y podemos elegirla como
ganador sin embargo softmax va más allá
y utiliza la función exponencial en cada
valor veamos cómo funciona consideremos
los mismos valores 8.43 y 1.5 ahora por
cada uno obtenemos su exponente natural
otra vez con el número de oiler lo cual
nos da estos valores
2980.5
1.49 20.08 y 4.48 ahora sí lo sumamos y
dividimos cada uno entre la suma que es
3007 y el resultado son estos valor
valores
99149 pun 0066 y 0014 como puedes ver
esta operación separa mucho los números
grandes de los pequeños ahora la primer
neurona nos da un
99% de probabilidad en lugar del 62 por
de antes muy bien Cuándo debes usar cada
función depende de algunas cosas la
función logística o sigmoid se
recomienda solamente en la capa de
salida cuando requerimos un resultado
binario cero o uno perro o gato calvo o
con pelo la tangente hiperbólica o tan
es superior a la función logística para
capas ocultas sin embargo en muy pocos
casos da resultados superiores a relo
por ejemplo en redes muy simples de
regresión relu es la que normalmente vas
a utilizar A menos que quieras
experimentar mucho con otras funciones
si te topas mucho con problemas como las
neuronas muertas puedes probar
disminuyendo la tasa de aprendizaje o
explorando con otras funciones el rel y
p relu puedes explorarlas si batallas
mucho con las neuronas muertas de relu
Sin embargo estas pueden caer un poco en
el problema de desvanecimiento de
gradiente gelu Aunque tiene tiempo que
se propuso y es utilizada en redes
famosas como gpt y otros Transformers
aún en muchas publicaciones es
considerada como relativamente nueva de
manera general tiene mejores resultados
que relu especialmente en redes muy
grandes o Transformers puedes
experimentar con ella y comparar los
resultados contra relu switch Funciona
muy bien y en general vence arru Solo
que Su costo computacional es un poco
más alto Mich en tareas de visión
computacional ha dado mejores resultados
incluso que switch y de hecho se utilizó
en Yolo 4 pero en Yolo 5 fue reemplazado
por el relu y
sigmoid utiliza softmax en la última
capa de tus redes de clasificación la
función de identidad lineal o no
utilizar una función de activación
puedes hacerlo en tus redes cuando son
de regresión ahora hay otras funciones
de activación llamadas oscilatorias las
cuales pueden resolver el famoso
problema del or exclusivo con una sola
neurona algo que antes se consideraba
imposible de hacer estas funciones
prometen permitir redes más eficientes
con menos neuronas Y quizá puedan cerrar
la brecha entre las neuronas
artificiales y las cerebrales estas
funciones al día de hoy todavía se
consideran un poco experimentales
entonces veremos a detalle Cómo
funcionan en un siguiente video hasta
entonces