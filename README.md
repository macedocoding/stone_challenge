# Desafio técnico Stone

Desafio técnico relativo ao processo seletivo da empresa Stone para o cargo de estagiário de Engenharia de Dados.
A disponibilização dos serviços utilizados será feita por meio de containeres Docker, portanto é fundamental a instalação do Docker Engine e Docker Compose v2.

[Instalação Docker Engine/Docker Compose](https://docs.docker.com/engine/install/)

## Instalação e configuração do ambiente

### Ambiente Python
Após clonar o repositório em sua máquina local, acesse diretório e crie um ambiente virtual Python com o comando `python -m .venv venv`.
Após isso, [ative o ambiente](https://docs.python.org/3/library/venv.html) conforme seu sistema operacional.

### Requerimentos
As bibliotecas Python utilizadas foram listadas no arquivo `requirements.txt` e podem ser instaladas através do comando `$ pip install -r rquirements.txt`.

### Solução OLTP local em Postgres
Após criar um ambiente virtual Python, acesse a pasta `postgres` e rode o comando `docker compose -f docker-compose.yaml up -d`.

Isso vai levantar um container Docker Postgres e executará as queries de criação das tabelas.
Lembrando que a documentação (HTML) e o arquivo de modelagem lógica do SQL Power Architect estão disponíveis no diretório `modeling`.

### Apache Hop
Para a instalação do Apache Hop em Docker, acesse o diretório `hop` e execute o comando `docker compose -f docker-compose.yaml up -d`

Isso vai levantar um container Docker com Apache Hop, uma ferramenta de ETL low code muito versátil e open source.

