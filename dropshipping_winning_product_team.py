#### SETUP LLM ####

import os
#os.environ["OPENAI_API_KEY"] = "Your Key"

from dotenv import load_dotenv

load_dotenv()

#### SETUP LLMS ####
# OLLAMA OR GROQ (uncomment in .env file)
# important!!! : for GROQ the field "tools" is not supported so we need to use tools of llms with another llm setup openai or ollama
OPENAI_API_BASE=os.getenv("OPENAI_API_BASE")
OPENAI_MODEL_NAME=os.getenv("OPENAI_MODEL_NAME")  # Adjust based on available model
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

# Or just OLLAMA using langchain if using GROQ for the crew manager as GROQ doesn't support the field "tools" of the agents
from langchain_community.llms import Ollama

ollama_llm = Ollama(model="mistral:7b")

# LMSTUDIO
#OPENAI_API_BASE="http://localhost:1235/v1"
#OPENAI_MODEL_NAME=NA # no need model to be loaded in the webui
#OPENAI_API_KEY=NA # no need freee frreeeeeee freeeeeeeeeeeeeeee

# so need to create a client for ollama or lmstudio as it mimics openai endpoint logic already
# but if you want you can create client as crewai is langchain compatible using langchian imports of those like : from langchain_community.llms import Ollama, from langchain_community.llms import LlamaCpp ...


### OPTION TO HAVE HUMAN INTERACTION IN THE CREW PROCESS ####
#from langchain.agents import load_tools
#human_tools = load_tools(["human"])
# then when creating an agent you pass in the human tool to have human interact at that level. eg:
#digital_marketer = Agent(
  #role='...',
  #goal='...',
  #backstory="""...""",
  #verbose=..., # True or False
  #allow_delegation=...,
  #tools=[search_tool]+human_tools # Passing human tools to the agent
  #max_rpm=..., # int
  #max_iter=..., # int
  #llm=...
#)


#### SETUP TOOLS FOR AGENTS TO USE ####
from langchain_community.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()


#### AGENTS DEFINITION ####

from crewai import Agent

# Topic for the crew run
topic = " 'Dropshipping winning product' "

# Creating a senior digital marketer agent with memory and verbose mode
digital_marketer = Agent(
  role='Senior Digital Marketer',
  goal=f'Find the best strategy to be profitable in {topic}',
  verbose=True,
  memory=True,
  backstory="""Having more than 30 years experience in online sale and profit making millions online.
   Your are able to compare and find best potential product to sell online by analysing trends and price change and gapes in the market. you always find winning products that have a impressive first impression effect. People always buy your products after few seconds seeing it and they are satisfied. You are one of the world leaders in online winning product sales.""",
  tools=[search_tool],
  allow_delegation=True,
  llm=ollama_llm,
  max_rpm=2,
  max_iter=3,
)

# Creating a writer agent with custom tools and delegation capability
writer = Agent(
  role='Writer',
  goal=f'Narrate compelling stories about products trends online and their value to users about the {topic} of the moment.',
  verbose=True,
  memory=True,
  backstory="""With a flair for simplifying complex topics, you craft
  engaging narratives that captivate and educate, bringing new
  discoveries to light in an accessible manner. You have the goal to convert reader to online purchaser. After having red your article they should be convinced in where is the value for them. You push people to make compulsive purchases.""",
  tools=[search_tool],
  allow_delegation=True,
  llm=ollama_llm,
  max_rpm=2,
  max_iter=3,
)

# A user persona that reads articles and make purchasing decisions based ont he content of the article and being very critical and hard to convince.
critical_buyer_persona = Agent(
  role='Critical buyer persona',
  goal=f'Provides critical view on the potential for buying those products online from a dropshipping store {topic}',
  verbose=True,
  memory=True,
  backstory="""You reading articles and making online purchasing decision based on their persuasiveness and value for you in your life. You are looking for a product that appeal to you. You have 40 years old and you are an employee in a makeup store. You have 2 children. one boy of 7 years old and a girl of 15 years old. You are single mother and thinking about your future. You like reading articles and make purchasing decisions but you are not easy to convince.""",
  tools=[search_tool],
  allow_delegation=False,
  llm=ollama_llm,
  max_rpm=2,
  max_iter=3,
)

