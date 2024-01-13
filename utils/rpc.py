import aiohttp

id = 0

async def rpc_call(call_data, url):
    global id
    call_data["id"] = id
    id += 1
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=call_data, headers={'Content-Type': 'application/json'}) as response:
                if response.status == 200:
                    result = await response.json()
                    return result
                else:
                    print(f"HTTP request failed with status code {response.status}")
        except Exception as e:
            print(f"An error occurred: {e}")

async def get_user_burns(addr, url, api_key):
    burns = await rpc_call({
            "method": "bcn_burntCoins",
            "params": [],
            "key": api_key
            },url)
    totalBurns = 0
    for burn in burns["result"]:
        if burn["address"] == addr.lower():
            totalBurns += float(burn["amount"])
    return totalBurns

async def check_syncing(url, api_key):
    sync_check = await rpc_call({
        "method": "bcn_syncing",
        "params": [],
        "key": api_key
        },url)
    try:
        return sync_check["result"]["syncing"]
    except:
        return True