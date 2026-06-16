import os
import subprocess
import sys

def run_script(script_path, working_dir=None):
    print(f"\n[{'*'*10}] Running {script_path} [{'*'*10}]")
    if working_dir:
        cwd = working_dir
        cmd = [sys.executable, os.path.basename(script_path)]
    else:
        cwd = os.getcwd()
        cmd = [sys.executable, script_path]
        
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode != 0:
        print(f"Error running {script_path}. Exiting.")
        sys.exit(1)

def run_notebook(notebook_path):
    print(f"\n[{'*'*10}] Executing Notebook {notebook_path} [{'*'*10}]")
    cmd = [sys.executable, "-m", "nbconvert", "--to", "notebook", "--execute", "--inplace", notebook_path]
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"Error executing notebook {notebook_path}. Exiting.")
        sys.exit(1)

def main():
    print("==================================================")
    print("   Bluestock Capstone - Master Run Pipeline")
    print("==================================================")
    
    # Run Python scripts
    run_script("scripts/etl_pipeline.py")
    
    # Run Analytics Notebooks
    run_notebook("notebooks/04_performance_analytics.ipynb")
    run_notebook("notebooks/05_advanced_analytics.ipynb")
    
    print("\n" + "="*50)
    print("Pipeline Execution Complete!")
    print("All processed datasets, databases, and metrics have been generated.")
    print("="*50)

if __name__ == "__main__":
    main()
