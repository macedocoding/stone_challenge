# Desafio técnico Stone

Desafio técnico relativo ao processo seletivo da empresa Stone para o cargo de estagiário de Engenharia de Dados.
A disponibilização dos serviços utilizados será feita por meio de Docker e serviços em nuvem do provedor GCP, portanto é fundamental a instalação do Docker Engine e Docker Compose v2, além de ter uma conta na Google Cloud Provider com um projeto previamente criado e um bucket no Google Storage.

[Instalação Docker Engine/Docker Compose](https://docs.docker.com/engine/install/)

## Instalação e configuração do ambiente

### Ambiente Python
Após clonar o repositório em sua máquina local, acesse diretório e crie um ambiente virtual Python com o comando `python -m .venv venv`.
Após isso, [ative o ambiente](https://docs.python.org/3/library/venv.html) conforme seu sistema operacional.

### Requerimentos
As bibliotecas Python utilizadas foram listadas no arquivo `requirements.txt` e podem ser instaladas através do comando `$ pip install -r requirements.txt`.

### gcloud
É necessária a instalação da Google Cloud CLI para facilitarmos o processo de autenticação local.
Para isso, é só seguir o [tutorial](https://cloud.google.com/sdk/docs/install?hl=pt-br) para seu sistema operacional.

### Autenticação GCP
Para esta solução, utilizaremos a chave de autenticação JSON da sua conta GCP que deve ser baixada e salva no endereço seguinte (a partir do diretório clonado) `stone_challenge/hop/ENV/key.json`.
Além disso, a partir de seu terminal, digite `$ gcloud auth login` e siga as instruções, lembrando que já deve ter em mãos o ID do projeto criado na cloud.

### Criação dos volumes e redes no Docker
Para garantir a persistência dos dados, devemos criar volumes lógicos que serão mapeados dentro do container de cada serviço, já as redes garantem a comunicação entre os containeres durante a execução do pipeline.

Para criarmos os volumes, digite:
```
$ docker volume create pg_volume
$ docker volume create hop_volume
```

Para criarmos as redes, digite:
```
$ docker network create pg_network
$ docker network create hop_network
```

## Solução OLTP local em Postgres
Após criar um ambiente virtual Python, acesse a pasta `postgres` e rode o comando `docker compose -f docker-compose.yaml up -d`.

Isso vai levantar um container Docker Postgres e executará as queries de criação das tabelas em segundo plano.
Lembrando que a documentação (HTML) e o arquivo de modelagem lógica do SQL Power Architect estão disponíveis no diretório `modeling`.

## Apache Airflow
Apache Airflow já foi previamente instalado com o comando `$ pip install -r requirements.txt`, porém é importante apontar a variável de ambiente `AIRFLOW_HOME` para o diretório `airflow` (que ja possui um arquivo de configuração e a dag) na raíz do projeto através do comando `$ export AIRFLOW_HOME=projeto/clonado/airflow`. or último, digite `$ airflow standalone` para inicializar o banco de dados, criar um usuário e iniciar todos os componentes do Airflow.

A interface gráfica pode ser acessada através de um navegador, digitando-se `localhost:8081` na barra de endereço. O usuário padrão é `admin` e a senha é fornecida no próprio terminal ao final da inicialização.

Para mais detalhes, acesse o [guia de início rápido do Airflow](https://airflow.apache.org/docs/apache-airflow/stable/start.html).

## Apache Hop Web
Para a instalação do Apache Hop Web em Docker, acesse o diretório `hop` e execute o comando `docker compose -f docker-compose.yaml up -d`

Isso vai levantar um container Docker com Apache Hop na versão Web, uma ferramenta de ETL low code muito versátil e open source onde serão feitas as transformações necessárias nos dados e sua persistência no bucket.

### ETL no Apache Hop Web
Para acessar a interface gráfica do Apache Hop Web, digite em seu navegador `localhost:8080`.
Após isso, feche a tela de boas vindas e selecione o projeto `stone_challenge` na parte superior esquerda da aplicação. Automaticamente, o ambiente `DEV` com as configurações necessárias, como conexão com Postgres e Storage será selecionado automaticamente.
Após isso, clique em `Open` no canto superior esquerdo, e selecione `ETL/workflow.hwf`.
Por último clique no pequeno triângulo no canto superior esquerdo da tela para iniciar a execução do workflow.

## Data Warehouse no Bigquery
Com os arquivos parquet salvos no seu bucket, representando tabelas de um banco de dados desnormalizado e otimizado para queries de recuperação de dados, é possível acessar o Bigquery e criar tabelas a partir de cada um desses arquivos. Temos, então um protótipo de Data Warehouse que pode ser acessado por diversas ferramentas de Analytics para análise de tomada de decisão.

## Metabase
Uma excelente ferramenta de self-service BI open source é o Metabase, que possui integração nativa com Bigquery e roda no navegador.
Para levantarmos um container básico do Metabase é só digitar `docker run -d -p 3000:3000 --name metabase metabase/metabase-enterprise` e, em seguida, acessar do seu navegador `localhost:3000`.
Quando acessar a interface gráfica, basta seguir os passos para criar uma conta e conectar ao seu bigquery de forma muito compreensível.

# Futuras melhorias
Uma abordagem mais integrada ao Airflow pode ser mais interessante para o gerenciamento dos serviços que compõe o pipeline.