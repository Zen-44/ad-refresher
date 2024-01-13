from utils.ads import AdTarget, Ad, competing_targets
from utils.rpc import rpc_call
from utils.dna_profile import Profile
from eth_account import Account
import os
import json
import time

CONFIG = {}
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "..", "config.json")
try:
    with open(file_path, 'r') as json_file:
        CONFIG = json.load(json_file)
except FileNotFoundError:
    # create default config
    CONFIG = {
        "private_key": "",
        "address": "",
        "max_burn": 10.0,
        "daily_max_burn": 25.0,
        "refresh_duration": 600,
        "node_url": "",
        "node_api_key": "",
        "ads": [],
        "lightweight": False
        }
    with open(file_path, 'w') as json_file:
        json.dump(CONFIG, json_file, indent=2)
    
def load_config():
    with open(file_path, 'r') as json_file:
        CONFIG = json.load(json_file)
    return CONFIG

def save_config():
    with open(file_path, 'w') as json_file:
        json.dump(CONFIG, json_file, indent=2)
        
async def set_ads():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("= Setting ads to be ran = ")
    if CONFIG["node_url"] == "" or CONFIG["node_api_key"] == "":
        print("Please configure a node connection first!")
        print("You will be returned to the menu...")
        time.sleep(5)
    if CONFIG["address"] == '':
        print("Please configure you address first!")
        print("You will be returned to the menu...")
        time.sleep(5)
        return
    print("This overwrites previous ad configurations\n")
    print("Your ads are: ")
    identity = await rpc_call({
        "method": "dna_identity",
        "params": [
            CONFIG["address"]
        ],
        "key": CONFIG["node_api_key"]
    },CONFIG["node_url"])
    profile_hash = identity["result"]["profileHash"]

    if profile_hash == "":
        print("You don't seem to have any ads published!!")
        print("Returning to menu...")
        time.sleep(3)
        return

    user_profile = await rpc_call({
        "method": "ipfs_get",
        "params": [
            profile_hash
        ],
        "key": CONFIG["node_api_key"]
    },CONFIG["node_url"])
    user_profile = user_profile["result"]

    decoded_profile = Profile.from_hex(user_profile[2:])
    index = 1

    for ad_data in decoded_profile.ads:
        print(f"{index}) ",end = "")
        # Get ad
        ad = await rpc_call({
            "method": "ipfs_get",
            "params": [
                ad_data["cid"]
            ],
            "key": CONFIG["node_api_key"]
        },CONFIG["node_url"])
        try:
            ad = Ad.from_hex(ad["result"][2:]).__dict__
            print(f'Title:       {ad["title"]}')
            print(f'   Description: {ad["desc"]}')
            print(f'   Targets:     ', end = "")
            targets = AdTarget.from_hex(ad_data["target"]).__dict__
            first = True
            anyTarget = False
            for key in targets:
                if targets[key]:
                    if first:
                        first = False
                    else:
                        print(" " * 16, end = "")
                    print(f'{key.capitalize()}: {targets[key]}')
                    anyTarget = True
            if not anyTarget:
                print("None")
            
            print()
        except:
            print("Error: This ad was not loaded")

        index += 1
    
    ads_to_be_ran = input("\nEnter numbers of ads to be ran (their number separated by space): ")
    ads_to_be_ran = list(map(int,ads_to_be_ran.split()))
    if len(ads_to_be_ran) > 3:
        option = input("Only 3 ads can with the same targets can be seen at once by users. Are you sure you want to add more than 3 ads? [Y/N]: ")
        if option.capitalize()[0] == "N":
            print("You will be returned to the menu...")
            time.sleep(3)
            return
    CONFIG["ads"] = []
    for index in ads_to_be_ran:
        ad_to_be_added = decoded_profile.ads[index - 1]
        CONFIG["ads"].append(ad_to_be_added)
        CONFIG["ads"][-1]["target"] = AdTarget.from_hex(CONFIG["ads"][-1]["target"]).to_hex()   # use correct burn encoding
    save_config()
    print("Selected ads have been added succesfully!\nReturning to menu...")
    time.sleep(3)

