import os
import sys

def run_script(path):
    exit_code = os.system(f'python "{path}"')
    if exit_code != 0:
        print(f"Script failed: {path}")
        sys.exit(1)

if __name__ == "__main__":
    print("---- Database creation ----")
    run_script(r"C:\Users\HP\Documents\Restaurent_analysis\scripts\database_creation.py")



    print("---- Analysis of Data ----")

    run_script(r"C:\Users\HP\Documents\Restaurent_analysis\scripts\analysis.py")



    print("All steps completed successfully!")

