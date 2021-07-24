Tips Arena Core
_______________
Rotinas para controle e execução das rotinas batch.

Fluxo extração e processamento de dados

1. Fazer a extração do HTML da lista de países
    * Insere o HTML na fila de processamento de países.
2. Processar o HTML da lista de países
    * Obtem as URLs de competições de cada país.
    * Insere a URL do país na fila de extração de competições do país.
3. Extrair o HTML das competições para cada URL de país.
    * Insere o HTML na fila de processamento de edições de competição
4. Processar o HTML das competições de cada país
    * Obtem as URLs das edições de cada competição
    * Insere a URL de cada edição da competição na fila de extração de edições da competição.
5. Extrair o HTML edições da competição
    * Insere HTML da edições da competição contendo a lista na fila de processamento de edições.
6. Processar o HTML de edições da competição
    * Obtem as URLs de edições de uma competição
    * Insere cada URL de edição de competição nas filas
        - extração do HTML das partidas da edição da competição.
        - extração do HTML da edição da competição.
        - extração do HTML das equipes da edição da competição
7. Extrair HTML partidas da edição da competição
    * Insere o HTML na fila de processamento de partidas da edição da competição.
8. Processar HTML partidas da edição da competição
    * Obtem as URLs das partidas da edição da competição
    * Insere cada URL de partida na fila de extração de partida.
9. Extrair HTML equipes edição da competição
    * Insere o HTML na fila de processamento de equipes da edição da competição.
10. Processar HTML equipes da edição da competição
    * Obtem as URLs das equipes da edição.
    * Insere cada URL de equipe na fila de extração de equipe










Licença
-------

Copyright (C) 2018 DevRox Tech (Daniel Cirino).
