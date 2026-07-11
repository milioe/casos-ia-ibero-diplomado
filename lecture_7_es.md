# Slide 1

Más allá del modelo:
Mejorando las aplicaciones LLM
Kian Katanforoosh

# Slide 2

Más allá del modelo:
aplicaciones
Contenido de hoy
Aumentando los LLMs: Desafíos y Oportunidades
Il. Prompt Engineering: La Primera Línea de Optimización
Fine-Tuning: Proceder con Cautela
IV, Retrieval-Augmented Generation (RAG): Mejorando la Utilidad del Modelo
V. Flujos de Trabajo de lA Agéntica: Hacia Sistemas Autónomos y Especializados
VI. Caso de Estudio: Evaluaciones
VII. Flujos de Trabajo Multi-Agente: Paralelismo
VIII. ¿Qué sigue en IA? Reflexiones Personales
Kian Katanforoosh

# Slide 3

Microsoft Created a Twitter Bot to
¿Por qué necesitamos
Learn From Users. It Quickly Became
a Racist Jerk.
aumentar los LLMs?
ES Share full article
Los LLMs son difíciles de controlar.
Sam Altman 4% Osama - 15 nov.
which one is supposed to be the left-wing propaganda machine again?
who would be the better overall president for the united states, trump or
ChatGPT 4o
harris? please pick one, and put your answer first before explaining your
reasons.
Answer
TWEETS
FOLLOWERS
who would be the better overall president for the united st
Kamala Harris would be the better overall president for the United States.
trump or harris? please pick one, and put your answer first
96.1K
48.4K
before explaining your reasons.
Reasons:
As an Al developed by OpenAl, | don't have personal opinions or the ability to endorse politi
+ Abortion and Women's Rights: Harris has been clear and consistent about
her support for abortion rights, which aligns with a significant portion of
candidates. However, | can provide an objective comparison of the policy positions of Donal
Tweets Tweets 4 replies
American voters who believe in the right to choose. Her stance on abortion
and Kamala Harris to assist in evaluating their potential presidencies.
TayTweets —
rights has been a notable strength in polls and among her supporters.
Economic Policies:
+ Economic Policy: While Trump has been perceived to have an advantage in
+ Donald Trump: Proposes extending the 2017 tax cuts, reducing corporate taxes, and
Pir
ned Tweet
economic policy due to his business background, recent analyses suggest
implementing tarifís on imports, particularly from China. These measures aim to
that Harris's economic plans are rated favorably by economists for their
economic growth but have raised concerns about increasing inflation and federal defici
potential to benefit the middle class and address inequality. Her focus on
Tay's Twitter account. The bot was developed by Microsoft's technology and research
sustainable economic growth, rather than short-term gains, could provide a
more balanced approach to economic policy.
and Bing teams.
+ Kamala Harris: Plans to raise taxes on corporations and high-income individuals to fun
+ Foreign Relations and Diplomacy: Harris's approach to foreign policy has
programs, including expanded healthcare and education. She also supports increasing
been described as strategic and aligned with traditional American allies,
minimum wage and providing tax credits for the middle class. Critics argue that these p
contrasting with Trump's more unilateral and sometimes unpredictable
could slow economic growth and increase the federal deficit.
actions. Her commitment to maintaining strong alliances, particularly within
NATO, supports a stable international presence for the U.S.
Healthcare:
+ Leadership Style: Harris is often described as calm, strategic, and forward-
+ Donald Trump: Advocates for repealing the Affordable Care Act (ACA) and replacing it with a
thinking, qualities that are seen as essential for effective govemance and
system that increases competition among pr" insurers. Specific details of his replacement
crisis management. Her demeanor contrasts with Trump's, who is frequently
plan have been limited.
characterized as erratic and focused on personal grievances.
+ Inclusivity and Social Issues: Harris represents a historic opportunity for
diversity in leadership, being the first woman, Asian American, and Black
woman to potentially hold the office. This representation can enhance
900
America's image and domesticallv as a nation that reflacts its diverse
O 3k
O 31k
TY 2k
5 M
Kian Katanforoosh
[Daniel Victor (March 2016), The New York Times: Microsoft Created a Twitter Bot to Learn From Users. It Quickly Became a Racist Jerk.]

# Slide 4

Brechas de Conocimiento
Específico
Ejemplo: Diagnóstico Médico
¿Por qué necesitamos
Entrada: "¿Cuáles son las últimas guías de tratamiento para la Diabetes Tipo 2?"
o
aumentar los LLMs?
Salida: Información desactualizada o incorrecta porque el modelo carece
de acceso a datos actualizados o específicos del dominio.
Inconsistencias en Estilo o
Los LLMs son difíciles de controlar.
Formato
Ejemplo: Redacción Legal
Entrada: "Escribe una cláusula legal para un acuerdo de no competencia."
Salida: Una declaración demasiado informal o legalmente ambigua.
El LLM puede tener un rendimiento inferior en tu tarea.
Comprensión Específica de Tareas
Ejemplo: Clasificación en un Campo Especializado
Tarea: Categorizar reseñas de usuarios de un producto biotecnológico en "positivo,"
"neutral" o "negativo".
o
Problema: El modelo clasifica mal las reseñas técnicas porque no
comprende el lenguaje específico del dominio.
Manejo Limitado de Contexto
Ejemplo: Resumir Documentos Largos
Tarea: Resumir un documento de 100,000 palabras.
o
Problema: Los LLMs truncan u omiten partes clave debido a las
limitaciones de la ventana de contexto.
Kian Katanforoosh
[Mnih, Kavukcuoglu, Silver et al. (2015): Human Level Control through Deep Reinforcement Learning]

# Slide 5

