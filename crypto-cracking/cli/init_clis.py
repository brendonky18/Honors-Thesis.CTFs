from time import sleep
from cli import ClientRSA
import argparse
from ipaddress import ip_address
import signal, multiprocessing, threading
from debugger import Debugger
from queue import Queue
import os, sys, ctypes


d: Debugger
CONN_ATTEMPTS = 3
CONN_WAIT = 10
DEBUG_VERBOSE = False

# TODO: refactor with init_servs.py
def main(host: str, host_num: int=-1):
    # generates arguments
    port = 0x666c
    flag = 1
    # Message being sent should be the password for the next user
    if host_num != -1:
        num_attempts = 0
        while CONN_ATTEMPTS > num_attempts:
            file_path = f"/mnt/.share/pass{host_num + 1}"
            try:
                with open(file_path, "r") as user_file:
                    user_info = user_file.read()
            except FileNotFoundError:
                d.warn(f"File {file_path} not created. Will try again in {CONN_WAIT} second{'s' if CONN_WAIT > 1 else ''}")
                num_attempts += 1
                sleep(CONN_WAIT)
            else:
                d.ok(f"Opened file {file_path}")
                break
        if CONN_ATTEMPTS == num_attempts:
            d.err(f"File {file_path} not created. Unable to open after {num_attempts} attempts")
            exit(1)
          
        flag_text = f"flag{{{user_info.split(':')[1]}}}"
        d.debug(f"flag: {flag_text}")
        flag = int.from_bytes(flag_text.encode("ascii"), "big")

        port += host_num

    # load GLIBC
    libc = ctypes.CDLL(None)
    syscall = libc.syscall

    # other c constants
    SYS_KCMP = 312
    KCMP_FILE = 0

    p = multiprocessing.Process(
        target=ClientRSA, 
        args=(host, port), 
        kwargs={"flag": flag, "conn_attempts": CONN_ATTEMPTS, "conn_wait": CONN_WAIT, "verbose": DEBUG_VERBOSE}, 
        name=f"cli-{port}"
    )
    d.info("Spawning client process")
    p.start()

    d.info("All clients spawned")

    def cleanup(signum: int=-1, frame=None):
        """Signal handler to gracefully close terminate the clients and close their sockets

        Parameters
        ----------
        signum : int
            the signal number from 1 to 15
        frame : frame or None
            the stack frame at the time of execution
        """
        d.debug("cleanup")
        p.terminate()
        d.debug("all procs terminated")
        input_thread.join()
        d.info("Exiting main")
        exit()

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    running = True

    def get_input(out: Queue):
        nonlocal running
        """Handles user input in a separate thread to prevent blocking

        Parameters
        ----------
        out : Queue
            Queue to write the input result to, so it can be parsed in main
        """
        # WARN: do not use sys.stdin.read() will err when set to nonblocking
        # INFO: stdout, stdin, and stderr when opened in a shell all point to the same file descriptor
        # Therefore, setting O_NONBLOCK for any one of these will set it for all of them
        # see: 
        #  - https://stackoverflow.com/questions/19485751/linux-c-why-fcntl-act-on-stdin-will-also-affect-on-stdout-and-stderr
        #  - https://stackoverflow.com/questions/23865898/when-non-blocking-i-o-is-turned-on-for-stdout-is-it-correct-for-the-os-to-turn
        
        # creates a new open file description for stdin, so it can be set to non-blocking separately from stdout
        out_fd = sys.stdout.fileno()
        old_in_fd = sys.stdin.fileno()
        new_in_fd = os.open("/dev/fd/0", os.O_RDONLY | os.O_NONBLOCK)
        sys.stdin = os.fdopen(new_in_fd)
        pid = os.getpid()

        # Calls the syscall kcmp (kernel compare) to check if the new OFDs have been created
        if syscall(SYS_KCMP, pid, pid, KCMP_FILE, old_in_fd, new_in_fd) == 0:
            raise RuntimeError("Could not create new open file description for stdin")
        else:
            d.debug(f"stdout blocking: {os.get_blocking(out_fd)} stdin blocking: {os.get_blocking(new_in_fd)}")

        while running:
            try:
                user_input = sys.stdin.readline(1)
            except EOFError as e:
                d.err(f"{e}. Could not read input")
                break
            except KeyboardInterrupt:
                d.info("done")
                break
            else:
                if user_input == "q":
                    running &= False
                elif user_input != "":
                    d.warn("Ignoring input")
                    d.info("Type \"q\" to quit the program")

            sleep(0.01)
            
    
    out = Queue()
    input_thread = threading.Thread(target=get_input, name="get_input", args=(out,))
    input_thread.start()

    while running:
        running &= p.is_alive()
        
        sleep(0.01)
    d.debug("All procs ended")
    cleanup()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--host", type=ip_address, default=ip_address("127.0.0.1"))
    p.add_argument("--hostnum", dest="hostnum", type=int, default=-1)
    p.add_argument("-v", default=False, action="store_true")
    args = p.parse_args()
    DEBUG_VERBOSE = args.v
    d = Debugger(DEBUG_VERBOSE)
    d.debug(args)

    main(str(args.host), args.hostnum)