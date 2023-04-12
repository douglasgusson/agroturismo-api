# Agroturismo API

## Ambiente virtual:

### Criação do ambiente virtual:

```bash
python -m venv .venv
```

### Ativação do ambiente virtual:

```bash
source .venv/bin/activate
```

## Instalação das dependências:

```bash
pip install -r requirements.txt
```

## Execução do projeto:

```bash
uvicorn agroturismo_api.main:app --reload
```

## Execução com Docker:

### Build da imagem:

```bash
docker build -t agroturismo-api .
```

### Execução da imagem:

```bash
docker run -p 8000:8000 agroturismo-api
```
