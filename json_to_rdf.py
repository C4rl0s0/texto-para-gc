import json

# função que nomeia entidades recebidas substituindo espaços e hifens por underlines. função também normaliza os dados
# fazendo com que cada nome seja constituido apenas de letras minusculas, para evitar que a mesma entidade seja representada
# com vértices distintos por causa de diferenças entre caracteres minusculos e maiusculos.

def underlined(s: str) -> str:
    s = s.replace(' ','_')
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
uri_map = {"person": "Person", "location": "Place", "organization": "Organization", "date": "Date",
           "occupation": "Occupation", "technology": "Product", "event": "Event", "work of art": "CreativeWork"}

# Primeira etapa do código é extrair todas as entidades presentes na estrutura, juntamente com seu respectivo tipo.
# Para isto, extrai-se de cada relação dentro da estrutura JSON a entidade 1 e 2, armazenando elas em um dicionario
# 'entities', e estas entidades são então mapeadas a seu tipo. Dentro desta etapa também é realizada uma normalização,
# caso o código identifique uma entidade já presente em 'entities' mas ela contém um tipo diferente, é adicionado a
# entidade um parenteses indicando o tipo desta entidade e então ela pode ser armazenada como uma entidade distinta.

for relation in relations:
    if relation["entity 1"] in entities.keys() and relation["entity 1 type"] != entities[relation["entity 1"]]:
        disambiguity = relation["entity 1"] + f" ({relation['entity 1 type']})"
        entities[disambiguity] = relation["entity 1 type"]
    else:
        entities[relation["entity 1"]] = relation["entity 1 type"]
    if relation["entity 2"] in entities.keys() and relation["entity 2 type"] != entities[relation["entity 2"]]:
        disambiguity = relation["entity 2"] + f" ({relation['entity 2 type']})"
        entities[disambiguity] = relation["entity 2 type"]
    else:
        entities[relation["entity 2"]] = relation["entity 2 type"]

# Nesta etapa já é começada a escrita da estrutura RDF, adicionando os prefixos que serão necessários.

rdf_file.write("@prefix ex: <https://example.org/> .\n@prefix sch: <https://schema.org/> .\n\n")

# Nesta etapa são escritas dentro do arquivo "graph.txt" todas as relações identificadas, criando triplas
# <Sujeito-verbo-predicado> com uma URI básica.

for relation in relations:
    e1, _, r, e2, _ = relation.values()
    rdf_file.write(f"ex:{underlined(e1)} ex:{camel_case(r)} ex:{underlined(e2)} .\n")

rdf_file.write("\n")

# Por último, se utiliza do dicionário 'entity' criado anteriormente para delimitar o tipo de cada entidade detectada
# pelo protótipo, incluindo todos os tipos encontrados ao grafo. O dicionário 'uri-map' mapeia cada tipo previsto na
# detecção de entidades para o seu esquema válido dentro da URL Schema.org, caso o programa identifique uma entidade que
# não foi prevista pelo código, sua URI passa a ser Schema.org/Thing, que equivale ao tipo mais genérico de item dentro
# do sistema.

for entity, type in entities.items():
    rdf_file.write(f"ex:{underlined(entity)} a sch:{uri_map.get(type, 'Thing')} .\n")

f.close()
rdf_file.close()