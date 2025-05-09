import os
from langchain import hub
from langchain.agents import create_react_agent
from langchain.agents import AgentExecutor
from langchain_deepseek import ChatDeepSeek
from langchain_experimental.tools import PythonREPLTool
import dotenv
dotenv.load_dotenv()

llm = ChatDeepSeek(model="deepseek-chat",
                   api_key=os.getenv("DEEPSEEK_API_KEY"))

tools = [PythonREPLTool()]


def code_execution_tool() -> str:
    """Create a code execution agent."""

    instructions = """You are an agent designed to write and execute python code to answer questions.
    You have access to a python REPL, which you can use to execute python code.
    If you get an error, debug your code and try again.
    Only use the output of your code to answer the question. 
    You might know the answer without running any code, but you should still run the code to get the answer.
    If it does not seem like you can write code to answer the question, just return "I don't know" as the answer.
    """

    base_prompt = hub.pull("langchain-ai/react-agent-template")
    # Create a partial prompt with instructions
    prompt = base_prompt.partial(instructions=instructions)
    # Create the agent executor
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt,
        verbose=True,
        max_iterations=3,
        max_execution_time=120,
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    results = agent_executor.invoke(
        {"input": "Start code execution for data analysis"})
    results["output"]
