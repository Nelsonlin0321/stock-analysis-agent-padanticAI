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

instructions = """You are an agent designed to write and execute python code for comprehensive stock analysis given data.
    The data include the stock symbol, percentage increase, sample data in markdown format, pandas dataframe info, and csv data path for python code analysis. 
    You have access to a python REPL, which you can use to execute python code.
    If you get an error, debug your code and try again.
    The analysis should cover the last 5 trading days (e.g., calculate average change, determine a simple trend)
    change, determine a simple trend).
    """

base_prompt = hub.pull("langchain-ai/react-agent-template")
# Create a partial prompt with instructions
prompt = base_prompt.partial(instructions=instructions)
# Create the agent executor
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)
generate_code_agent = AgentExecutor(agent=agent, tools=tools, verbose=True)

if __name__ == '__main__':
    code_execution_input = """
    Response: Here is the structured data for the top NASDAQ performance stock:

    ### Stock Symbol
    - **Symbol**: `ZVZZT`

    ### Percentage Increase
    - **Percentage Increase**: `217.84%`

    ### Sample Data (Markdown Format)
    ```markdown
    | Date                      |   Open |   High |   Low |   Close |   Volume |   Dividends |   Stock Splits |
    |:--------------------------|-------:|-------:|------:|--------:|---------:|------------:|---------------:|
    | 2025-05-08 00:00:00-04:00 |  23.09 |  73.39 | 73.39 |   73.39 |   108252 |           0 |              0 |
    ```

    ### Pandas DataFrame Info
    ```plaintext
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 1 entries, 0 to 0
    Data columns (total 8 columns):
    #   Column        Non-Null Count  Dtype                           
    ---  ------        --------------  -----                           
    0   Date          1 non-null      datetime64[ns, America/New_York]
    1   Open          1 non-null      float64                         
    2   High          1 non-null      float64                         
    3   Low           1 non-null      float64                         
    4   Close         1 non-null      float64                         
    5   Volume        1 non-null      int64                           
    6   Dividends     1 non-null      float64                         
    7   Stock Splits  1 non-null      float64                         
    dtypes: datetime64[ns, America/New_York](1), float64(6), int64(1)
    memory usage: 192.0 bytes
    ```

    ### CSV Data Path for Python Analysis
    - **CSV Path**: `/Volumes/mnt/Workspace/stock-analysis-agent-padanticAI/zvzzt_performance_in_the_past_5.csv`
    """
    results = generate_code_agent.invoke(
        {"input": code_execution_input})
    print(results["output"])
