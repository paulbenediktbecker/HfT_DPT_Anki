import subprocess
import os 
def pull_commit_push():

    commit_message = input("Input commit Message")
    commit_message = "'" + commit_message + "'"

    cmd = "git pull"
    args = cmd.split()
    subprocess.call(args)

    cmd = "git add -A"
    args = cmd.split()
    subprocess.call(args)

    cmd = "git commit -m"
    args = cmd.split()
    args.append(commit_message)
    subprocess.call(args)

    cmd = "git push"
    args = cmd.split()
    subprocess.call(args)

