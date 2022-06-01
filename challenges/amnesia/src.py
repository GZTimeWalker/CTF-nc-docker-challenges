import subprocess
import os
import sys
import uuid

def run(level):
    print("Your code for Mild Amnesia: (Two empty lines to end): ")
    code1 = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        code1.append(line)
        if len(code1) >= 2 and code1[-1] == '' and code1[-2] == '':
            break

    play_path = uuid.uuid4().hex

    os.system(f"mkdir -m777 -p /tmp/{play_path}/lib/i386-linux-gnu/ && chmod +t /tmp/{play_path}")

    with open(f"/tmp/{play_path}/code.c", "w") as fd1:
        for i in code1:
            fd1.write(i)
            fd1.write("\n")
        fd1.close()

    print('Compiling...\n')
    sys.stdout.flush()

    os.system(f"ln compile_{level}.sh /tmp/{play_path}/compile.sh")
    os.system(f"ln ld-2.33.so /tmp/{play_path}/lib/ld-linux.so.2")
    os.system(f"ln libc-2.33.so /tmp/{play_path}/lib/i386-linux-gnu/libc.so.6")

    p = subprocess.run(["/bin/sh", "-c", f"cd /tmp/{play_path}/ && ./compile.sh"], stderr = subprocess.DEVNULL)

    if p.returncode != 0:
        return

    print('Running...\n')
    sys.stdout.flush()

    p = subprocess.run(
            ["chroot", f"/tmp/{play_path}/", "/a.out"],
            stdout = subprocess.PIPE,
            stdin = subprocess.DEVNULL,
            stderr = subprocess.STDOUT,
        )


    try:
        output = p.stdout.decode()
    except UnicodeDecodeError:
        print("Output decode error, non-ASCII character detected. Failed. ")
        output = "(invalid)"

    subprocess.run(["rm", "-rf", f"/tmp/{play_path}"])

    retval = p.returncode

    print(f"Return: {retval}")
    print(f"Output: \n{output}")

    if (retval != 0):
        print("Your code didn\'t end properly.")
    elif output == "Hello, world!" or output == "Hello, world!\n":
        print("Passed!")
        try:
            print(open(f"flag{level}").read())
        except FileNotFoundError:
            print("Flag file not found! Please contact developers.")
    else:
        print("Failed.")

if __name__ == "__main__":
    try:
        level = int(input("Challenge level (1/2): "))
        if 0 < level < 3:
            run(level)
        else:
            print("Invalid level.")
    except:
        print("Error occured.")
