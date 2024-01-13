import asyncio
import sys
import time
import utils.menu as menu
import os
import subprocess
from utils.ads import AdBurnKey, AdTarget, competing_targets
from utils.rpc import rpc_call, get_user_burns, check_syncing
from utils.burn import BurnAttachment
from utils.log import log


async def runner():
    log("Refreshing ads...")
    # Get competitors
    burns = await rpc_call({
        "method": "bcn_burntCoins",
        "params": [],
        "key": CONFIG["node_api_key"]
    }, CONFIG["node_url"])
    
    if "result" not in burns:
        log("Could not load burns!")
        return

    competitors = []
    for burn in burns["result"]:
        competitor = None
        try:
            ad = AdBurnKey.from_hex(burn["key"])
            competitor = (burn["amount"], AdTarget.from_hex(ad.target).__dict__, ad.cid)
        except:
            log("Burn not identified as an ad.")
        if competitor:
            competitors.append(competitor)

    competitors_scores = []
    for x in competitors:
        score = float(x[0])
        if x[1]["language"]:
            score *= 22
        if x[1]["os"]:
            score *= 5
        competitors_scores.append((x[0], score, x[1], x[2]))
    competitors_scores.sort(key = lambda x: x[1], reverse = True)

    # iterate through ads that should be kept alive
    for ad in CONFIG["ads"]:
        # create local top for ad
        ad_target = AdTarget.from_hex(ad["target"]).__dict__
        local_top = []
        for c in competitors_scores:
            if competing_targets(ad_target, c[2]):
                local_top.append(c)

        if (ad_target, ad["cid"]) in [(x[2], x[3]) for x in local_top[:3]]:
            # if ad is already in local top we do not burn any more coins
            log("Ad already in top!")
            continue

        ad_score = 0
        for elem in local_top:
            if ad_target == elem[2] and ad["cid"] == elem[3]:
                ad_score = elem[1]

        score_to_overtake = 0
        try:
            score_to_overtake = local_top[max(0,4-len(CONFIG["ads"]))-1][1]
        except IndexError:
            pass
        burn_amount = (score_to_overtake - ad_score)
        if ad_target["language"] != '':
            burn_amount /= 22
        if ad_target["os"] != '':
            burn_amount /= 5

        burn_amount += 0.01
        burn_amount = round(burn_amount, 5)

        # send burn tx
        if burn_amount > CONFIG["max_burn"]:
            log(f"Burn of {burn_amount} exceeds limit!")
            continue
        daily_burns = await get_user_burns(CONFIG["address"], CONFIG["node_url"], CONFIG["node_api_key"]) + burn_amount
        if daily_burns > CONFIG["daily_max_burn"]:
            log(f"Attempted to burn {burn_amount}, but your burns exceed the daily limit!")
            continue
        log(f"Sending burn of {burn_amount} iDNA.")

        if CONFIG["lightweight"]:
            raw_burn_tx = await rpc_call({
                "method": "bcn_getRawTx",
                "params": [{
                    "type": 12,                 # burn tx
                    "from": CONFIG["address"], 
                    "amount": burn_amount,
                    "payload": '0x' + BurnAttachment(key = AdBurnKey(cid = ad["cid"], target = ad["target"]).to_hex()).to_hex(), 
                    "useProto": True
                }],
                "key": CONFIG["node_api_key"]
            },CONFIG["node_url"])

            script_dir = os.path.dirname(os.path.abspath(__file__))
            sign_service_path = os.path.join(script_dir, "sign", "sign.js")
            signed_tx = subprocess.run(['node', sign_service_path, raw_burn_tx["result"]], capture_output=True, text=True)
            
            send_raw_tx = await rpc_call({
                "method": "bcn_sendRawTx",
                "params": [
                    signed_tx.stdout.strip()
                ],
                "key": CONFIG["node_api_key"]
                },CONFIG["node_url"])
            
            if "result" in send_raw_tx:
                log("Burn sent succesfully!")
            else:
                log("Something went wrong!")

            continue

        send_burn_tx = await rpc_call({
            "method": "dna_sendTransaction",
            "params": [{
                "type": 12,                 # burn tx
                "from": CONFIG["address"], 
                "amount": burn_amount,
                "payload": '0x' + BurnAttachment(key = AdBurnKey(cid = ad["cid"], target = ad["target"]).to_hex()).to_hex(), 
                "useProto": True
            }],
            "key": CONFIG["node_api_key"]
        },CONFIG["node_url"])

        if "result" in send_burn_tx:
            log("Burn sent succesfully!")
        else:
            log("Something went wrong!")
        
# ---------------------------------------------------------------------------------------

if __name__ == "__main__":
    # load config
    CONFIG = menu.load_config()

    try:
        arg = sys.argv[1]
    except:
        arg = None
    
    if arg == "--config": 
        while True:
            menu.showMenu()
            # get choice
            n = input("Your option: ")
            switch_dict = {
                "1": menu.set_ads,
                "2": menu.set_identity,
                "3": menu.set_max_burn,
                "4": menu.set_max_daily_burn,
                "5": menu.set_refresh_duration,
                "6": menu.set_node_connection,
                "7": menu.set_operating_mode,
                "8": menu.save_exit
            }
            if asyncio.iscoroutinefunction(switch_dict[n]):
                asyncio.run(switch_dict[n]())
            else:
                switch_dict[n]()
    else:
        # run mode
        #asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        while True:
            CONFIG = menu.load_config()  # look for updates
            if CONFIG["node_url"] == "":
                log("There is no node URL configured!")
                time.sleep(10)
                continue
            if CONFIG["node_api_key"] == "":
                log("There is no API key configured for the node!")
                time.sleep(10)
                continue
            if asyncio.run(check_syncing(CONFIG["node_url"], CONFIG["node_api_key"])):
                log("The node is currently syncing or is not accessible...")
                time.sleep(30)
                continue
            if CONFIG["address"] == "":
                log("There is no address configured!")
                time.sleep(10)
                continue
            if len(CONFIG["ads"]) == 0:
                log("There are no ads configured!")
                time.sleep(CONFIG["refresh_duration"])
                continue
            asyncio.run(runner())
            log("Sleeping...")
            time.sleep(CONFIG["refresh_duration"])