import os
from pathlib import Path

def generate_llm_readme(repo_path, output_file="llm_input.txt"):
    """Processes directory structure and file contents for LLM ingestion"""
    # Convert repo_path to string for compatibility
    repo_path = Path(repo_path).resolve()
    output_file = repo_path / output_file  # Ensure output file is in the same directory

    exclude_dirs = {'.github', 'node_modules'}
    exclude_files = {'compiled_code.txt'}
    include_ext = {'.yaml', '.yml', 'Dockerfile', 'Chart.yaml'}
    sensitive_keywords = {'password', 'secret', 'key', 'certificate'}

    output = []

    # Generate directory tree
    tree = []
    for root, dirs, files in os.walk(repo_path):
        # Filter directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        rel_path = os.path.relpath(root, repo_path)
        level = rel_path.count(os.sep)
        indent = '│   ' * level + '├── ' if level > 0 else ''
        tree.append(f"{indent}{os.path.basename(root)}/")
        for f in files:
            if f not in exclude_files and (Path(f).suffix in include_ext or Path(f).name in include_ext):
                tree.append(f"{indent}│   ├── {f}")

    output.append("Directory Structure:\n" + '\n'.join(tree) + '\n\n')

    # Process file contents
    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = Path(root) / file
            if file in exclude_files or (file_path.suffix not in include_ext and file_path.name not in include_ext):
                continue

            try:
                with open(file_path, 'r') as f:
                    content = f.read()

                    # Basic redaction
                    lines = []
                    for line in content.split('\n'):
                        if any(kw in line.lower() for kw in sensitive_keywords):
                            lines.append("# REDACTED: Sensitive content removed")
                        else:
                            lines.append(line)

                    output.append(f"=== File: {file_path.relative_to(repo_path)} ===\n")
                    output.append('\n'.join(lines) + '\n\n')

            except UnicodeDecodeError:
                output.append(f"=== File: {file_path.relative_to(repo_path)} ===\n")
                output.append("# BINARY FILE CONTENTS NOT SHOWN\n\n")

    # Write to output file
    with open(output_file, 'w') as f:
        f.writelines(output)

if __name__ == "__main__":
    repo_path = Path.home() / 'Documents' / 'elk-stack-repo'
    
    # Ensure the directory exists before proceeding
    if not repo_path.exists():
        print(f"Error: Directory {repo_path} does not exist.")
    else:
        generate_llm_readme(repo_path)
        print(f"LLM input file generated at: {repo_path / 'llm_input.txt'}")


