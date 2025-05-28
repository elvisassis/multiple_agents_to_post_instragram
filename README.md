# 🤖 Sistema de Criação de Posts com Múltiplos Agentes de IA

Projeto desenvolvido durante a **Imersão Alura**, explorando o poder do **Gemini Console** para automatizar a criação de conteúdo para redes sociais com múltiplos agentes inteligentes.

---

## 🚀 Visão Geral

Este sistema utiliza **4 agentes de IA**, cada um com uma função específica, para criar automaticamente posts otimizados para o Instagram com base em tendências e lançamentos recentes sobre um tópico.

---

## 🧠 Arquitetura de Agentes

### 1. 🔍 Agente Buscador de Notícias
- **Função:** Pesquisa no Google os lançamentos mais recentes e relevantes sobre um tópico.
- **Modelo:** `gemini-2.0-flash`
- **Ferramentas:** `google_search`

### 2. 📋 Agente Planejador de Conteúdo
- **Função:** Analisa os lançamentos encontrados, realiza novas buscas e monta um plano estratégico de conteúdo.
- **Modelo:** `gemini-2.0-flash`
- **Ferramentas:** `google_search`

### 3. ✍️ Agente Redator de Post
- **Função:** Cria um rascunho engajador e informativo do post para Instagram, baseado no plano criado.
- **Modelo:** `gemini-2.0-flash`

### 4. 🛠️ Agente Revisor de Qualidade
- **Função:** Revisa o texto do post com foco em clareza, correção e tom adequado ao público jovem.
- **Modelo:** `gemini-1.5-pro`

---

## 📦 Como Funciona

```text
TÓPICO → Buscador → Planejador → Redator → Revisor → ✅ Post Final Pronto!
```

1. O usuário insere um tópico de interesse.
2. O **Agente Buscador** localiza os lançamentos mais quentes.
3. O **Agente Planejador** elabora um plano estratégico para o conteúdo.
4. O **Agente Redator** escreve o post.
5. O **Agente Revisor** faz o polimento final.

---

## 🛠️ Tecnologias Utilizadas

- **[Gemini Console](https://aistudio.google.com/)** (modelos Gemini 2.0 e 1.5)
- **Python 3.x**
- **Ferramentas de busca integradas com IA**
- **Prompt Engineering para orquestração de agentes**

---

## 📸 Exemplo de Uso

```bash
❓ Por favor, digite o TÓPICO sobre o qual você quer criar o post de tendências: inteligência artificial
```

O sistema irá:

- Buscar notícias atuais sobre IA
- Planejar os tópicos mais relevantes
- Redigir um post criativo
- Revisar e entregar o conteúdo final pronto para publicação

---

## ✨ Resultado Esperado

Um post otimizado e informativo como este:

> A IA não para de evoluir! Conheça os 3 lançamentos mais quentes do mês e como eles estão moldando o futuro da tecnologia. 🚀  
> Da geração de vídeos à IA multimodal — tudo explicado de forma simples e com exemplos práticos.  
>  
> #InteligenciaArtificial #TechTrends #IAemAlta

---

## 📌 Requisitos

- Conta no [Gemini AI Studio](https://aistudio.google.com/)
- Configuração de agentes e permissões de busca
- Ambiente Python configurado com suporte a chamadas do console

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se livre para abrir issues ou pull requests.

---

## 📄 Licença

Este projeto é licenciado sob a [MIT License](LICENSE).

---

Feito com 💚 durante a [Imersão Alura](https://www.alura.com.br/)
