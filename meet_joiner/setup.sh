apt install python3-pip
apt install python3.11-venv
python3 -m venv ./venv
source venv/bin/activate
pip install selenium
pip install faker
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt -f install
sudo dpkg -i google-chrome-stable_current_amd64.deb
if above step fails run again -> sudo apt -f install
run again sudo dpkg -i google-chrome-stable_current_amd64.deb


env is ready
copy code


