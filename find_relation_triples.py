import google.generativeai as genai
import json
import os

# Para fazer o código rodar é necessário ter a biblioteca do geminiAi instalada e precisa ter uma key da geminiAi
# registrada na máquina como uma variável de ambiente sob o nome API_KEY. Consulte o "READ-ME" para mais informações.

genai.configure(api_key=os.environ["API_KEY"])

# Modelo gemini-1.5-flash configurado para exibir respostas apenas como estruturas json válidas, impedindo a LLM de
# gerar textos desnecessários para o programa.

model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "application/json"})

# texto de entrada precisa estar completamente armazenado dentro do arquivo 'paragraph.txt' para que o programa funcione
# como esperado.

f = open("paragraph.txt")
paragraph = f.read()

# principal prompt do programa, responsável por processar o texto de entrada e identificar o máximo possível de entidades
# e relacionamentos possíveis entre eles, é passado no prompt os tipos de entidades mais importantes e o mesmo acontece
# com os relacionamentos. Uma pequena linha de texto é incluida para evitar que o programa tipifique a mesma entidade
# da mesma forma, mesmo se o mesmo nome está se referindo a entidades diferentes. O exemplo apresentado tem a função de
# guiar o programa para que ela identifique entidades e nomeie relacionamentos da melhor forma possível.

prompt = """
Given a prompt, identify as many entities and relations among them as possible and output a list of relations in the format 
[ENTITY 1, ENTITY 1 TYPE, RELATION, ENTITY 2, ENTITY 2 TYPE]. The relations are directed, so the order matters.
Top entities of interest: person, location, organization, date, occupation (a.k.a. person's work, specialization, 
research discipline, interests, occupation), technology, event, work of art.
Top relations of interest: "works as", "worked as", "works for", "worked for", "was released in", "was born in", "is from",
"participates in", "happened at"
Reminder: The same word can refer to two different types of entities inside the same text. Context is important.

Example:
prompt: Barack Obama (born August 4, 1961) is an American politician who served as the 44th president of the United 
States from 2009 to 2017. A member of the Democratic Party, he was the first African-American president in U.S. history.
output:
["Barack Obama", "person", "was born in", "August 4, 1961", "date"],
["Barack Obama", "person", "works as", "politician", "occupation"],
["Barack Obama", "person", "has nationality", "american", "nationality"],
["Barack Obama", "person", "worked as", "president", "occupation"],
["Barack Obama", "person", "is from", "United States", "location"],
["Obama's presidency of the United States", "event", "started in", "2009", "date"],
["Obama's presidency of the United States", "event", "ended at", "2017", "date"],
["Barack Obama", "person", "is part of", "Democratic Party", "group"],
["Barack Obama", "person", "has race", "African-American", "race"],


Here goes the prompt that you need to identify entities and relations:

"{}"
""".format(paragraph)

# Nessa parte do código é gerada a resposta da LLM. Também se configura a temperatura para 0 para se garantir que os
# resultados sejam determinisitcos, uma entrada de texto irá sempre gerar o mesmo grafo de conhecimento.

response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(temperature=0.0))

# Finalmente, deve-se converter a lista resultante da interação com a LLM em uma estrutura JSON, para isso, cada tupla
# contendo entidade 1, seu tipo, relação, entidade 2 e seu tipo, será convertida em um dicionário, onde cada item é
# mapeado por uma string que representa a sua função dentro daquela tupla. Com isto feito, os resultados são escritos em
# "Relations.json

list_of_relations = eval(response.text)
list_of_json_schemas = []
for relation in list_of_relations:
    json_schema = dict()
    json_schema["entity 1"] = relation[0]
    json_schema["entity 1 type"] = relation[1]
    json_schema["relation"] = relation[2]
    json_schema["entity 2"] = relation[3]
    json_schema["entity 2 type"] = relation[4]
    list_of_json_schemas.append(json_schema)

with open("Relations.json", "w") as outfile:
    json.dump(list_of_json_schemas, outfile)