def set_identity():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("= Setting identity = ")
    if CONFIG["lightweight"]:
        priv_key_hex = input("Enter your private key: ")
        CONFIG["private_key"] = priv_key_hex
        private_key_bytes = bytes.fromhex(priv_key_hex)
        CONFIG["address"] = Account.from_key(private_key_bytes).address
        save_config()
        print("Private key has been saved succesfully!\nRetunring to menu...")
        time.sleep(3)
    else:
        addr = input("Enter your Idena address: ")
        CONFIG["address"] = addr
        save_config()
        print("Address has been saved succesfully!\nRetunring to menu...")
        time.sleep(3)

def set_max_burn():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("= Setting maximum burn amount = ")
    print("Your ad will not be refreshed if a burn exceeds this limit")
    print("This limit can be exceeded by multiple lower burns!!!")
    max_burn_amount = input("Enter the maximum amount that should be burnt at one time (iDNA): ")
    CONFIG["max_burn"] = float(max_burn_amount)
    save_config()
    print("Amount was saved succesfully!\nReturning to menu...")
    time.sleep(3)

def set_max_daily_burn():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("= Setting maximum burn amount per day = ")
    print("Your ads will not be refreshed if all your burns from the last 24 hours exceed this limit.")
    max_burn = input("Enter the maximum amount that should be burnt in 24h (iDNA): ")
    CONFIG["daily_max_burn"] = float(max_burn)
    save_config()
    print("Amount was saved succesfully!\nReturning to menu...")
    time.sleep(3)

def set_refresh_duration():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("= Setting refresh duration = ")
    print("This is how often the script will check to see if your selected ads are in the top")
    refresh_duration = int(input("Enter refresh duration (minutes): "))
    CONFIG["refresh_duration"] = refresh_duration * 60
    save_config()
    print("Duration saved succesfully!\nReturning to menu...")
    time.sleep(3)

async def set_node_connection():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("= Setting node connection = ")
    print("You can set your own node (localhost) or a shared node (if you configured the lightweight version)")
    while True:
        url = input("Enter the node URL: ")
        api_key = input("Enter the API key: ")
        # get status
        check_status = await rpc_call({
            "method": "bcn_syncing",
            "params": [],
            "key": api_key
        },url)
        try:
            if check_status["result"]:
                break
        except:
            print("The node you provided can not be reached or the API key is incorrect!")
    CONFIG["node_url"] = url
    CONFIG["node_api_key"] = api_key
    save_config()
    print("Node was saved succesfully!\nReturning to menu...")
    time.sleep(3)

def set_operating_mode():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("= Setting script operating mode = ")
    print("There are 2 operating modes: full and lightweight\n")
    print("Lightweight: You can connect to a shared node and you need to have your private key added to the config.\n  You also need nodejs installed!!")
    print("Full: You need to run your own Idena node with the address owning the ads and connect to it (ideally on your local network).\n  This mode does not require you to config a private key and nodejs is not required.\n")
    if CONFIG["lightweight"]:
        print(f"The script is currently configured in lightweight mode.")
        print("(Nodejs is required for this operating mode!)\n")
        switch = input("Would you like to switch to full mode? [Y/N]: ")
        if switch.capitalize()[0] == "Y":
            CONFIG["lightweight"] = False
            CONFIG["private_key"] = ""
            save_config()
            print("Mode was saved succesfully!\nReturning to menu...")
            time.sleep(3)
        else:
            print("Mode was saved succesfully!\nReturning to menu...")
            time.sleep(3)
    else:
        print(f"The script is currently configured in full mode.")
        switch = input("Would you like to switch to lightweight mode? [Y/N]: ")
        if switch.capitalize()[0] == "Y":
            CONFIG["lightweight"] = True
            priv_key_hex = input("Enter your private key (for the address owning the ads): ")
            CONFIG["private_key"] = priv_key_hex
            private_key_bytes = bytes.fromhex(priv_key_hex)
            CONFIG["address"] = Account.from_key(private_key_bytes).address
            save_config()
            print("Mode was saved succesfully!\nReturning to menu...")
            time.sleep(3)
        else:
            print("Returning to menu...")
            time.sleep(3)


def save_exit():
    save_config()
    exit(0)

def showMenu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("= Configuration mode =")
    print("Select one of the options to edit: ")
    print("1) Set ads to be ran")
    print("2) Set identity")
    print("3) Set max burn per refresh")
    print("4) Set max daily burn")
    print("5) Set refresh duration")
    print("6) Set node connection")
    print("7) Set operating mode")
    print("8) Save and exit")