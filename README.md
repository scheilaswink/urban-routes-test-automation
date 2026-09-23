### Como executar

1. Criar e ativar o ambiente virtual (na raiz do projeto):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instalar as dependências:

```bash
pip install -r requirements.txt
```

3. Atualizar `URBAN_ROUTES_URL` em `data.py` com uma URL de container ativa (esses containers expiram — pegue uma nova na plataforma se o teste falhar com erro de conexão).

4. Rodar toda a suíte de testes:

```bash
pytest main.py -v
```

Para rodar um teste específico:

```bash
pytest main.py::TestUrbanRoutes::test_select_plan -v
```

### Diretrizes de nomenclatura de código

- **Nomes de variáveis** são escritos em `snake_case` e descrevem sua finalidade;
- **Constantes** são escritas em maiúsculas;
- **Comentários** são usados para explicar blocos importantes de código;
- A **organização do código** é modular, com blocos de código reutilizáveis importados para onde for necessário;
- Evite funções de espera (`wait`) desnecessárias que fazem com que o teste seja executado por mais tempo do que o necessário;
- Siga uma **convenção de nomenclatura** para títulos de teste que começam com `test\_` e fornece uma descrição clara do cenário de teste. Os títulos dos testes são fornecidos no resumo.
