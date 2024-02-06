## TODO
- core features
   - [] new Updater that only updates on order completion to reduce spam
      - [] use pairing of ad activity vs orderCount for better more accurate/logical updates
   - [] log user state data of each update for accuracy check 
   - [x] fix new day 30 day count reset bug
- telebot features
   - [] query advertiser data from telegram
   - [] subscription to different streams (binance, htx, swap rates etc)
- QOL features
  - [] add function to only report updates on watchlist and whale events.
    - []  configurable threshold for 'whale' events
  - []  add function to add user ids to watchlist in realtime and update watchlist file  Extension
  - []  add swapping rates updates
  - []  add triggers to prompt for swapping when rate is good

## Instructions 
1. Run the pip command below to install required python modules.
```
pip install -r requirements.txt
```
2. Create a [cex_name]_config.json (e.g. htx_config.json) file containing relevant secrets/config as listed in the template.json file.

3. Run main.py with the command and arguments below. [cex] is the name of the exchange api that you want to use, can be htx OR binance for now. [mode] is the mode (type of updater) that you want to run, can be 1 for now.
```
python main.py [cex] [1]
```

## Explanations
1. [cex_name]_advertisers.txt contains the information of all advertisers that are tracked by the program. It will automatically be updated as the program runs.
2. [cex_name]_watchlist.txt contains a list of cex-specific user ids that are to be specifically tracked.