# custom values can be added to agents: allow_delegation (ability to delegate tasks or ask questions), max_rpm (rate limiting request to llm), verbose (True to have logs of agent interactions), max_iter (maximum iterations to avoid loops and have best answer after the number of defined iterations of the task). eg:
#max_rpm=10, # Optinal: Limit requests to 10 per minute, preventing API abuse
#max_iter=5, # Optional: Limit task iterations to 5 before the agent tried to gives its best answer

#### DEFINE TASKS ####

from crewai import Task

# Research Wining Product task
digital_marketing_task = Task(
  description=f"""Identify the next big trend in {topic}.
  Focus on identifying pros and cons and the overall narrative.
  Your final report should clearly articulate the key points,
  its market opportunities, and potential risks.""",
  expected_output='A comprehensive 3 paragraphs long report on the potential dropshipping winning products.',
  tools=[search_tool], # if process=Process.sequential can put tool here as well but if it is hierarchical put it only at the agent level not task level for fluidity
  agent=digital_marketer,
)

# Writing task with language model configuration
write_task = Task(
  description=f"""Compose an insightful article on {topic}.
  Focus on the latest trends and how it's impacting the industry.
  This article should be easy to understand, engaging, and positive. Use AIDA technique of writing to convince readers. It is mor elike a sales pages and should tackle potential buyers questions.""",
  expected_output=f'A SEO optimized article with: An engaging title,  4 paragraph article on {topic} with sub-titles, 3 questions for the FAQ with answers, 3 hashtags amd 10 comma separated keywords. All fromated as markdown. with one image prompt suggestion to create an image to illustrate this article using llm image generators.',
  tools=[search_tool], # if process=Process.sequential can put tool here as well but if it is hierarchical put it only at the agent level not task level for fluidity
  agent=writer,
  async_execution=False,
  output_file='dropshipping_winning_product_article.md'  # Example of output customization
)

# Persona reading of the article taks and purchasing decision
critical_buyer_persona_task = Task(
  description=f""" read the article presented and provide insighful decision on why you will buy or not one or all the product suggested. You are critical and provide your reasons about those {topic}.""",
  expected_output=f'Write a report in your final purchasing decisona fter having red the article and your detailed motivation. Make sure that it is well structured and easy to understand for people who are not expert like you in online purchase.',
  tools=[search_tool], # if process=Process.sequential can put tool here as well but if it is hierarchical put it only at the agent level not task level for fluidity
  agent=writer,
  async_execution=False,
  output_file='persona_final_decision_and_motivations.md'  # Example of output customization
)




#### COMBINE THE AGENT AND SET WORKFLOW ####

from crewai import Crew, Process

## PROCESS SEQUENTIAL
# Forming the tech-focused crew with enhanced configurations, this config for process=Process.sequential
#crew = Crew(
  #agents=[digital_marketer, writer],
  #tasks=[digital_marketing_task, write_task],
  #process=Process.sequential,  # Here tasks are done in order so agent one do his job and the next agent is waiting for the output to work with it and do his task
  #verbose=2, # here it is a number not like the other ones with True or False, it is the level of logs
#)..]

# PROCESS HIERARCHICAL (here the manager handles the interaction and the defined agents crew, liek a 'judge' and decider)
# This config for the crew for process=PRocess.hierarchical (so with a manager that handles the other agents, we need to set an llm also for the manager and tools have to be at agent level and not task level)

from langchain_openai import ChatOpenAI

project_crew = Crew(
  tasks=[digital_marketing_task, write_task, critical_buyer_persona_task],  # Tasks to be delegated and executed under the manager's supervision. they use ollama (mistral:7b)
  agents=[digital_marketer, writer, critical_buyer_persona],
  manager_llm=ChatOpenAI(temperature=0.1, model="mixtral-8x7b-32768", max_tokens=1024),  # Defines the manager's decision-making engine, here it is openai but use the custom llm you want . here uses Groq (mixtral-8x7b-32768)
  process=Process.hierarchical,  # Specifies the hierarchical management approach
  verbose=2,
)


### START THE TEAM WORK ####

# Starting the task execution process with enhanced feedback
# result = crew.kickoff()
result = project_crew.kickoff()
print(result)







