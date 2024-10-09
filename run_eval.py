import os
import json
import time
import shutil
import numpy as np
import importlib.util 
from evaluator.checker import Checker

def clean_up():
    time.sleep(0.5)
    if os.path.exists('game.log'):
        os.remove('game.log')
    if os.path.exists('test'):
        shutil.rmtree('test')

def list_folders(directory):  
    folders = [] 
    for item in os.listdir(directory):  
        item_path = os.path.join(directory, item)  
        if os.path.isdir(item_path):  
            folders.append(item)
    return folders

def load_main(folder_path, task):
    single_dir = f'codes/{folder_path}/{task}/main.py'
    mac_dir = f'codes/{folder_path}/{task}/{task}/main.py'
    main_dir = single_dir if os.path.exists(single_dir) else mac_dir
    return main_dir

def evaluate(folder_path, checker, result_path, restore=True):
    if not os.path.exists(f'codes/{folder_path}'):
        return
    if not os.path.exists(f'results/{result_path}'):
        os.makedirs(f'results/{result_path}')

    all_tasks = list_folders(f'codes/{folder_path}')

    prev_results = None
    if os.path.exists(f'results/{result_path}/results.json'):
        with open(f'results/{result_path}/results.json', 'rb') as f:
            prev_results = json.load(f)
    if prev_results is not None and restore:
        tasks = [x for x in all_tasks if x not in prev_results]
    else:
        tasks = all_tasks
    
    print('*******************************************')
    print(f'# Evaluate: {folder_path}')
    print(f'# Number of tasks: {len(tasks)}')
    print('*******************************************')
    
    results = {
        "all": {
            "total": 0,
            "total_basic": 0,
            "total_advanced": 0,
            "basic": 0,
            "advanced": 0
        }
    }
    for task in tasks:
        class_name = f"Test{task}"
        print('*******************************************')
        print(f'# Evaluate Task: {task}')
        print('*******************************************')
        try:
            class_file_path = os.path.join('evaluator', f"{class_name}.py")
            spec = importlib.util.spec_from_file_location(class_name, class_file_path)  
            module = importlib.util.module_from_spec(spec)  
            spec.loader.exec_module(module)  

            eval_class = getattr(module, class_name)  
            evaluator = eval_class(checker, load_main(folder_path, task))
            res = evaluator.main()
            
            results[task] = res
            results['all']['total'] += res['total']
            results['all']['total_basic'] += res['total_basic']
            results['all']['total_advanced'] += res['total_advanced']
            results['all']['basic'] += res['basic']
            results['all']['advanced'] += res['advanced']
            clean_up()

        except Exception as e:
            print(f"An error occured while evaluating task '{task}': {e}")
    
    if prev_results is not None and restore:
        prev_results.update(results)
        results = prev_results
        results['all']['total'] = sum([results[task]["total"] for task in all_tasks if task != 'all'])
        results['all']['total_basic'] = sum([results[task]["total_basic"] for task in all_tasks if task != 'all'])
        results['all']['total_advanced'] = sum([results[task]["total_advanced"] for task in all_tasks if task != 'all'])
        results['all']['basic'] = sum([results[task]["basic"] for task in all_tasks if task != 'all'])
        results['all']['advanced'] = sum([results[task]["advanced"] for task in all_tasks if task != 'all'])
    with open(f'results/{result_path}/results.json', 'w') as file:
        json.dump(results, file, indent=4)


def calculate_all(path):
    folders = list_folders(path)
    tasks = {}
    total = {
        'basic': [],
        'advanced': []
    }
    for folder in folders:
        with open(f'{path}/{folder}/results.json', 'r') as json_file:
            data = json.load(json_file)
        for item in data:
            if item != 'all':
                if tasks.get(item) is not None:
                    tasks[item]['basic'].append(data[item]['basic'])
                    tasks[item]['advanced'].append(data[item]['advanced'])
                else:
                    tasks[item] = {}
                    tasks[item]['total'] = data[item]['total']
                    tasks[item]['total_basic'] = data[item]['total_basic']
                    tasks[item]['total_advanced'] = data[item]['total_advanced']
                    tasks[item]['basic'] = [data[item]['basic']]
                    tasks[item]['advanced'] = [data[item]['advanced']]
            else:
                total['total'] = data[item]['total']
                total['total_basic'] = data[item]['total_basic']
                total['total_advanced'] = data[item]['total_advanced']
                total['basic'].append(data[item]['basic'])
                total['advanced'].append(data[item]['advanced'])

    for item in tasks:
        tasks[item]['mean_basic'] = np.around(np.mean(tasks[item]['basic']),2)
        tasks[item]['mean_advanced'] = np.around(np.mean(tasks[item]['advanced']),2)
        tasks[item]['std_basic'] = np.around(np.std(tasks[item]['basic']),2)
        tasks[item]['std_advanced'] = np.around(np.std(tasks[item]['advanced']),2)
    
    total['mean_basic'] = np.around(np.mean(total['basic']),2)
    total['mean_advanced'] = np.around(np.mean(total['advanced']),2)
    total['std_basic'] = np.around(np.std(total['basic']),2)
    total['std_advanced'] = np.around(np.std(total['advanced']),2)

    with open(f'{path}/results.txt', 'w', encoding='utf-8') as file:
        file.write("Task\t\tBasic\t\tAdvanced\n")
        for item in tasks:
            file.write(f"{item}\t\t{tasks[item]['mean_basic']}±{tasks[item]['std_basic']}/{tasks[item]['total_basic']}\t{tasks[item]['mean_advanced']}±{tasks[item]['std_advanced']}/{tasks[item]['total_advanced']}\n")
        file.write(f"Overall\t\t{total['mean_basic']}±{total['std_basic']}/{total['total_basic']}\t{total['mean_advanced']}±{total['std_advanced']}/{total['total_advanced']}\n")

if __name__ == "__main__":
    api_key = ''
    checker = Checker(
        api_key=api_key,
    )
    for path in ['4o-mini-0']:
        evaluate(path, checker, f"{path.rsplit('-', 1)[0]}/{path}")
    calculate_all('results/4o-mini')