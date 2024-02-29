### CrewAI and Groq

** stack **
- Linux ubuntu-22.04
- Openai
- Groq
- Ollama
- LangChain (Amazing librairy and amazing developer team which makes us like the usefulness of Python coding in an easy understandable way)
- CrewAI (Wrapper and base of everything. Very clever from their developer. Apache License)

** This application has the boiler plate for agent to work ona  task in a hierachical process with a manager or in a sequential process without manager. **

1- Intall requirements.txt : ```python pip install -r requriements.txt```

2- create a .env file for the envrionement variabled see the example_for_secrets.txt file and create your .env file like that providing you the ability to switch for the LLM engine or API to use

3- choose if using Ollama, LMStudio, Openai, Groq ....

4- use the script file to create your agents, then create your set of tasks. you can have tools funtions set before that has helper functions. Don't ask the LLM to use two parameter, it works better with one parameter only to provide to the function tool. Make the LLM life easy for better performance and design your function to take one argument only or no argument. Here we use the documentation example of DuckDuckGo_Search

5- Create your crew with agents, tasks and manager (if hierarchical process method choosen)

6- run the app

7- files are going to be output for the report on the agents work


# ** options **
See the comments to have have more ability to design and customize your agent
You can intreoduce human intaraction in the process by adding it the tools


# notice
Groq doesn't accept some fields like here for example the important one  'tools' so you need to use another llm API for that.
Here in the hierarchical example we use Groq only for the manager and Ollama for the agents llms


It is an Apache2.0 license project, therefore...
... Enjoy!!!
Diallo S. (Creditizens)
