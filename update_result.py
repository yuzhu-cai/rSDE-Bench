from collections import OrderedDict
# from evaluator.utils import parse_data
from evaluator.utils_win import parse_data

def merge_result(model_names):
    def _load_result(result_dir):
        with open(result_dir, 'r') as f:
            data = f.readlines()
        return data

    def _save_result(result, result_dir):
        with open(result_dir, 'w') as f:
            f.writelines('\n'.join(result))
        return

    overall_dict = OrderedDict()
    overall_softwares = []
    for model_name in model_names:
        result_dir = f'results/{model_name}/results.txt'
        result = _load_result(result_dir)
        result_dict = parse_data(result)
        overall_softwares.extend(list(result_dict.keys()))
        overall_dict[model_name] = result_dict

    overall_softwares = list(set(overall_softwares))
    current_index = overall_softwares.index('Overall')
    overall_softwares.pop(current_index)
    overall_softwares = overall_softwares + ['Overall']
    head_line = ['Model']
    start_line = ['Task']
    software_lines = [[overall_softwares[i]] for i in range(len(overall_softwares))]
    for i in range(len(model_names)):
        model_name = model_names[i]
        head_line.extend([model_name for _ in range(2)])
        start_line.extend(['Basic', 'Advanced'])
        for j in range(len(overall_softwares)):
            software = overall_softwares[j]
            if software in overall_dict[model_name]:
                software_lines[j].extend(list(overall_dict[model_name][software].values()))
            else:
                software_lines[j].extend(['-','-'])
    overall_lines = ['\t'.join(head_line), '\t'.join(start_line)] + ['\t'.join(line) for line in software_lines]
    _save_result(overall_lines, f'results/results_col.txt')

    overall_softwares = list(set(overall_softwares))
    current_index = overall_softwares.index('Overall')
    overall_softwares.pop(current_index)
    overall_softwares = ['Overall'] + overall_softwares
    head_line = ['Task']
    start_line = ['Model']
    model_lines = [[model_names[i]] for i in range(len(model_names))]
    for i in range(len(overall_softwares)):
        software = overall_softwares[i]
        head_line.extend([software for _ in range(2)])
        start_line.extend(['Basic', 'Advanced'])
        for j in range(len(model_names)):
            model_name = model_names[j]
            if software in overall_dict[model_name]:
                model_lines[j].extend(list(overall_dict[model_name][software].values()))
            else:
                model_lines[j].extend(['-','-'])

    overall_lines = ['\t'.join(head_line), '\t'.join(start_line)] + ['\t'.join(line) for line in model_lines]
    # print(overall_lines)
    _save_result(overall_lines, f'results/results.txt')
    return

if __name__ == '__main__':
    # merge_result(['gemini-1.5-flash', 'gpt-4', 'gpt-4o-mini', 'MetaGPT', 'ChatDev'])
    # merge_result(['res1', 'res2', 'res3'])
    merge_result(['ChatDev-updating-0', 'ChatDev-updating-1', 'ChatDev-updating-2', 'ChatDev-updating-3', 'ChatDev-updating-4', 'ChatDev-updating-5'])
    # merge_result(['ChatDev-BackendFirst', 'ChatDev-BackendFirst-Updating-0', 'ChatDev-BackendFirst-Updating-1', 'ChatDev-Coding-0', 'ChatDev-Coding-1', 'ChatDev-Coding-Updating', 'ChatDev-Coding-Updating2', 'ChatDev-Coding-Updating3','ChatDev-Coding-Reviewing','ChatDev-Coding-Reviewing2','ChatDev-Coding-Reviewing3', 'ChatDev-Coding-Reviewing-Updating'])