import cex_api
import time
import logging
import tg_logger
import json
import sys
import traceback
from ad import Ads
from Updater import BareBonesUpdater

cex, mode= sys.argv[1:3]
api = None

# choose exchange
if cex == "htx":
  with open("htx_config.json") as f:
    env = json.load(f)
  api = cex_api.HtxAPI()
  from User import HtxUser as User
else:
  with open("binance_config.json") as f:
    env = json.load(f)
  api = cex_api.BinanceAPI()
  from User import BinanceUser as User

    
ADVERTISERS_FILENAME = env["ADVERTISERS_FILENAME"]
WATCHLIST_FILENAME = env["WATCHLIST_FILENAME"]
TELE_TOKEN = env["TELE_TOKEN"]
TELE_USERS = env["TELE_USERS"]
TIMEOUT = env["TIMEOUT"]


def main(logger, users, updater):
  
  while True: # always restart after error out
    try:
      # add watchlist to user list
      for user_id in watchlist:
        if user_id not in users:
          users[user_id] = User(api.get_user(user_id), user_id)
      
      while True:
        print("Starting Cycle...")
        buy_list, sell_list = api.get_ad_list()
        ad_list = [Ads(ad) for ad in buy_list] + [Ads(ad) for ad in sell_list]
        
        # check for new ads and add new advertisers if any
        for ad in ad_list:
          if ad.user_id not in users:
            user = api.get_user(ad.user_id)
            users[ad.user_id] = User(user, ad.user_id) # add new user to db
            logger.info(f"A new advertiser just joined: {ad.user_name}")
            
        for user in users.values():
          try:
            new_data = api.get_user(user.id)
          except:
            logger.error("ERROR getting %s data! id: %s", user.name, user.id)
            new_data = user.data
          updater.update_user(user, new_data)
          user.data = new_data

        with open(ADVERTISERS_FILENAME, 'w') as file:
          save_dict = {}
          for user in users.values():
            save_dict[user.id] = user.data
          file.write(json.dumps(save_dict, indent=2))
        time.sleep(TIMEOUT)
      
    except Exception as e:
      logger.error(traceback.format_exc())
      logger.error("PROGRAM CRASHED! Restarting...")
      time.sleep(TIMEOUT)


if __name__ == "__main__":
  # load watchlist
  watchlist = []
  with open(WATCHLIST_FILENAME) as file:
    watchlist = file.readlines()
    watchlist = [x.strip() for x in watchlist]
  
  # load users
  users = {}
  with open(ADVERTISERS_FILENAME) as file:
    data = json.load(file)
  for user_id in data:
    user = User(data[user_id], user_id)
    users[user.id] = user
  
  # setup logging
  logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
  logger = logging.getLogger(__name__)
  logger.setLevel(logging.INFO)
  handler = tg_logger.setup(logger, token=TELE_TOKEN, users=TELE_USERS)
  handler.setFormatter(logging.Formatter('%(message)s'))
  
  # choose mode
  if mode == 1:
    updater = BareBonesUpdater(logger)
  else:
    updater = BareBonesUpdater(logger)
  
  main(logger, users, updater)

  
  
  
  