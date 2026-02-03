# https://microsoft.github.io/autogen/stable/reference/python/autogen_agentchat.agents.html#autogen_agentchat.agents.CodeExecutorAgent

from autogen_agentchat.agents import CodeExecutorAgent
import asyncio
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor


def getCodeExecutorAgent(code_executor):

    code_executor_agent = CodeExecutorAgent(
        name='CodeExecutor',
        code_executor = code_executor
    )

    return code_executor_agent


async def main():

    docker=DockerCommandLineCodeExecutor(
    work_dir='temp',
    image="python:3.11-slim", # Lightweight but functional
    container_name="autogen_runtime",
    auto_remove=True,
    timeout=120
)


    code_executor_agent = getCodeExecutorAgent(docker)

    task = TextMessage(
        content=''' Here is the Python Code which You have to run.
```python
print('Hello to Vinay World')
''',
    source='User'
    )


    try:
        await docker.start()

        res = await code_executor_agent.on_messages(
            messages=[task],
            cancellation_token=CancellationToken()
        )
        print('result is :',res)

    except Exception as e:
        print(e)
    finally:
        await docker.stop()

if (__name__ == '__main__'):
    asyncio.run(main())

    