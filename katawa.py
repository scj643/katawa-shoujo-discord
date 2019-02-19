from multiprocessing import Process, Pipe
from pypresence import Presence  # The simple rich presence client in pypresence
import time

route_dict = {'hanako': {'details': "Hanako's Route", 'image': "hanako"},
              'rin': {'details': "Rin's Route", 'image': "rin"},
              'shizune': {'details': "Shizune's Route", 'image': "shizune"},
              'lilly': {'details': "Lilly's Route", 'image': "lilly"},
              'emi': {'details': "Emi's Route", 'image': "emi"},
              'kenji': {'details': "Kenji's Route?", 'image': "kenji"}}


def rpc_process(conn, routes):
    large_icon = 'main_icon'

    client_id = "545357282880389141"  # Put your Client ID in here
    rpc = Presence(client_id)  # Initialize the Presence client
    current_route = "hanako"
    current_act = '1'
    connected = False
    while not connected:
        try:
            rpc.connect()  # Start the handshake loop
            connected = True
        except FileNotFoundError:
            connected = False
            print("Is Discord running?")
            time.sleep(5)
    start_time = int(time.time())

    rpc.update(start=start_time, state="In Game")  # Set's start time

    while True:  # The presence will stay on as long as the program is running
        if current_route in routes.keys():
            rpc_route = routes[current_route]
            rpc.update(details=rpc_route['details'], large_image=rpc_route['image'], small_image=large_icon,
                       large_text=rpc_route['details'], start=start_time, state="Act: {}".format(current_act))
        if conn.poll(5):
            received = conn.recv()
            if received[0]:
                current_route = received[0]
            if received[1]:
                current_act = received[1]


if __name__ == '__main__':
    parent_conn, child_conn = Pipe(duplex=False)
    p = Process(target=rpc_process, args=(parent_conn, route_dict,))
    p.daemon = True
    p.start()
    print("Available routes")
    for i in route_dict.keys():
        print(i)
    while True:
        route = input("New Route: ")
        act = input("Act?: ")
        child_conn.send((route, act))
        time.sleep(5)
