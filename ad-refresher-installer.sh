sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install git unzip curl screen python3.11 pip nodejs npm -y

git clone https://github.com/Zen-44/ad-refresher
chmod +x $PWD/ad-refresher/main.py

cd ad-refresher
python3.11 -m pip install -r requirements.txt
cd sign
npm install
cd

(crontab -l 2>/dev/null; echo "@reboot screen -dmS refresher python3.11 $PWD/ad-refresher/main.py") | crontab -
screen -dmS refresher python3.11 $PWD/ad-refresher/main.py

echo ""
echo "Ad refresher was installed. Please configure your node and address (python3.11 ./ad-refresher/main.py --config)"
