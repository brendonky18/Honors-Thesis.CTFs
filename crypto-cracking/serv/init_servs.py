import serv, gen_brute_force, gen_small_e, gen_fermat
import signal, multiprocessing

def main():
    print("gen_small_e")
    # TODO: wait for client to send me the ports I should be using
    ports = 0x666c, 0x666d, 0x666e
    procs = [
        multiprocessing.Process(target=serv.main, args=(*gen_brute_force.generate(),   ports[0]), name="brute_force"),
        multiprocessing.Process(target=serv.main, args=(*gen_small_e.generate(),       ports[1]), name="small_e"),
        multiprocessing.Process(target=serv.main, args=(*gen_fermat.generate(),        ports[2]), name="fermat")
    ]

    for p in procs:
        print("Spawning server process")
        p.start()
    print("All servers spawned")
    
    def cleanup(*args):
        for p in procs: 
            p.terminate()
        
        print("\nExiting main")
        exit()

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

if __name__ == "__main__":
    main()