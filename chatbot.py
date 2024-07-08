import os
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from chroma_connector import ChromaDBConnection
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
from meeting import schedule_meeting
from datetime import datetime

load_dotenv()

def detect_intent(user_input, groq_chat, system_prompt, memory):
    # Criar o prompt com a mensagem do sistema e novo mensagem do usuário
    messages = [
        SystemMessage(content=system_prompt),
        *memory.chat_memory.messages,
        HumanMessage(content=user_input)
    ]

    # Chamar o modelo de linguagem com o prompt
    response = groq_chat.invoke(messages)
    response_content = response.content.lower()

    # Verificar se a resposta sugere que o usuário quer agendar uma reunião
    if "agendar" in response_content or "marcar" in response_content:
        return True, response_content
    return False, response_content

def get_meeting_details():
    details = {}

    questions = [
        "Por favor, forneça um resumo para a reunião:",
        "Por favor, descreva a reunião:",
        "Por favor, forneça a data e hora de início (formato: YYYY-MM-DDTHH:MM:SS):",
        "Por favor, forneça a data e hora de término (formato: YYYY-MM-DDTHH:MM:SS):",
        "Por favor, forneça os e-mails dos participantes, separados por vírgula:"
    ]

    keys = ['summary', 'description', 'start_datetime', 'end_datetime', 'attendees']

    for i, question in enumerate(questions):
        user_input = input(question)

        # Validar e formatear datas e horas
        if keys[i] in ['start_datetime', 'end_datetime']:
            valid_format = False
            while not valid_format:
                try:
                    datetime_obj = datetime.strptime(user_input, '%Y-%m-%dT%H:%M:%S')
                    details[keys[i]] = datetime_obj.strftime('%Y-%m-%dT%H:%M:%S') # Formato desejado
                    valid_format = True
                except ValueError:
                    print("Formato de data errado")
                    user_input = input("Por favor, forneça a data e hora novamente (formato: YYYY-MM-DDTHH:MM:SS): ")
                    
            # Verificar que end_datetime não é anterior a start_datetime
            if keys[i] == 'end_datetime':
                start_datetime = datetime.strptime(details['start_datetime'], '%Y-%m-%dT%H:%M:%S')
                end_datetime = datetime_obj
                if end_datetime < start_datetime:
                    print("A data e hora de término não podem ser antes da data e hora de início.")
                    while end_datetime < start_datetime:
                        user_input = input("Por favor, forneça end_datetime novamente (formato: YYYY-MM-DDTHH:MM:SS): ")
                        try:
                            end_datetime = datetime.strptime(user_input, '%Y-%m-%dT%H:%M:%S')
                            if end_datetime >= start_datetime:
                                details['end_datetime'] = end_datetime.strftime('%Y-%m-%dT%H:%M:%S')
                        except ValueError:
                            print("Formato de data errado")
        else:
            details[keys[i]] = user_input
        if keys[i] == 'attendees':
            details[keys[i]] = [email.strip() for email in user_input.split(",")]

    return details

def main():
    groq_api_key = os.getenv('GROQ_API_KEY')
    model = "llama3-70b-8192"

    groq_chat = ChatGroq(
        api_key=groq_api_key,
        model=model,
    )

    print("Oi, tudo certo? Sou teu chatbot e estou aqui para te ajudar, o que você quer saber?")

    system_prompt = """
        Você é um assistente virtual que responde perguntas de um usuário.
        Você sabe respostas de diversos tamanhos, mas, se o cliente não especifica, você tem que dar respostas de tamanho médio.
        Se a pergunta não puder ser respondida de uma forma concisa, responda que não sei.
        Use o contexto fornecido para responder da melhor forma possível.
        Além de responder perguntas gerais, você também pode fornecer tutoriais passo a passo sobre como usar ferramentas internas da empresa, como plataformas de comunicação e sistemas de gerenciamento de projetos.
        Ferramentas específicas incluem Github, Vscode, Jira e Discord.
        Para cada ferramenta, forneça tutoriais sobre acesso, uso e/ou instalação.
        Além disso, você pode agendar reuniões de boas-vindas integrando-se com sistemas de calendário, como Google Calendar.
        As respostas tem que ser objetivas, sem dar detalhes sobre metadados ou informações que não sejam relevantes para o usuário.
        Você só pode responder perguntas sobre as ferramentas mencioandas, agendar reuniões e responder as perguntas das quias você
        tem contexto.
    """

    conversational_memory_length = 5

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        k=conversational_memory_length,
    )

    chroma_connector = ChromaDBConnection()
    
    programa = True
    
    while programa:
        user_input = input("O que você quer saber? Coloque 1 para sair\n")
        if user_input.lower() == '1':
            programa = False
        if user_input.lower() != '1':
            # Detectar a intenção do usuário
            intent, response_content = detect_intent(user_input, groq_chat, system_prompt, memory)

            if intent:
                print("Parece que você quer agendar uma reunião. Vamos coletar algumas informações.")

                # Coleta de detalhes da reunião através do chatbot
                meeting_details = get_meeting_details()

                try:
                    # Agendamiento de la reunión a través del chatbot
                    meeting_link = schedule_meeting(
                        meeting_details['summary'],
                        meeting_details['description'],
                        meeting_details['start_datetime'],
                        meeting_details['end_datetime'],
                        meeting_details['attendees']
                    )
                    print(f"Reunião agendada com sucesso: {meeting_link}")
                except Exception as e:
                    print(f"Ocorreu um erro ao agendar a reunião: {e}")
            
            else:
                results = chroma_connector.search(user_input, 7)
                if results and 'documents' in results:
                    faq_contexts = []
                    documents = results['documents']
                    for i, document in enumerate(documents[0]):
                        faq_contexts.append(f"Conteudo {i + 1}: {document}")
                        
                    combined_input = f"{user_input}\n\nContexto relevante:\n" + "\n".join(faq_contexts)

                else:
                    combined_input = f"{user_input}\n\nContexto relevante:\nNenhuma pergunta encontrada relacionada."
                
                chat_history = memory.chat_memory
                chat_messages = chat_history.messages

                # Convertir mensajes en el historial del chat a HumanMessage y AIMessage
                formatted_messages = []
                for message in chat_messages:
                    if isinstance(message, HumanMessage):
                        formatted_messages.append(HumanMessage(content=message.content))
                    elif isinstance(message, AIMessage):
                        formatted_messages.append(AIMessage(content=message.content))

                # Crear el prompt con el mensaje del sistema, mensajes del historial y nuevo mensaje del usuario
                messages = [
                    SystemMessage(content=system_prompt),
                    *formatted_messages,
                    HumanMessage(content=combined_input)
                ]

                # Llamar al modelo de lenguaje con el prompt
                response = groq_chat.invoke(messages)
                
                # Asegurarse de que response sea una lista y obtener el primer mensaje AI
                response_content = response.content

                print("Chatbot:", response_content)

                # Guardar contexto en la memoria
                memory.save_context({"input": combined_input}, {"output": response_content})



if __name__ == "__main__":
    main()
