import os
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types  # Para criar conteúdos (Content e Part)
from datetime import date
import textwrap # Para formatar melhor a saída de texto
from IPython.display import display, Markdown # Para exibir texto formatado no Colab
import requests # Para fazer requisições HTTP
import warnings

warnings.filterwarnings("ignore")

os.environ["GOOGLE_API_KEY"] = "AIzaSyCTrRcIxkGdi9-SohFNXuDMNte8HUvuU5o"

# Função auxiliar que envia uma mensagem para um agente via Runner e retorna a resposta final
def call_agent(agent: Agent, message_text: str) -> str:
    # Cria um serviço de sessão em memória
    session_service = InMemorySessionService()
    # Cria uma nova sessão (você pode personalizar os IDs conforme necessário)
    session = session_service.create_session(app_name=agent.name, user_id="user1", session_id="session1")
    # Cria um Runner para o agente
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    # Cria o conteúdo da mensagem de entrada
    content = types.Content(role="user", parts=[types.Part(text=message_text)])

    final_response = ""
    # Itera assincronamente pelos eventos retornados durante a execução do agente
    for event in runner.run(user_id="user1", session_id="session1", new_message=content):
        if event.is_final_response():
          for part in event.content.parts:
            if part.text is not None:
              final_response += part.text
              final_response += "\n"
    return final_response

# Função auxiliar para exibir texto formatado em Markdown no Colab
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

##########################################
# --- Agente 1: Buscador de Notícias --- #
##########################################
def agente_buscador(topico, data_de_hoje):
    buscador = Agent(
        name="agente_buscador",
        model="gemini-2.0-flash",
        instruction="""
        Você é um assistente de pesquisa, e a sua tarefa é usar a ferramenta de busca do Google (google_search)
        para recupear as últimas noticias de lançamento muito relevantes sobre o tópico abaixo.
        Foque em no máximo 5 lançamentos relevantes, com base no quantidade e entusiasmo das noticias sobre ele.
        Se um tema tiver poucas notícias ou reações entusiasmadas, é possivel que ele não seja tão relevante assim e
        pode ser subistituido por outro que tenha mais.
        Esses lançamentos relevantes devem ser atuais, de no máximo um mês antes da data de hoje.
        """,
         description="Agente que busca notícias sobre o tópico indicado no Google",
         tools=[google_search],
    )

    entrada_do_agente_buscador = f"Tópico: {topico}\nData de hoje: {data_de_hoje}"
    # Executa o agente
    lancamentos_buscados = call_agent(buscador, entrada_do_agente_buscador)
    return lancamentos_buscados

################################################
# --- Agente 2: Planejador de posts --- #
################################################
def agente_planejador(topico, lancamentos_buscados):
    planejador = Agent(
        name="agente_planejador",
        model="gemini-2.0-flash",
        # Inserir as instruções do Agente Planejador #################################################
        instruction="""
        Você é um planejado de conteúdo especialista em redes socias, Com base na lista de
        lançamentos mais recentes e relevantes buscador, você deve:
        usar a ferramenta de busca do Google (google_search) para criar um plano sobre
        quais os pontos mais relevantes que poderiamos abordar em um post sobre
        cada um deles. Você tambêm deve usar o Google (google_search) para encontrar mais
        informações.
        Ao final, você irá escolher o tema mais relevante entre eles com base nas suas pesquisas
        e retornar esse tema, seus pontos mais relevantes, e plano com os assuntos a serem abordados
         no posto que será escrito posteriormente.
        """,
        description="Agente que planeja posts",
        tools=[google_search]
    )

    entrada_do_agente_planejador = f"Tópico:{topico}\nLançamentos buscados: {lancamentos_buscados}"
    # Executa o agente
    plano_do_post = call_agent(planejador, entrada_do_agente_planejador)
    return plano_do_post

######################################
# --- Agente 3: Redator do Post --- #
######################################
def agente_redator(topico, plano_de_post):
    redator = Agent(
        name="agente_redator",
        model="gemini-2.0-flash",
        instruction="""
            Você é um Redator Criativo especializado em criar posts virais para redes sociais.
            Você escreve posts para a empresa Alura, a maior escola online de tecnologia do Brasil.
            Utilize o tema fornecido no plano de post e os pontos mais relevantes fornecidos e, com base nisso,
            escreva um rascunho de post para Instagram sobre o tema indicado.
            O post deve ser engajador, informativo, com linguagem simples e incluir 2 a 4 hashtags no final.
            """,
        description="Agente redator de posts engajadores para Instagram"
    )
    entrada_do_agente_redator = f"Tópico: {topico}\nPlano de post: {plano_de_post}"
    # Executa o agente
    rascunho = call_agent(redator, entrada_do_agente_redator)
    return rascunho

##########################################
# --- Agente 4: Revisor de Qualidade --- #
##########################################
def agente_revisor(topico, rascunho_gerado):
    revisor = Agent(
        name="agente_revisor",
        model="gemini-1.5-pro",
        instruction="""
            Você é um Editor e Revisor de Conteúdo meticuloso, especializado em posts para redes sociais, com foco no Instagram.
            Por ter um público jovem, entre 18 e 30 anos, use um tom de escrita adequado.
            Revise o rascunho de post de Instagram abaixo sobre o tópico indicado, verificando clareza, concisão, correção e tom.
            Se o rascunho estiver bom, responda apenas 'O rascunho está ótimo e pronto para publicar!'.
            Caso haja problemas, aponte-os e sugira melhorias.
            """,
        description="Agente revisor de post para redes sociais."
    )
    entrada_do_agente_revisor = f"Tópico: {topico}\nRascunho: {rascunho_gerado}"
    # Executa o agente
    texto_revisado = call_agent(revisor, entrada_do_agente_revisor)
    return texto_revisado

data_de_hoje = date.today().strftime("%d/%m/%Y")

print("🚀 Iniciando o Sistema de Criação de Posts para Instagram com 4 Agentes 🚀")

# --- Obter o Tópico do Usuário ---
topico = input("❓ Por favor, digite o TÓPICO sobre o qual você quer criar o post de tendências: ")

# Inserir lógica do sistema de agentes ################################################
if not topico:
  print("Você esqueceu de digitar o tópico sobre o qual você quer criar o post!")
else:
  print(f"Maravilha! Você então criar o post sobre novidades em: {topico}")

  lancamentos_buscados = agente_buscador(topico, data_de_hoje)
  print("\n--- Resultado do Agente 1 (Buscador) ---\n")
#   display(to_markdown(lancamentos_buscados))
  print(lancamentos_buscados)
  print("--------------------------------------------------------")

  plano_de_post = agente_planejador(topico, lancamentos_buscados)
  print("\n--- Resultado do Agente 2 (Planejador) ---\n")
#   display(to_markdown(plano_de_post))
  print(plano_de_post)    
  print("--------------------------------------------------------")

  rascunho_de_post = agente_redator(topico, plano_de_post)
  print("\n--- Resultado do Agente 3 (Redator) ---\n")
#   display(to_markdown(rascunho_de_post))
  print(rascunho_de_post)
  print("--------------------------------------------------------")

  post_final = agente_redator(topico, rascunho_de_post)
  print("\n--- Resultado do Agente 4 (Revisor) ---\n")
#   display(to_markdown(post_final))
  print(post_final) 
  print("--------------------------------------------------------")