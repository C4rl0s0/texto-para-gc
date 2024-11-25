# O que é necessário para poder rodar o programa:

Para poder executar o código da forma desejada, é preciso que sua máquina possua duas coisas: A biblioteca da gemini API e uma API Key da google. Para instalar a biblioteca da API do GeminiAI, abra seu terminal (com um PATH direcionando ao arquivo Python.exe) e digite o seguinte comando:

pip install -q -U google-generativeai

E por último, gere a sua chave API dentro do site da google AI <https://aistudio.google.com/app/apikey?hl=pt-br>, e para que o programa consiga acessar essa chave, armazene ela como uma variável de ambiente dentro de sua máquina com o nome 'API-KEY'.

Em caso de dúvida, consulte o guia de primeiros passos da API <https://ai.google.dev/gemini-api/docs/get-started/tutorial> e sinta-se livre para alterar as primeiras linhas de código do arquivo 'find_relation_triples.py' para melhor adequar suas necessidades.

# Como executar o programa:

Antes de executar o programa, você precisa ter um arquivo 'paragraph.txt', e dentro deste precisa ter **apenas** o texto que você deseja converter para grafo. (O tamanho do texto é dependente do limite de tokens do modelo apresentado. Consulte o modelo para mais informações.)

depois disso, você precisa executar **nesta sequência** os arquivos 'find_relation_tuples.py' e 'json_to_rdf.py'. Você pode executar estes arquivos por meio de alguma IDE de sua escolha, ou, caso prefira, executar diretamente abrindo o terminal de comandos e digitando estes comandos **nesta ordem**:

python find_relation_tuples.py

python json_to_rdf.py

# Como utilizar a saída do programa:

O propósito do programa é que você possa utilizar ele para criar um grafo de conhecimento, porém a saída que ele cria (dentro do arquivo 'graph.txt') é um arquivo de texto formatado em Turtle. Para visualizar e criar de fato o grafo, importe o arquivo para um servidor dentro do Neo4J utilizando o plug-in Neosemantics.
