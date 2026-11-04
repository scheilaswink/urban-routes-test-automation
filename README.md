# Urban Routes — Automação de Testes E2E

Projeto da formação **Analista de QA da TripleTen**: automação de testes de ponta a ponta do fluxo de pedido de táxi do aplicativo web **Urban Routes**.

## 🧪 Cenários automatizados

| Teste | O que valida |
|---|---|
| `test_set_route` | Preenchimento dos endereços de origem e destino |
| `test_select_plan` | Seleção da tarifa Comfort |
| `test_fill_phone_number` | Cadastro do telefone com código de confirmação |
| `test_fill_card` | Adição de cartão de pagamento |
| `test_comment_for_driver` | Mensagem para o motorista |
| `test_order_blanket_and_handkerchiefs` | Pedido de cobertor e lenços |
| `test_order_2_ice_creams` | Pedido de 2 sorvetes |
| `test_car_search_model_appears` | Exibição do modal de busca de carro |

## 🛠️ Tecnologias

Python · Selenium WebDriver · Pytest · Page Object Model · Chrome DevTools Protocol

## 📁 Estrutura

- `main.py` — classe de testes `TestUrbanRoutes`
- `pages.py` — Page Object `UrbanRoutesPage`, com localizadores e ações da página
- `helpers.py` — funções auxiliares (ex.: captura do código de confirmação pelos logs de rede)
- `data.py` — dados de teste e URL do servidor

## ▶️ Como executar

1. Crie e ative o ambiente virtual (na raiz do projeto):
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Atualize `URBAN_ROUTES_URL` em `data.py` com uma URL de servidor ativa (os servidores expiram; gere uma nova na plataforma se o teste falhar com erro de conexão).
4. Rode a suíte de testes:
   ```
   pytest main.py -v
   ```
   Para rodar um teste específico:
   ```
   pytest main.py::TestUrbanRoutes::test_select_plan -v
   ```

## 📐 Boas práticas aplicadas

- Nomes de variáveis em `snake_case`, descrevendo sua finalidade; constantes em maiúsculas
- Código modular, com blocos reutilizáveis no padrão Page Object Model
- Esperas explícitas em vez de pausas fixas, para testes mais rápidos e estáveis
- Títulos de teste iniciados por `test_`, com descrição clara do cenário

## 👩‍💻 Autora

Scheila Schwede Wink — [LinkedIn](https://www.linkedin.com/in/scheila-schwede-wink/)