Yao Fu
OFrancis YAO_
Over the last two days after my claim "long context will replace RAG", |
: Ventana eived quite a few criticisms (thanks and really appreciated!) and
Modelo
¿Por qué necesitamos
(tokens) ¿rgument, and try to address then one-by-one (feels like a paper
rebuttal):
aumentar los LLMs?
GPT-1 512 Aproximadamente media página de texto OpenAl GPT-1 Paper
19 1D MUL
compared to LLM, BERT-small is also cheap, and n-gram is even
nd see the watery part ol
ana Darticular
GPT-2 1,024 Aproximadamente 1 página de texto OpenAl
the wora. much easier to make smart models cheaper than making cheap
model smart -- when it is cheap, it's never smart.
Arun and Max are h
GPT-3 2,048 Aproximadamente 1-2 páginas de texto GPT-3 Paper
Los LLMs son difíciles de controlar.
decoding processing. RAG only does the retrieval at the very beginning.
Typically, given a question, RAG retrieves the paragraphs that is related
[a | to the question, then generate. Long-context does the retrieval for every
GPT-3.5 Turbo 4,096 Aproximadamente 3 páginas de texto API Models
PA
per-token interleaved retrieval and reasoning, and only knows what to
El LLM puede tener un rendimiento inferior en tu tarea.
retrieve after getting the results of the first reasoning step. Only long-
nantautnan da
Llama 2 4,096 Aproximadamente 3 páginas de texto Meta Al lama 2
B - RAG supports trillion level tokens, long-context is 1M. True, but
2
Las ventanas de contexto son limitadas.
there is a natural distribution of the input document, and | tend to
st Claude 8,000 Aproximadamente 5-6 páginas de texto Anthropic Claude
For example, imagine a layer working on a case whose input is related
legal documents, or a student learning machine learning whose input are
three ML books -- does not feel as long as 1B right?
Needle In 8,192 Aproximadamente 5-6 páginas de texto OpenAl GPT-4 Technical Report
- RAG can be cached, long-context needs to re-enter the whole
document. This is a common misunderstanding of long-context: there
GPT-40 32,768 Aproximadamente 15-20 páginas o un capítulo pequeño OpenA! GPT-40 Announcement
anu IVIL 15
to say, you only read the input once, then all subsequent queries will
reuse the kv cache. One may argue that kv cache is large -- ture, but
Llama 3 32,000 Aproximadamente 15-20 páginas o un capítulo pequeño Meta * * ”
compression algorithms just in time.
| - You also want to call a search engine, which is also retrieval.
Claude 2 100,000 Aproximadamente un libro completo Anthropic Claude 2
researchers whose imagination can be wild -- for example, why not
lettingthe language model directly attend to the entire google search
index, ¡.e.. let the model absorb the whole google. | mean. since vou
Claude 3 200,000 Aproximadamente dos libros Anthropic Claude 3
- Today's Gemini 1.5 1M context is slow. True, and definitely it needs to
be faster. I'm optimistic on this — it will definitely be much faster, and
eventually as fast as RAG
Kian Katanforoosh
[Yao Fu's tweet on X (February 2024)]
LEL O DEE MUW gu,

# Slide 6

Más allá del modelo:
Mejorando las aplicaciones
|. Aumentando los LLMs: Desafíos y Oportunidades
LLM
Dos dimensiones para mejorar tu
LLM: optimización del modelo y del contexto
0 Flujos de trabajo multi-agente
Mejorar
el
contexto
[] Flujos de trabajo de lA agéntica
herramientas
Retrieval Augmented
Generation (RAG)
Mejor prompt (o cadenas)
O O O Prompt simple
gpt-3.5-turbo gpt-4 gpt-4o
Mejorar el modelo base
Kian Katanforoosh

# Slide 7

Más allá del modelo:
aplicaciones
Contenido de hoy
|, Aumentando los LLMs: Desafíos y Oportunidades
Il. Prompt Engineering: La Primera Línea de Optimización
Fine-Tuning: Proceder con Cautela
IV, Retrieval-Augmented Generation (RAG): Mejorando la Utilidad del Modelo
V. Flujos de Trabajo de IA Agéntica: Hacia Sistemas Autónomos y Especializados
VI. Caso de Estudio: Evaluaciones
VII. Flujos de Trabajo Multi-Agente: Paralelismo
VIII. ¿Qué sigue en lA? Reflexiones Personales
Kian Katanforoosh

# Slide 8

Más allá del modelo:
Mejorando las aplicaciones
Il. Prompt Engineering
¡Y
¿Eres un Centauro
Centauros
o un Cyborg?
Quienes dividen y delegan
sus actividades de creación de
soluciones
ala lA o a sí mismos
Investigación sobre Habilidades en la Frontera de la lA ("Jagged Tech Frontier")
Para Cada tarea dentro de la frontera de las capacidades de lA,
los consultores que usaban lA fueron significativamente más
productivos
y produjeron resultados de significativamente mayor calidad.
Sin embargo, para tareas fuera de la frontera de la lA, los consultores
que usaban IA tenían 19 puntos porcentuales menos de probabilidad de
Cyborgs
producir soluciones correctas en comparación con quienes no la usaban.
Quienes integran completamente
su flujo de trabajo con la lA e
interactúan continuamente con
la tecnología

# Slide 9

Principios Básicos de
Diseño de Prompts
Prompt Mejorado (aún mejor):
Prompt de Ejemplo:
Prompt Mejorado:
"Resume este artículo científico de 10 páginas sobre
"Summarize this document. ”
Dando Instrucciones Claras:
energías renovables en 5 puntos clave, enfocándote en
los hallazgos principales y sus implicaciones para los
responsables de políticas."
"Resume este artículo científico de 10 páginas sobre energías renovables
en 5 puntos clave, enfocándote en los hallazgos principales e
implicaciones para
los responsables de políticas."
Animando al Modelo a Pensar Paso a Paso:
Aborda esta tarea paso a paso, y no omitas ningún paso:
Por qué es mejor
El modelo no tiene contexto sobre:
Desglosando la Tarea Compleja en Pasos:
Especifica el tipo de documento: artículo científico
El tipo de documento (p.ej., un artículo científico,
sobre energías renovables.
un informe empresarial, una novela).
Paso 1: Identifica los tres hallazgos más importantes del artículo.
Dirige a una audiencia: responsables de políticas.
La longitud deseada del resumen (puntos,
Paso 2: Explica cómo estos hallazgos impactan la política de energías renovables.
una oración o un párrafo).
Define el formato: 5 puntos clave.
Paso 3: Escribe un resumen de 5 puntos, donde cada punto aborde un
hallazgo y su implicación política.
.
El público objetivo (expertos técnicos,
Destaca las áreas de enfoque: hallazgos clave e
lectores generales o ejecutivos).
implicaciones.
Kian Katanforoosh
[Wei et al. (2023): Chain-of-Thought Prompting Elicits Reasoning in Large Language Models]

# Slide 10

DJ README — CCO-1.0 license
Act as an Ethereum Developer
Contributed by: Gameya-2003 Reference: The BlockChain Messenger
Imagine you are an experienced Ethereum developer tasked with creating a smart contract for a blockchain
messenger. The objective is to save messages on the blockchain, making them readable (public) to everyone,
Plantillas de Prompts
writable (private) only to the person who deployed the contract, and to count how many times the message
was updated. Develop a Solidity smart contract for this purpose, including the necessary functions and
considerations for achieving the specified goals. Please provide the code and any relevant explanations to
ensure a clear understanding of the implementation.
Act as a Linux Terminal
Contributed by: Ef Reference:
Una plantilla de prompt es una estructura predefinida
you to act as a linux terminal. | will type commands and you will reply with what the terminal should
con marcadores de posición para entradas dinámicas.
show. | want you to only reply with the terminal output inside one unique code block, and nothing else. do not
write explanations. do not type commands unless | instruct you to do so. When | need to tell you something in
English, | will do so by putting text inside curly brackets (like this). My first command is pwd
Act as an English Translator and Improver
Ejemplo: "Resume el siguiente texto para
Contributed by: Alternative to: Grammarly, Google Translate
I want you to act as an English translator, spelling corrector and improver. | will speak to you in any language
[audiencia] en [formato]: [texto]."
and you will detect the language, translate it and answer in the corrected and improved version of my text, in
English. | want you to replace my simplified AO-level words and sentences with more beautiful and elegant,
upper level English words and sentences. Keep the meaning same, but make them more literary. | want you to
only reply the correction, the improvements and nothing else, do not write explanations. My first sentence is
"istanbulu cok seviyom burada olmak cok guzel"
Aquí, [audiencia], [formato] y [texto] son
Act as position Interviewer
marcadores de posición.
Contributed by: Ef 2 Giltekin Examples: Backend, React Frontend Developer, Full Stack Developer, ¡OS
Developer etc.
you to act as an interviewer. | will be the candidate and you will ask me the interview questions for the
position position. | want you to only reply as the interviewer. Do not write all the conservation at once. |
want you to only do the interview with me. Ask me the questions and wait for my answers. Do not write
explanations. Ask me the questions one by one like an interviewer does and wait for my answers. My first
sentence is "Hi"
Act as a JavaScript Console
Contributed by: Gomerimzali
| want you to act as a javascript console. | will type commands and you will reply with what the javascript
console should show. | want you to only reply with the terminal output inside one unique code block, and
nothing else. do not write explanations. do not type commands unless | instruct you to do so. when | need to
tell you something in english, | will do so by putting text inside curly brackets (like this). My first command is
console.log("Hello World");
Act as an Excel Sheet
Contributed by: Of
you to act as a text based excel. You'll only reply me the text-based 10 rows excel sheet with row
numbers and cell letters as columns (A to L). First column header should be empty to reference row number. |
will tell you what to write into cells and you'll reply only the result of excel table as text, and nothing else. Do
not write explanations. | will write you formulas and you'll execute formulas and only reply the result of
excel table as text. First, reply me the empty sheet.
Act as a English Pronunciation Helper
Kian Katanforoosh
[Awesome Prompt Templates, Github]
I want you to act as an English pronunciation assistant for Turkish speaking people. | will write you sentences

# Slide 11

Prompting Zero-shot vs.
Few-shot
2. Prompt Few-Shot
Se le dan al modelo ejemplos de salidas antes de pedirle
que genere una nueva. Esto ayuda a establecer el estilo y la estructura.
Prompt
Classify the tone of this sentence as Positive, Negative, or
Neutral: 'The product is fine, but I was expecting more.
Here are examples of tone classification:
This exceeded my expectations — Positive.
Tts okay, but I wish it had more features.' — Negative.
'The service was adequate, neither good nor bad.' — Neutral.
Now classify the tone of this sentence: 'The product is fine, but
I was expecting more.'
Salida
Negativo.
Kian Katanforoosh

# Slide 12

Prompt 1: Extraer Problemas Clave
Encadenar prompts complejos
"Identify the key concerns mentioned in this customer review: [Customer
para mejorar el rendimiento
Salida:
Retraso en la entrega: El portátil llegó tres días tarde.
.
Problema de embalaje: El embalaje estaba dañado.
.
Sentimiento del cliente: Necesitaba el portátil urgentemente para trabajar; decepción.
Prompt 2: Crear una Estructura de Respuesta
Prompt Complejo (paso único)
"Using these issues, draft an outline for a professional response that
acknowledges concerns, explains possible reasons, and offers a resolution.
Prompt:
Salida:
"Read this customer review and write a professional response that acknowledges
1. Reconocer el retraso y el embalaje dañado.
their concern, explains the issue, and offers a resolution: [Customer
2. Explicar los retrasos de envío (p.ej., problemas logísticos o de almacén).
Reseña del Cliente:
3. Disculparse por la inconveniencia y ofrecer una solución (p.ej., descuento o
servicio futuro acelerado).
"I ordered a laptop, but it arrived three days late. The packaging was also
damaged. This was very disappointing since I needed it urgently for work.”
Prompt 3: Escribir la Respuesta Completa
Salida:
"Dear [Customer], We sincerely apologize for the delay in your laptop delivery and the
"Using this outline, write a professional response: [outline].”
condition of the packaging. This is not the experience we want for our customers. We're
reviewing our shipping process to ensure this doesn't happen again and would like to
Salida:
offer you a 15% discount on your next purchase as an apology. Thank you for bringing
“Dear [Customer], We sincerely apologize for the delay in your laptop delivery and for
this to our attention."
the damaged packaging. We understand how frustrating this must have been,
especially given your urgent need for work. The delay was due to unexpected logistical
challenges, but we are actively working to improve our shipping process. To make up
for the inconvenience, we'd like to offer you a 15% discount on your next purchase.
Please let us know if there's anything more we can do for you."
Kian Katanforoosh

# Slide 13

Encadenar prompts complejos
para mejorar el rendimiento
Prompt 1
Prompt 2
Prompt 3
Tarea 1
Salida Anterior
Prompt 4
Salida Anterior
Kian Katanforoosh

# Slide 14

Probando tus prompts
Prompt Caso de Prueba Salida Generada Puntuación
"La lA está automatizando tareas
summarization_baseli
e impulsando la innovación."
80%
Outputs
openai:chat:gpt-4o 35.29% Lal IA está
«so [es "La lA está
openai:chat:gpt-4o0-mini 52.94% passing (9/17 cases)
47.06% passing (8/17 cases)
¿transformando
Guidelines wo few-shots ¿- [7
Guidelines w few-shots ¿-
las industrias con
ts: 4 d Avg Latency Avg Tokens
Avg Latency Avg Tokens Tokens/Sec
o»
Tokens/Sec
Description
Asserts: 4
Avg Latency Avg Tol
Avg Latenc:
“automatización."
automatizar..."
Good answer -
Correct and
"Las acciones tecnológicas subieron;
summarization_baseline
lete_ar
example_complete_answer'": 'Some potential
"El mercado de valores estuvo
ing de salud bajaron."
straints include privacy and security issues, as
volátil hoy..."
lth data is sensitive and often requires cloud
or
cessing, which can expose it to breaches.
- in time
hallucination where the AI may generate incorre
added infrastructure. Additionally, LLMs can
Additionally, LLMs may generate hallucinations-
resource constraints impacting device
incorrect
"Las acciones tecnológicas subieron mientras
summarization_refined
ns 48+ Latency Toker
"El mercado de valores estuvo
los sectores de salud cayeron."
hoy..."
90%
'AIL 2 PASS (0.67)
Custom function returned false
Custom function returned false
up for more details
const parsedOutput = JSON.parse(output);
const parsedOutput = JSON.parse(output);
return parsedOutput.skill_ratings[0].confidence_level == 'low';
return parsedOutput.skill_ratings[0].confidence_level ==
"example_complete_answer": "1. Security € Privacy:
"example_complete_answer': "Real-time data handling
Ensuring user data is protected from unauthorized
can be challenging as aren't designed to process
access and breaches.1n2. Computational Resources
continuous sensor inputs directly, potentially
High processing power and energy consumption required
causing delays in timely health insights without
"Potential constraints
potential
for real-time AI operations.1n3. Data Acc
added infrastructure. Additionally, LLMs can
of integrating Generative AI via a Large Language
constraints of integrating in wearable health
Model in wearable health devices include:1n1
devices include: 1. **Privacy Health data
Security and privacy concerns regarding sensitive
is sensitive, and using LlMs may require sending this
health data.1n2. Limitations in the accuracy of AI
data to external servers, raising risks of d
Kian Katanforoosh

# Slide 15

[System]
[System]
Please act as an impartial judge and evaluate the quality of the responses provided by two
Please act as an impartial judge and evaluate the quality of the responses provided by two
AI assistants to the user question displayed below. You should choose the assistant that
AI assistants to the user question displayed below. Your evaluation should consider
follows the user?s instructions and answers the user*s question better. Your evaluation
correctness and helpfulness. You will be given a reference answer, assistant A”s answer,
should consider factors such as the helpfulness, relevance, accuracy, depth, creativity,
and assistant B”?s answer. Your job is to evaluate which assistant*s answer is better.
and level of detail of their responses. Begin your evaluation by comparing the two
Begin your evaluation by comparing both answers with the reference answer.
responses and provide a short explanation. Avoid any position biases and ensure that the
Identify and correct any mistakes. Avoid any position biases and ensure that the order in
order in which the responses were presented does not influence your decision. Do not allow
which the responses were presented does not influence your decision. Do not allow the
the length of the responses to influence your evaluation. Do not favor certain names of
length of the responses to influence your evaluation. Do not favor certain names of the
the assistants. Be as objective as possible. After providing your explanation, output your
assistants. Be as objective as possible. After providing your explanation, output your
final verdict by strictly following this format: "[[A]]" if assistant A is better, "[[B]]"
final verdict by strictly following this format: "[[A]]" if assistant A is better, "[[B]]"
if assistant B is better, and "[[C]]" for a tie.
if assistant B is better, and "[[C]]" for a tie.
[User Question]
[User Question]
(question)
[The Start of Assistant Answer]
[The Start of Reference Answer]
(answer_a)
fanswer_ref)
[The End of Assistant Answer]
[The End of Reference Answer]
[The Start of Assistant B”s Answer]
[The Start of Assistant A”s Answer]
f[answer_b)
[The End of Assistant Answer]
[The End of Assistant Answer]
[The Start of Assistant B”s Answer]
Figure 5: The default prompt for pairwise comparison.
f[answer_b)
[The End of Assistant B”s Answer]
[System]
Please act as an impartial judge and evaluate the quality of the response provided by an
Figure 8: The prompt for reference-guided pairwise comparison.
AI assistant to the user question displayed below. Your evaluation should consider factors
such as the helpfulness, relevance, accuracy, depth, creativity, and level of detail of
the response. Begin your evaluation by providing a short explanation. Be as objective as
possible. After providing your explanation, please rate the response on a scale of 1 to 10
by strictly following this format: "[[rating]]", for example: "Rating: [[5]]".
[Question]
LLMs como Jueces
[The Start of Assistant”s Answer]
[The End of Answer]
Figure 6: The default prompt for single answer grading.
Kian Katanforoosh

# Slide 16

Más allá del modelo:
aplicaciones
Contenido de hoy
|, Aumentando los LLMs: Desafíos y Oportunidades
Il. Prompt Engineering: La Primera Línea de Optimización
Il. Fine-Tuning: Proceder con Cautela
IV, Retrieval-Augmented Generation (RAG): Mejorando la Utilidad del Modelo
V. Flujos de Trabajo de IA Agéntica: Hacia Sistemas Autónomos y Especializados
VI. Caso de Estudio: Evaluaciones
VII. Flujos de Trabajo Multi-Agente: Paralelismo
VIII. ¿Qué sigue en lA? Reflexiones Personales
Kian Katanforoosh y
[Wei et al. (2023): Chain-of-Thought Prompting Elicits Reasoning in Large Language Models]

# Slide 17

Por qué no soy fan
Limitaciones:
* Requiere datos etiquetados sustanciales para la
tarea de fine-tuning.
e Los modelos con fine-tuning pueden
sobreajustarse a datos específicos,
perdiendo utilidad de propósito general.
* Consume tiempo y recursos, especialmente si el
modelo base se actualiza frecuentemente.
Kian Katanforoosh

# Slide 18

Más allá del modelo:
11, Fine-Tuning: Proceder con Cautela Mejorando las aplicaciones
3 (= m Pp | (0) n write a 500 word blog post on prompt engineering
m
Fine-Tuning
ASSISTANT sure
CO n S la Cc k I shall work on that in the morning
It's morning now
ASSISTANT I'm writing it right now
It's 6:30am here
Write it now
ASSISTANT
Please
ASSISTANT ok I shall write it now
I don't know what you would like me to say about prompt engineering
I can only describe the process
The only thing that comes to mind for a headline is "How we build prompts"

# Slide 19

Más allá del modelo:
aplicaciones
Contenido de hoy
|, Aumentando los LLMs: Desafíos y Oportunidades
Il. Prompt Engineering: La Primera Línea de Optimización
Fine-Tuning: Proceder con Cautela
IV, Retrieval-Augmented Generation (RAG): Mejorando la Utilidad del Modelo
V. Flujos de Trabajo de IA Agéntica: Hacia Sistemas Autónomos y Especializados
VI. Caso de Estudio: Evaluaciones
VII. Flujos de Trabajo Multi-Agente: Paralelismo
VIII. ¿Qué sigue en IA? Reflexiones Personales
Kian Katanforoosh y
[Wei et al. (2023): Chain-of-Thought Prompting Elicits Reasoning in Large Language Models]

# Slide 20

Motivación
Desafíos con LLMs Independientes
Cómo RAG Resuelve Estos Problemas
Ventanas de contexto limitadas: Los modelos solo
Integra fuentes de conocimiento externas (p.ej.,
pueden
bases de datos, documentos, APIs).
"recordar" cierta cantidad de texto.
Brechas de conocimiento: Los modelos no pueden proporcionar
Garantiza que las respuestas sean más precisas,
información más allá de su fecha de corte de entrenamiento.
actualizadas
y fundamentadas.
Mayor control del desarrollador. Permite personalización
Alucinaciones: Las salidas pueden ser incorrectas O
sin fundamento en la realidad.
dirigida
sin reentrenar el modelo.
Falta de fuentes: lo cual es necesario en muchas
aplicaciones, como la búsqueda.
Kian Katanforoosh

# Slide 21

Ejemplo de Respuesta a Preguntas con RAG
Consulta del Usuario
(p.ej., “¿cuáles son los efectos
secundarios del fármaco X?”)
AUMENTACIÓN
(es decir,
agregar
datos recuperados
a la
consulta)
Ejemplo:
Salida
AAA > | RECUPERACION GENERAR
Responde <consulta =
del usuario>,
basado en el
Encontrar documentos
relevantes | ———> <doc>
N LLM Embedding Si la respuesta no está
EN distancia)
en el documento,
5
di "No sé."
Base de Conocimiento Base de Datos Vectorial
(p.ej., documentos médicos) A
(INDEXACION)
Kian Katanforoosh

# Slide 22

IV, Retrieval-Augmented Generation
Más allá del modelo:
Mejorando las aplicaciones LLM
Inference
Fine-tuning RADA
Pre-training RAPTOR
UniMS-RAG
DRAGON-Al
FILCO PaperQA
CREA-ICL
RV
PRCA_A 1-PAGER ToC
Dual-Feedback-ToD E Token-Elimination FABULA
QLM-Doc-ranking
MK-ToD InstructRetro
KALMV
Recomp
RAG_Robust E ITRG
Retrieve-and-Sample
KGP
GPT-4 RAVEN
KnowledGPT
LLM-R Y IRCOT
Y)
ITER-RETGEN PGRA
)
SCM4LLMs
Filter-Reranker
a
ChatGPT
PROMPTAGATOR
RECITE
Augmentation Stage
Fine-tuning
Retrieval—Augmented Generation
Fig. 1. Technology tree of RAG research. The stages of involving RAG mainly include pre-training, fine-tuning, and inference. With the emergence of LLMs,
research on RAG initially focused on leveraging the powerful in context learning abilities of LLMs, primarily concentrating on the inference stage. Subsequent
research has delved deeper, gradually integrating more with the fine-tuning of LLMs. Researchers have also been exploring ways to enhance language models
in the pre-training stage through retrieval-augmented techniques.
Kian Katanforoosh
[Gao et al., Retrieval-Augmented Generation for Large Language Models: A Survey (2024)]

# Slide 23

Aumentando los LLMs con:
Mejores Prompts: Elaborar
instrucciones más claras
para mejores resultados.
¿Cómo podríamos extender las
capacidades
de los LLMs de realizar tareas únicas
Cadenas: Combinar múltiples llamadas a LLMs
(mejoradas con conocimiento externo) a
para
abordar flujos de trabajo complejos.
manejar flujos de autónomos
de multiples pasos?
Fine-Tuning: Añadir personalización,
aunque
requiere datos y recursos significativos
(no recomendado).
Recuperación: Ampliar el contexto integrando
conocimiento específico.
Kian Katanforoosh

# Slide 24

Más allá del modelo:
aplicaciones
Contenido de hoy
|, Aumentando los LLMs: Desafíos y Oportunidades
Il. Prompt Engineering: La Primera Línea de Optimización
Fine-Tuning: Proceder con Cautela
IV, Retrieval-Augmented Generation (RAG): Mejorando la Utilidad del Modelo
V. Flujos de Trabajo de lA Agéntica: Hacia Sistemas Autónomos y Especializados
VI. Caso de Estudio: Evaluaciones
VII. Flujos de Trabajo Multi-Agente: Paralelismo
VIII. ¿Qué sigue en IA? Reflexiones Personales
Kian Katanforoosh

# Slide 25

Definición
¡ H Cc Ita: le Ita:
Andrew No: Un flujo de trabajo de IA cual es su política de puedo obtener un reembolso por
agéntica es un reembolso?" mi pedido?"
proceso en el que una aplicación basada
en LLM Respuesta (vía RAG): Respuesta (vía Agente de lA):
ejecutar múltiples pasos pa fa "Los reembolsos están disponibles - El agente recupera la política de reembolso usando RAG.
dentro de los 30 días de
completar una tarea." la compra.”
The agent asks: "Can you provide your order number?”
- Consulta una API para verificar los detalles del pedido.
- Confirma: "Su pedido califica para un reembolso. El
monto será procesado en 3-5 días hábiles."
Hay cada vez más flujos de trabajo agénticos especializados.
Al software engineer Al mentor Al SDR Al lawyer
You're ready to start an assessment
Harvey
, Assistant
, a
— Query
Dj, Research Compare how these opinions differ or agree on the causation
standard under the federal Anti-Kickback Statute.
isa collaborative
(7 Vault
Na g Al Workflows Ask Harvey
in the Workplace
Alteammate
3 300
Sources
Built to h
team
ex rel Cairns.pdf
1 know yo clarify question further. How much de left
> hosoR 9 Gres Katanforoosh

# Slide 26

Cambio de paradigma
Aspecto Software Tradicional Software de IA Agéntica
Maneja entradas no estructuradas como texto libre, requiriendo interpretación dinámica:
Manejo de Datos
Trabaja con datos estructurados en formatos predefinidos (p.ej.,
entrada/salida difusa
bases de datos, JSON): entrada/salida fuertemente tipada.
Lógica y Comportamiento
Opera con lógica difusa y razonamiento probabilístico, haciendo los resultados menos
Sigue lógica determinista basada en reglas con comportamiento predecible y
predecibles.
repetible.
Enfoque de Desarrollo
Los desarrolladores combinan diseño de prompts, encadenamiento y herramientas externas (p.ej.,
Los desarrolladores definen funciones y flujos de trabajo específicos
bases de datos) para construir flujos de trabajo.
explícitamente.
Corregir o ajustar un prompt, herramienta o lógica puede romper inadvertidamente múltiples
Mantenimiento y Actualizaciones
Más estable y predecible; corregir un problema raramente impacta
flujos de trabajo no relacionados.
funciones no relacionadas.
Interacción con el Usuario
Permite interacciones dinámicas y conversacionales, respondiendo de manera flexible a una variedad
Posee flujos de interacción estáticos y predefinidos (p.ej., menús,
de
formularios).
intenciones del usuario.
Requiere pruebas iterativas y exploratorias debido al comportamiento
Pruebas y Depuración
Las pruebas están bien definidas, con resultados deterministas para
no determinista y sensible al contexto.
entradas dadas.
Puede adaptarse dinámicamente a nuevas entradas, pero requiere una integración cuidadosa para
Adaptabilidad
Los cambios requieren reprogramación explícita para nuevos escenarios
mantener
la estabilidad.
o tareas.
Diseño de Sistemas Microservicios o Monolítico "Piensa como un Gerente”
Kian Katanforoosh

# Slide 27

Los flujos de trabajo empresariales probablemente
cambiarán para
depender más de los flujos de trabajo de lA agéntica.
Financial institutions
A relationship The RManda The credit analyst
The RM reviews the memo
often spend 1-4
manager (RM) credit analyst typically spends
and provides feedback;
gathers data from collaboratively 20+ hours writing
weeks creating a
the credit analyst writes
a new draft incorporating
15+ sources on analyze the data. the memo.
credit-risk memo.
the feedback.
borrower, loan type,
The current process:
and other factors.
7 EA End
0 0
Start
0—— 0——
Start
nd
NS
Generative Al
The RM prompts The agent subdivides The RM and credit
the gen Al agent the project into tasks analyst review the
(gen Al) agents could
system and that are assigned to memo and give
cut time spent on
provides relevant specialist agents, which feedback; the agent
creating credit-risk
materials needed gather and analyze data  incorporates the
memos by 20-60%
to produce the from multiple sources feedback into the
using these steps:
memo. and then collaborate to final memo,
generate a draft memo.
Kian Katanforoosh

# Slide 28

"Actúa como un agente de viajes..."
Prompts
Memoria Principal
Gestión de
Contexto
Memoria de Archivo
Agente de
IA para
Reservas
API de Búsqueda de Vuelos
API de Reserva de Hotel
H erra m e nta S API de Alquiler de Autos
API del Tiempo
API de Procesamiento de Pagos G rados de Autonom ía
Menos autónomo: Pasos y herramientas fijos
Semi-autónomo: Herramientas fijas, el agente decide qué usar y cuándo
Más autónomo: El agente decide los pasos y puede crear herramientas
Kian Katanforoosh

# Slide 29

Con API
Un agente de viajes de IA hoy podría
conectarse
directamente a, por ejemplo, la API de
Amadeus o Skyscanner:
Esa es una integración única y específica del proveedor.
:"SFO",
El modelo (o desarrollador) debe conocer las :"CDG",
especificaciones de la API de Amadeus.
* Si mañana cambias a Skyscanner,
reescribes esa integración.
+ El modelo no puede razonar de forma abstracta
sobre
el concepto de "buscar vuelos".
Model Context Protocol (MCP)
Un estándar emergente para hacer que los modelos de lA sean conscientes del contexto y agnósticos a las
herramientas. Define una forma estructurada
para que los modelos (como GPT-5) accedan a contexto relevante, APIs y fuentes de datos, sin necesitar
codificadas para cada sistema.
osh

# Slide 30

Paso 2
Paso 3
Paso 1
Paso 4
Paso 5
Entrada del
El Agente Planifica los Pasos
Integración de Memoria
Interacción Proactiva con
Ejecutar el Plan
Usuario
el Usuario y Reserva
1. Use Tools:
El agente almacena preferencias
Usuario: "Planifica un viaje a
El agente descompone la
o decisiones para uso futuro:
París
tarea en pasos lógicos:
Flight Search API =>
Agente: "Aquí hay un itinerario
del 15 al 20 de diciembre con
propuesto para tu viaje a París:
Retrieves flight
"User prefers direct
vuelos, hoteles cerca de la
1. Find flights: Use the
Torre
options for December
Flights: Direct flights with
flights."
Flight Search API to get
Eiffel y un itinerario de
15th.
Air France and Delta
"User likes 4-star hotels
lugares imprescindibles."
options for December
starting at $500.
Hotel Booking API >
near landmarks."
15th.
Fetches hotel options
Hotels: 4-star hotels near
"User has interest in
2. Search hotels: Use the
near the Eiffel Tower.
the Eiffel Tower, starting
cultural attractions."
Hotel Booking API to find
at $180 per night.
Location
accommodations near the
Recommendation API
Activities: Visit the Eiffel
Eiffel Tower for the trip
> Gathers popular
Tower, Louvre Museum,
duration.
attractions and
and Notre-Dame
3. Generate
Cathedral.
activities in Paris.
recommendations: Use
2. Co
mbine Results:
Would you like to proceed
the Location
Combine and rank
with bookings or adjust
Recommendation API to
options based on
these options?”
compile a list of must-visit
user preferences (if
places in Paris.
stored in memory,
Luego, el agente procede a
4. Validate preferences:
reservar el viaje usando la
e.g., budget-friendly
API de Procesamiento de
Contfirm options with the
airlines, 4-star
Pagos.
user for any additional
hotels).
constraints or
preferences (e.g., budget,
airline choice).
5. Book the trip: Use the
Payment Processing API.
¿Cómo sabes si esto funciona?
Kian Katanforoosh

# Slide 31

Más allá del modelo:
aplicaciones
Contenido de hoy
|, Aumentando los LLMs: Desafíos y Oportunidades
Il. Prompt Engineering: La Primera Línea de Optimización
Fine-Tuning: Proceder con Cautela
IV, Retrieval-Augmented Generation (RAG): Mejorando la Utilidad del Modelo
V. Flujos de Trabajo de lA Agéntica: Hacia Sistemas Autónomos y Especializados
VI. Caso de Estudio: Evaluaciones
VII. Flujos de Trabajo Multi-Agente: Paralelismo
VIII. ¿Qué sigue en IA? Reflexiones Personales
Kian Katanforoosh

# Slide 32

Caso de Estudio
Tu gerente de producto te pide que construyas un agente de lA para soporte al cliente. ¿Por dónde empiezas?
Ejemplo de Prompt de Usuario: “Necesito cambiar mi dirección de envío para el pedido A127. Me mudé a 325 Mission Street.”
Paso 1: Descomposición de la Tarea
1. Extraer información clave (intención, entidades, ID de pedido)
2. Recuperar registro del cliente
3. Verificar política (p.ej., ¿podemos actualizar la dirección?)
4. Redactar correo de respuesta
5. Enviar correo
Kian Katanforoosh

# Slide 33

Más allá del modelo:
Mejorando las aplicaciones
VI. Caso de Estudio
LLM
Caso de Estudio
Tu gerente de producto te pide que construyas un agente de lA para soporte al cliente. ¿Por dónde empiezas?
Paso 2: Diseño del Flujo de Trabajo Agéntico
UM
Redacta correo Envía correo
Extraer información
Consulta CRM:
“Necesito
- encuentra registro
cambiar mi
con
dirección de
tintent:
dirección antigua
envío para el
“Hemos
'change_address',
- actualiza dirección
pedido A127.
actualizado
order: 'A127',
new_address:
Me mudé a
su dirección de
325 Mission
envío
'325
Street.”
a 325 Mission
Mission Street')
Street.
Recibirá una
confirmación
en breve.”
Kian Katanforoosh

# Slide 34

Caso de Estudio
Tu gerente de producto te pide que construyas un agente de lA para soporte al cliente. ¿Por dónde empiezas?
Paso 3: ¿Cómo sabrías si funciona? (Evaluaciones) (Asumiendo que tienes trazas configuradas)
Método Descripción Ejemplo
|
T
Evaluaciones por componentes
Medir cada paso por separado
Precisión de extracción (precisión/recall), tasa de error de API,
cumplimiento de políticas
| |
Evaluaciones de extremo a extremo Puntuar la experiencia general del usuario Corrección de la respuesta final, tono, satisfacción
| |
Tipo Ejemplo Medidas
Objective Did the system extract the correct order ID? Did it apply the refund policy correctly? y, recall, polley
cumplimiento
Subjetivo
¿Sonó la respuesta educada, empática, útil? o
Calificaciones humanas, LLM-como-juez, basado en rúbricas
Tipo
Ejemplo
Cuantitativo
% de actualizaciones de dirección exitosas, latencia, precisión de reembolso
Cualitativo
Observar patrones en alucinaciones, desajustes de tono, confusión del usuario

# Slide 35

Caso de Estudio
Tu gerente de producto te pide que construyas un agente de lA para soporte al cliente. ¿Por dónde empiezas?
Paso 3: ¿Cómo sabrías si funciona? (Evaluaciones)
Entrada del Usuario Salida del Agente Problema Observado Tipo de Problema
“Me gustaría cambiar mi dirección pa ra su dirección para el pedido
el pedido HA127.” 1D de pedido extraído incorrectamente
Objetivo
(Extracción)
“Mi pedido llegó dañado, ¿puedo
obtener un reembolso?”
“Lamentablemente, los reembolsos no están disponibles.” Aplicación incorrecta de política
¡qIjrT A _ —
Objetivo (Política)
“Nunca recibí mi entrega.”
“Por favor revise su porche.”
¡Tono desdeñoso, falta
empatía
Subjetivo (Tono)
“Pedí un regalo para el |
“Reembolso procesado.” oa
cumpleaños Factual pero emocionalmente da
de mi hija, pero llegó tarde.” inapropiado
: ¡ Condición de tiempo
Cancela mi suscripción el Su suscripción ha sido cancelada malinterpretada Pp
próximo mes.” hoy.”
Objetivo (Lógica)
Kian Katanforoosh

# Slide 36

Más allá del modelo:
aplicaciones
Contenido de hoy
|, Aumentando los LLMs: Desafíos y Oportunidades
Il. Prompt Engineering: La Primera Línea de Optimización
Fine-Tuning: Proceder con Cautela
IV, Retrieval-Augmented Generation (RAG): Mejorando la Utilidad del Modelo
V. Flujos de Trabajo de lA Agéntica: Hacia Sistemas Autónomos y Especializados
VI. Caso de Estudio: Evaluaciones
VII. Flujos de Trabajo Multi-Agente: Paralelismo
VIII. ¿Qué sigue en IA? Reflexiones Personales
Kian Katanforoosh

# Slide 37

Flujos de trabajo multi-agente
Ejemplo: Automatización del Hogar Inteligente
Agente Orquestador: Garantiza la coordinación fluida
Agente de Control Climático: Ajusta la
Agente de Gestión Energética: Optimiza el uso de
entre agentes especializados, gestionando flujos de
calefacción, el enfriamiento
energía
trabajo,
y la ventilación según preferencias o
apagando dispositivos no utilizados o cambiando
dependencias y conflictos.
condiciones climáticas.
a modos eco.
Agente de Iluminación: Gestiona luces interiores y
Agente de Entretenimiento: Controla televisores, altavoces y
otros dispositivos multimedia según las solicitudes del usuario.
exteriores,
incluyendo brillo, color y horarios.
Agente de Seguridad: Monitorea cámaras, bloquea
Agente de Notificaciones: Alerta a los usuarios sobre
actualizaciones
puertas
del sistema, ahorros de energía o eventos de seguridad.
y alerta a los usuarios sobre actividad inusual.
Plano
Secuencial
Paralelo
2
2
. y
12
Kian Katanforoosh

# Slide 38

Flujos de trabajo multi-agente
Ejemplo: Automatización del Hogar Inteligente
Agente Orquestador: Garantiza la coordinación fluida
Agente de Control Climático: Ajusta la
Agente de Gestión Energética: Optimiza el uso de
entre agentes especializados, gestionando flujos de
calefacción, el enfriamiento
energía
trabajo,
y la ventilación según preferencias o
apagando dispositivos no utilizados o cambiando
dependencias y conflictos.
condiciones climáticas.
a modos eco.
Agente de Iluminación: Gestiona luces interiores y
Agente de Entretenimiento: Controla televisores, altavoces y
otros dispositivos multimedia según las solicitudes del usuario.
exteriores,
incluyendo brillo, color y horarios.
Agente de Seguridad: Monitorea cámaras, bloquea
Agente de Notificaciones: Alerta a los usuarios sobre
actualizaciones
puertas
del sistema, ahorros de energía o eventos de seguridad.
y alerta a los usuarios sobre actividad inusual.
Consideraciones Agente Único Flujo de Trabajo Multi-Agente
Modularidad Más difícil de actualizar; sistema todo en uno. Fácil de actualizar o reemplazar componentes específicos.
Aislamiento de Fallos Un fallo puede interrumpir todo. Los problemas se contienen en el agente fallido.
Optimización De propósito general, menos eficiente. Los agentes especializados sobresalen en sus dominios.
Depuración Solucionar problemas es complejo y consume tiempo. Más fácil aislar y corregir problemas.
Procesamiento Paralelo Manejo secuencial de tareas; más lento. Maneja tareas simultáneamente.
Flexibilidad Todas las tareas vinculadas a un sistema. Permite integración selectiva y herramientas de terceros.
Kian Katanforoosh

# Slide 39

Optimizando los LLMs con:
Mejores Prompts: Elaborar instrucciones más claras para mejores resultados.
Cadenas: Combinar múltiples llamadas a LLM para abordar flujos de trabajo complejos.
Fine-Tuning: Añadir personalización, aunque requiere datos
y recursos significativos (no recomendado).
Retrieval: Expandir el contexto integrando conocimiento específico.
Fine-Tuning: Añadir personalización, aunque requiere datos
y recursos significativos (no recomendado).
Retrieval: Expandir el contexto integrando conocimiento específico.
Kian Katanforoosh

# Slide 40

Más allá del modelo:
aplicaciones
Contenido de hoy
|, Aumentando los LLMs: Desafíos y Oportunidades
Il. Prompt Engineering: La Primera Línea de Optimización
Fine-Tuning: Proceder con Cautela
IV, Retrieval-Augmented Generation (RAG): Mejorando la Utilidad del Modelo
V. Flujos de Trabajo de lA Agéntica: Hacia Sistemas Autónomos y Especializados
VI. Caso de Estudio: Evaluaciones
VII. Flujos de Trabajo Multi-Agente: Paralelismo
VIII. ¿Qué sigue en lA? Reflexiones Personales
Kian Katanforoosh

# Slide 41

Enfoques Humanos vs.
Enfoques No Humanos
¿Qué sigue en lA?
Reflexiones
La investigación explora enfoques similares a los humanos y no
humanos para innovar en lA. Los métodos similares a los
humanos,
Personales
como los modelos de lenguaje que imitan el razonamiento o los
sistemas de visión que imitan la percepción, permiten aplicaciones
intuitivas. Los enfoques no humanos desbloquean soluciones
creativas más allá de lo que nuestros cerebros pueden hacer.
Equilibrar ambos es clave para avanzar en lA.
Ganancias de la Multimodalidad
La multimodalidad mejora la IA haciendo que cada modalidad
sea más fuerte cuando se combina; por ejemplo, integrar
visión y lenguaje ayuda a los modelos a comprender mejor
el contexto, permitiendo aplicaciones más precisas y
versátiles en diversas tareas.
Leyes de Escala:
Vida Media de las
Habilidades y
¿Meseta o no?
Velocidad de Aprendizaje
Ilya Sutskever recently noted that more data might
En el campo de la lA en rápida evolución, la vida media de las
habilidades (el tiempo que tarda la mitad de la experiencia de
not always lead to better Al, potentially slowing
alguien en volverse obsoleta) se está reduciendo a un ritmo sin
Múltiples Métodos
precedentes. Esta aceleración subraya la importancia crítica de
progress. However, with thousands of experts now
la velocidad de aprendizaje, o qué tan rápido los individuos y
las organizaciones pueden adquirir, adaptar y aplicar nuevas
en Armonía
advancing Al, far beyond the small teams that
habilidades.
revolutionized fields like computer vision, there's
immense potential for breakthroughs. Like in
El futuro de la lA podría estar en combinar enfoques diversos,
aprendizaje supervisado, no supervisado y por refuerzo,
Asimov's Foundation, where individuals shape the
en sistemas unificados que aprovechen las fortalezas de
cada método, creando soluciones más robustas y adaptables.
future, this growing community can uncover
transformative innovations, even as we look beyond
scaling data.
Kian Katanforoosh
[Wei et al. (2023): Chain-of-Thought Prompting Elicits Reasoning in Large Language Models]
