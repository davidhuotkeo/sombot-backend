import os
import subprocess

def setup_env():
    env_path = "env"
    command_file = "commands/command.txt"

    is_env_exist = os.path.exists(env_path)

    if not is_env_exist:
        with open(command_file, "r") as command:
            raw_command = command.read()
            cmds = raw_command.split("\n")
            for cmd in cmds:
                print(f"Running {cmd}")
                subprocess.run(cmd)
