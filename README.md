# Agente de IA para Agendar Reuniões e Responder FAQs

Este projeto é um agente de IA desenvolvido para responder perguntas frequentes (FAQs), fornecer tutoriais sobre ferramentas internas da empresa e agendar reuniões de boas-vindas através da integração com o Google Calendar. O programa funciona diretamente no terminal, então para rodar ele é tão simples como rodar o arquivo chatbot.py

## Tecnologias Utilizadas

- **Python 3.x**
- **Google APIs**
- **ChromaDB**
- **LangChain**
- **Groq**

## Chave do Groq

Para poder usar é necessario que você tenha uma chave e colocar dita chave no arquivo .env, em GROQ_API_KEY. Para conseguir a chave entra no groqcloud, cria uma conta e vai na parte onde estão os API keys. Nessa página existe um botão que diz "Create API key". É só colocar um nome para a chave e copiar a chave gerada. Finalmente a chave gerada é colocada no arquivo .env, como foi explicado anteriormente. 

### Como Gerar Credenciais OAuth2 para o Projeto

Para usar a API do Google (como é neste caso, Google Calendar API) com seu projeto, siga os passos abaixo para gerar suas próprias credenciais OAuth2:

1. **Criar um Projeto no Google Cloud:**
   - Acesse a [Console de Desenvolvedores do Google](https://console.cloud.google.com/).
   - Crie um novo projeto ou selecione um projeto existente onde deseja habilitar a API.

2. **Habilitar a API Necessária:**
   - No painel de navegação esquerdo, vá para "Biblioteca".
   - Procure e selecione a API que seu projeto necessita (por exemplo, "Google Calendar API").
   - Clique em "Habilitar".

3. **Configuração da Tela de Consentimento OAuth (OAuth Consent Screen):**
   - Antes de criar as credenciais, é necessário configurar a Tela de Consentimento OAuth:
     - No painel de navegação esquerdo, vá para "Configuração".
     - Selecione "Tela de Consentimento OAuth".
     - Preencha os campos obrigatórios, como nome do aplicativo, email de suporte e domínios autorizados.
     - Coloque a API do Google Calendar nas permissões.
     - Salve as alterações.

4. **Configurar Credenciais OAuth2:**
   - No painel de navegação esquerdo, vá para "Credenciais".
   - Clique em "Criar credenciais" e selecione "ID do cliente OAuth".
   - Escolha o tipo de aplicação adequado para seu caso (Neste caso seria Aplicação instalada para desenvolvimento local).
   - Preencha as informações necessárias, incluindo o nome do cliente e os URIs de redirecionamento (exemplo: `http://localhost` para desenvolvimento local).

5. **Baixar o Arquivo `credentials.json`:**
   - Após criar as credenciais, clique em "Baixar JSON" na linha correspondente às credenciais recém-criadas.
   - Este arquivo `credentials.json` contém as informações necessárias para autenticar suas solicitações à API do Google.

6. **Configurar no seu Projeto:**
   - Coloque o arquivo `credentials.json` no mesmo diretório dos arquivos do projeto.

Certifique-se de manter o arquivo `credentials.json` seguro e não compartilhá-lo publicamente para proteger suas credenciais de acesso.


## Dependências

Para instalar todas as dependências necessárias, utilize o arquivo `requirements.txt` que tem o seguinte conteúdo:

```plaintext
google-auth
google-auth-oauthlib
google-auth-httplib2
google-api-python-client
google.oauth2
chromadb
sentence-transformers
psycopg2-binary
python-dotenv
langchain
langchain_groq

Utilize pip install -r requirements.txt

Em relação com os dados, eles se encontram na pasta chromaData, então não vai ser necessario entrar em PostgreSQL, que é o lugar onde eles estavam originalmente, salvo que de um erro ou seja apagado o que esta nessa pasta mencionada anteriormente.

Caso isso aconteça, voçê tera que restaurar em postgreSQL o arquivo de backup e trocar os dados que estão no arquivo .env em relação com o nome e senha para o seu respectivo caso.

