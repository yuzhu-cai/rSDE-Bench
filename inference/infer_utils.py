import os

def extract_python_code(reply):
    lines = reply.split('\n')
    code_block = []
    collecting_code = False

    for line in lines:
        stripped_line = line.strip()

        if stripped_line.startswith('```python'):
            collecting_code = True
            code_block = []
        elif stripped_line == '```' and collecting_code:
            collecting_code = False
            break  # Stop collecting code after the first closing ```
        elif collecting_code:
            code_block.append(line)

    # Join code lines into a single string
    code_text = '\n'.join(code_block)

    return code_text


def create_files(pyfiles, software_path):
    if not os.path.exists(software_path):
        os.makedirs(software_path)

    with open(os.path.join(software_path,'main.py'), 'w') as f:
        f.write(pyfiles)


def extract_code_blocks(reply):
    lines = reply.split('\n')
    code_dict = {}
    current_filename = None
    collecting_code = False
    current_code = []

    for line in lines:
        stripped_line = line.strip()
        
        if stripped_line.startswith('@') and (stripped_line.endswith('.py') or stripped_line.endswith('.html') or stripped_line.endswith('.css')):
            if current_filename and collecting_code:
                code_dict[current_filename] = '\n'.join(current_code)
                current_code = []

            current_filename = stripped_line.split()[-1].split('/')[-1]
            collecting_code = False
        
        elif stripped_line.startswith('```python') or stripped_line.startswith('```html') or stripped_line.startswith('```css'):
            collecting_code = True
            current_code = []
        
        elif stripped_line == '```' and collecting_code:
            if current_filename:
                code_dict[current_filename] = '\n'.join(current_code)
            collecting_code = False
            current_code = []
            current_filename = None

        elif collecting_code:
            current_code.append(line)

    return code_dict


def build_website_project(codes, software_path):
    if not os.path.exists(software_path):
        os.makedirs(software_path)
    if not os.path.exists(f'{software_path}/templates'):
        os.makedirs(f'{software_path}/templates')
    if not os.path.exists(f'{software_path}/static'):
        os.makedirs(f'{software_path}/static')

    for code in codes:
        if code.endswith('.py'):
            with open(os.path.join(software_path, code), 'w') as f:
                f.write(codes[code])
        if code.endswith('.html'):
            with open(os.path.join(software_path, f'templates/{code}'), 'w') as f:
                f.write(codes[code])
        if code.endswith('.css'):
            with open(os.path.join(software_path, f'static/{code}'), 'w') as f:
                f.write(codes[code])
