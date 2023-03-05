import subprocess

subprocess.call(["python", "bronze_to_silver.py"])

subprocess.call(["python", "silver_to_gold.py"])