try:
    from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
except ImportError:
    # Fallback or alternative path if needed, but assuming autogen-ext contains it
    from autogen.coding import LocalCommandLineCodeExecutor

from config.constants import TIMEOUT_DOCKER, WORK_DIR_DOCKER

def getDockerCommandLineExecutor():
    # We use LocalCommandLineCodeExecutor because the backend is already running 
    # inside a Docker container (agent_backend). 
    # Nested Docker (DinD) is complex and unnecessary here.
    executor = LocalCommandLineCodeExecutor(
        work_dir=WORK_DIR_DOCKER,
        timeout=TIMEOUT_DOCKER
    )
    
    return executor


async def start_docker_container(docker):
    if hasattr(docker, 'start'):
        print("Starting Docker Container")
        await docker.start()
        print("Docker Container Started")


async def stop_docker_container(docker):
    if hasattr(docker, 'stop'):
        print("Stop Docker Container")
        await docker.stop()
        print("Docker Container Stopped")
