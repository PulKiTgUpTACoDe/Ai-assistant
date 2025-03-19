import os

# Get the current directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# List of directories where __init__.py files should be created
dirs = [
    'core/agents',
    'core/memory',
    'core/retrieval',
    'core/tools',
    'core/utils',
    'models',
    'services',
    'database',
    'database/faiss_index',
    'web',
    'tests',
    'scripts',
    'config'
]

# Create __init__.py in each directory
for dir_path in dirs:
    # Convert to absolute path
    abs_dir_path = os.path.join(base_dir, dir_path.replace('/', os.path.sep))
    
    # Make sure the directory exists
    os.makedirs(abs_dir_path, exist_ok=True)
    
    # Create the __init__.py file
    init_file = os.path.join(abs_dir_path, '__init__.py')
    with open(init_file, 'w') as f:
        pass  # Create an empty file
    print(f"Created {init_file}")

print("All __init__.py files created successfully!") 