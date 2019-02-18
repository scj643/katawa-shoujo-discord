from pypresence import Presence  # The simple rich presence client in pypresence
import time

route_dict = {'hanako': {'details': "Hanako's Route", 'image': "hanako"},
              'rin': {'details': "Rin's Route", 'image': "rin"},
              'shizune': {'details': "Shizune's Route", 'image': "shizune"},
              'lilly': {'details': "Lilly's Route", 'image': "lilly"},
              'emi': {'details': "Emi's Route", 'image': "emi"},
              'kenji': {'details': "Kenji's Route?", 'image': "kenji"}}

current_route = "hanako"

large_icon = 'main_icon'

client_id = "545357282880389141"  # Put your Client ID in here

if __name__ == '__main__':
    print("Available routes")
    for i in route_dict.keys():
        print(i)
    start_time = int(time.time())
    RPC = Presence(client_id)  # Initialize the Presence client
    connected = False
    while not connected:
        try:
            RPC.connect()  # Start the handshake loop
            connected = True
        except FileNotFoundError:
            connected = False
            print("Is Discord running?")
            time.sleep(5)

    RPC.update(start=start_time, state="In Game")  # Set's start time
    while True:  # The presence will stay on as long as the program is running
        new_route = input('new route: ')
        if new_route in route_dict.keys():
            route = route_dict[new_route]
            RPC.update(details=route['details'], large_image=route['image'], small_image=large_icon,
                       large_text=route['details'], start=start_time, state="In Game")
        time.sleep(15)  # Can only update rich presence every 15 seconds
