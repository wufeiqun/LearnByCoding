import traceback
import subprocess

def run_cmd(cmd):
    try:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait(timeout=10)
        out = p.stdout.read() #type: str
        err = p.stderr.read() #type: str
        return p.returncode, out, err
    except subprocess.TimeoutExpired:
        print("执行代码超时: {0}".format(cmd))
    except:
        print(traceback.print_exc())
    finally:
        p.kill() #The child process is not killed if the timeout expires

if __name__ == "__main__":
    cmd = "sleep 15"
    run_cmd(cmd)
