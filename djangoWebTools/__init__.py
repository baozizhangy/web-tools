import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
local_file_path = BASE_DIR + '/djangoWebTools/logs/local.logs'
print(f"=======local_file_path:{local_file_path}")
if os.path.isfile(local_file_path):
    run_env = "local"
else:
    run_env = "server"


