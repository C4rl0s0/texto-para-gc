import json

# função que nomeia entidades recebidas substituindo espaços e hifens por underlines. função também normaliza os dados
# fazendo com que cada nome seja constituido apenas de letras minusculas, para evitar que a mesma entidade seja representada
# com vértices distintos por causa de diferenças entre caracteres minusculos e maiusculos.

def underlined(s: str) -> str:
    s = s.replace(' ','_')
    s = s.replace(',','')
    return s.replace('-', '_').lower()

# função que nomeia relacionamentos em camel case, escolha puramente estética e pode ser alterada dependendo da configuração
# do neosemantics.

def camel_case(s: str) -> str:
    temp = s.split(' ')
    for i, word in enumerate(temp):
        if i == 0:
            continue
        temp[i] = word.capitalize()
    return ''.join(temp)

# o código recebe como entrada o conteúdo dentro do arquivo "Relations.json" e registrará o conteúdo de saída dentro
# do arquivo "graph.txt". O arquivo de saída não tem extensão rdf, mas terá formatação em rdf. O neosemantics permite
# que você copie e cole textos formatados em turtle ou importe arquivos txt e ele reconhece isso como um arquivo rdf,
# logo bibliotecas como rdf2lib não são necessárias.

f = open("Relations.json")
rdf_file = open("graph.txt", "w")
x = f.read()
relations = json.loads(x)
entities = dict()
disambiguities = dict()
uri_map = {"person": "Person", "location": "Place", "organization": "Organization", "date": "Date",
           "occupation": "Occupation", "technology": "Product", "event": "Event", "work of art": "CreativeWork"}

# Primeira etapa do código é extrair todas as entidades presentes na estrutura, juntamente com seu respectivo tipo.
# Para isto, extrai-se de cada relação dentro da estrutura JSON a entidade 1 e 2, armazenando elas em um dicionário
# 'entities', e estas entidades são então mapeadas a seu tipo. Dentro desta etapa também é realizada uma normalização,
# caso o código identifique uma entidade já presente em 'entities' mas ela contém um tipo diferente, essa entidade é
# adicionada ao dicionário 'disambiguities' para que seja devidamente tratada ao decorrer do código.

for relation in relations:
    if relation["entity 1"] in entities.keys() and relation["entity 1 type"] != entities[relation["entity 1"]]:
        disambiguities[relation["entity 1"]] = relation["entity 1 type"]
    else:
        entities[relation["entity 1"]] = relation["entity 1 type"]
    if relation["entity 2"] in entities.keys() and relation["entity 2 type"] != entities[relation["entity 2"]]:
        disambiguities[relation["entity 2"]] = relation["entity 2 type"]
    else:
        entities[relation["entity 2"]] = relation["entity 2 type"]

# Nesta etapa já é começada a escrita da estrutura RDF, adicionando os prefixos que serão necessários.

rdf_file.write("@prefix ex: <https://example.org/> .\n@prefix sch: <https://schema.org/> .\n\n")

# Nesta etapa são escritas dentro do arquivo "graph.txt" todas as relações identificadas, criando triplas
# <Sujeito-verbo-predicado> com uma URI básica. Caso uma destas triplas tenha uma das entidades ambíguas, o
# programa é capaz de detectar isso pelo mapeamento entre o nome da entidade e seu tipo não existir no 
# dicionário 'entities', então para resolver a desambiguidade, é adicionado ao nome da entidade o tipo que ela
# representa, criando uma entidade distinta.

for relation in relations:
    e1, e1t, r, e2, e2t = relation.values()
    if entities[e1] != e1t:
        e1 += " " + disambiguities[e1]
    if entities[e2] != e2t:
        e2 += " " + disambiguities[e2]
    rdf_file.write(f"ex:{underlined(e1)} ex:{camel_case(r)} ex:{underlined(e2)} .\n")

rdf_file.write("\n")

# Por último, se utiliza do dicionário 'entities' criado anteriormente para delimitar o tipo de cada entidade detectada
# pelo protótipo, incluindo todos os tipos encontrados ao grafo. O dicionário 'uri-map' mapeia cada tipo previsto na
# detecção de entidades para o seu esquema válido dentro da URL Schema.org, caso o programa identifique uma entidade que
# não foi prevista pelo código, sua URI passa a ser Schema.org/Thing, que equivale ao tipo mais genérico de item dentro
# do sistema. O mesmo método de desambiguação é feito aqui, exceto que tudo que é necessário é percorrer também
# o dicionário 'disambiguities'.

for entity, type in entities.items():
    rdf_file.write(f"ex:{underlined(entity)} a sch:{uri_map.get(type, 'Thing')} .\n")

for entity, type in disambiguities.items():
    entity += " " + str(type)
    rdf_file.write(f"ex:{underlined(entity)} a sch:{uri_map.get(type, 'Thing')} .\n")

f.close()
rdf_file.close()
