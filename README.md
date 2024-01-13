# Idena Ad Refresher
This tool monitors the ad list and keeps yours in their relevant top.  
Currently, the script tries to keep all the ads you set in their relevant top. This can lead to significant burns depending on how many ads you configure and their targets! (Ads with no targets will burn more on average)  
Ads with no targets attempt to overtake all others, while ads with targets only try to overtake ones with similar or no targets.  

### Automatic setup
If you have an ubuntu server this script will install everything for you. It will also start the script after reboots.   
```
source <(curl -sL https://raw.githubusercontent.com/Zen-44/ad-refresher/main/ad-refresher-installer.sh)
```   

### Requirements
Python version 3.11 required.  
**Installing python requirements**:  
```
python3.11 -m pip install -r requirements.txt
```

**Installing nodejs requirements**:
```
cd sign
npm install
```
  
### Running the script:  
```
python3.11 main.py
```  
  
### Config parameter
```
python3.11 main.py --config
```  
This opens a menu which allows configuring the script.  
### Running modes
Full mode:  
- You need to have access to a running Idena node with the address owning your ads.
- The script will not use your private key directly.  

Lightweight mode:
- You can also access a shared node for the script's operation.
- The script will need to store the private key of the address owning the ads.
- Nodejs is required.  
  
By default, the script is set to full mode.
