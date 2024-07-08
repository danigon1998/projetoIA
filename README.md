# Agente de IA para Agendar Reuniões e Responder FAQs

Este projeto é um agente de IA desenvolvido para responder perguntas frequentes (FAQs), fornecer tutoriais sobre ferramentas internas da empresa e agendar reuniões de boas-vindas através da integração com o Google Calendar. O programa funciona diretamente no terminal, então para rodar ele é tão simples como rodar o arquivo chatbot.py

## Tecnologias Utilizadas

- **Python 3.x**
- **Google APIs**
- **ChromaDB**
- **LangChain**
- **Groq**

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

