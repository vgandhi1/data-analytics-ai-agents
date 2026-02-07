from autogen_agentchat.agents import AssistantAgent
from agents.prompts.DataAnalyzerAgentPrompt import get_data_analyzer_prompt


def getDataAnalyzerAgent(model_client, filename="data.csv"):
    data_analyzer_agent = AssistantAgent(
        name='Data_Analyzer_Agent',
        description='An agent which helps with solving Data Analysis task and gives the code as well',
        model_client=model_client,
        system_message=get_data_analyzer_prompt(filename)
    )

    return data_analyzer_agent
