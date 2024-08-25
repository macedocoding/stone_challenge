# Desafio técnico Stone

Desafio técnico relativo ao processo seletivo da empresa Stone para o cargo de estagiário de Engenharia de Dados.
A disponibilização dos serviços utilizados será feita por meio de containeres Docker, portanto é fundamental a instalação do Docker Engine e Docker Compose v2.

[Instalação Docker Engine/Docker Compose](https://docs.docker.com/engine/install/)

## Instalação e configuração do ambiente

### Ambiente Python
Após clonar o repositório em sua máquina local, acesse diretório e crie um ambiente virtual Python com o comando `python -m .venv venv`.
Após isso, [ative o ambiente](https://docs.python.org/3/library/venv.html) conforme seu sistema operacional.

### Requerimentos
As bibliotecas Python utilizadas foram listadas no arquivo `requirements.txt` e podem ser instaladas através do comando `$ pip install -r requirements.txt`.

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

### Solução OLTP local em Postgres
Após criar um ambiente virtual Python, acesse a pasta `postgres` e rode o comando `docker compose -f docker-compose.yaml up -d`.

Isso vai levantar um container Docker Postgres e executará as queries de criação das tabelas.
Lembrando que a documentação (HTML) e o arquivo de modelagem lógica do SQL Power Architect estão disponíveis no diretório `modeling`.

### Apache Hop
Para a instalação do Apache Hop em Docker, acesse o diretório `hop` e execute o comando `docker compose -f docker-compose.yaml up -d`

Isso vai levantar um container Docker com Apache Hop, uma ferramenta de ETL low code muito versátil e open source.

### Apache Airflow
Apache Airflow já foi previamente instalado com o comando `$ pip install -r rquirements.txt`, porém é importante apontar a variável de ambiente `AIRFLOW_AIRFLOW` para o diretório `airflow` na raíz do projeto através do comando `$ export AIRFLOW_HOME=./airflow`.Por último, digite `$ airflow standalone` para inicializar o banco de dados, criar um usuário e iniciar todos os componentes do Airflow.

A interface gráfica pode ser acessada através de um navegador, digitando-se `localhost:8080` na barra de endereço. O usuário padrão é `admin` e a senha é fornecida no próprio terminal no final da inicialização.

Para mais detalhes, acesse o [guia de início rápido do Airflow](https://airflow.apache.org/docs/apache-airflow/stable/start.html).

#### Configurações Apache Airflow
Algumas configurações precisam ser feitas no arquivo `airflow/airflow.cfg` a fim de facilitarmos a execução das tasks. Para isso, abra o arquivo de configuração citado, procure pelas variáveis de ambiente abaixo e altere seus valores:

```
load_examples = False
min_file_process_interval = 5
expose_config = True
dag_dir_list_interval = 20
```
Após isso, reinicie o Apache Airflow.

