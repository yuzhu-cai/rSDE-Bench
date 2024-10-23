import os
import json
import time
import shutil
import numpy as np
from inference.agents import OpenAILLM, ClaudeAILLM, GeminiAILLM
from inference.infer_utils import extract_python_code, create_files
from inference.software import softwares


def init_agent(model_name='gpt-4o-mini'):
    if model_name.startswith('gpt'):
        agent = OpenAILLM(
            api_key=# your api key,
            base_url=# base url,
            model=model_name,
            description= "Generate complete code to finish this task:"
        )
    elif model_name.startswith('claude'):
        agent = ClaudeAILLM(
            api_key=# your api key,
            base_url=# base url,
            model=model_name,
            description= "Generate complete code to finish this task:"
        )
    elif model_name.startswith('gemini'):
        system_message = f"""
        You are a software coding assistant. Your task is to generate a code snippet that accomplishes a specific goal.
        The code snippet must be concise, efficient, and well-commented for clarity.
        Consider any constraints or requirements provided for the task. Remember to generate GUI.

        If the task does not specify a programming language, default to Python.
        """
        # system_message = "Generate complete code to finish this task:"
        agent = GeminiAILLM(
            api_key=# your api key,
            base_url=# base url,
            model=model_name,
            description=system_message
        )
    return agent

def infer_task(agent, task_prompt, save_path):
    response = agent.infer(task_prompt)
    pyfiles = extract_python_code(response)
    create_files(pyfiles, save_path)
    return 

def infer(model_name='gpt-4o-mini', repeat_times=3, softwares=None, restore=True):
    if softwares is None:
        return None
    
    for i in range(repeat_times):
        for s in softwares:
            save_path = 'codes/{}-{}/{}'.format(model_name, i, s['name'])
            if restore and os.path.exists(save_path):
                continue
            agent = init_agent(model_name)
            infer_task(agent, s['task'], save_path)
            print('############ Finish {} ###########'.format(save_path))
    return


if __name__ == "__main__":
    repeat_times = 1
    softwares = ''
    # for model_name in ['gpt-4o-mini', 'claude-3-sonnet', 'gemini-1.5-flash-latest']:
    # for model_name in ['gemini-1.5-flash']:
    for model_name in ['gpt-4o-mini']:
    # for model_name in ['gpt-4']:
        infer(model_name, repeat_times, softwares, restore=True)