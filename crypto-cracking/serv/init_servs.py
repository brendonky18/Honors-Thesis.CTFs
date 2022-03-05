from serv import ServerRSA
import gen_brute_force, gen_small_e, gen_fermat
import signal, multiprocessing
from enum import Enum
from debugger import Debugger
 
def main():
    d = Debugger(True)

    d.printf("gen_small_e")
    # TODO: wait for client to send me the ports I should be using
    ports = 0x666c, 0x666d, 0x666e
    procs = [
        multiprocessing.Process(target=ServerRSA, args=(gen_brute_force.generate, ports[0]), name="brute_force"),
        multiprocessing.Process(target=ServerRSA, args=(gen_small_e.generate,     ports[1]), name="small_e"),
        multiprocessing.Process(target=ServerRSA, args=(gen_fermat.generate,      ports[2]), name="fermat")
    ]

    for p in procs:
        d.printf(f"Spawning server process {p.name}")
        p.start()
    d.info("All servers spawned")
    
    def cleanup(*args):
        for p in procs: 
            p.terminate()
        
        d.info("Exiting main")
        exit()

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    while True:
        d.info("Type \"q\" to quit the program")
        val = input()
        if val == "q":
            cleanup()
        else:
            d.warn("Ignoring input")

if __name__ == "__main__":
    main()