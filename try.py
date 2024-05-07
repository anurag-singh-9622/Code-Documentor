import os

original_file_path = 'python_gp.py'

base_name, _ = os.path.splitext(original_file_path)
file_path_with_md = f"{base_name}.md"
print(base_name)
print(file_path_with_md)