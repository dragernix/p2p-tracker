from abc import ABC, abstractmethod

class Updater(ABC):
  
  def __init__(self, logger) -> None:
    self.logger = logger
  
  @abstractmethod
  def update_user(self, user, data):
    pass
  
  # @abstractmethod
  # def log_user_changes(self, user, data):
  #   pass
  
  # @abstractmethod
  # def log_user_ad_changes(self, user, data):
  #   pass
  
  
class BareBonesUpdater(Updater):
  
  def __init__(self, logger) -> None:
    super().__init__(logger)
  
  def update_user(self, user, new_data):
    self.log_user_changes(user, new_data)
    self.log_user_ad_changes(user, new_data)
    
    
  def log_user_changes(self, user, new_data):
    cp = user.check_counterparty(new_data)
    ttl_buy = user.check_total_buy(new_data)
    ttl_sell = user.check_total_sell(new_data)
    mth_buy = user.check_month_buy(new_data)
    mth_sell = user.check_month_sell(new_data)
    
    if ttl_buy or mth_buy:
      self.logger.info(f"{user.name} just completed {max(ttl_buy, mth_buy)} BUY orders")
    
    if ttl_sell or mth_sell:
      self.logger.info(f"{user.name} just completed {max(ttl_sell, mth_sell)} SELL orders")
    
    if cp:
      self.logger.info(f"{user.name} has {cp} new counterparty")
      
  
  def log_user_ad_changes(self, user, new_data):
    buy_listed, sell_listed = user.check_ads_listed(new_data)
    buy_delisted, sell_delisted = user.check_ads_delisted(new_data)
    buy_increased, sell_increased = user.check_ads_increased(new_data)
    buy_decreased, sell_decreased = user.check_ads_decreased(new_data)
    
    for listed in buy_listed + sell_listed:
      self.logger.info(f"{listed['name']} LISTED {listed['tradeType']} order of {listed['change']} {listed['asset']} for {listed['price']} {listed['currency']}")

    for delisted in buy_delisted + sell_delisted:
      self.logger.info(f"{delisted['name']} DELISTED {delisted['tradeType']} order of {delisted['change']} {delisted['asset']} for {delisted['price']} {delisted['currency']}")

    for increased in buy_increased + sell_increased:
      self.logger.info(f"{increased['name']} ADDED {increased['change']} {increased['asset']} to {increased['tradeType']} order of {increased['price']} {increased['currency']}. New Total: {increased['quantity']} {increased['asset']}")

    for decreased in buy_decreased + sell_decreased:
      self.logger.info(f"{decreased['name']} DEPLETED {decreased['change']} {decreased['asset']} to {decreased['tradeType']} order of {decreased['price']} {decreased['currency']}. New Total: {decreased['quantity']} {decreased['asset']}")


class SummarisedUpdater(Updater):
  
  def __init__(self, logger) -> None:
    super().__init__(logger)
    self.sell_stacks = {}
    self.buy_stacks = {}
  
  def update_user(self, user, new_data):
    if user.id not in self.sell_stacks:
      self.sell_stacks[user.id] = stack()
      
    if user.id not in self.buy_stacks:
      self.buy_stacks[user.id] = stack()
      
    buys, sells = self.log_user_changes(user, new_data)
    self.update_user_ad_changes(user, new_data)
    self.log_ad_changes(user, buys, sells)
  
  def log_ad_changes(self, user, buys, sells):
    for i in range(buys):
      ad = self.buy_stacks[user.id].pop()
      if ad:
        # print(ad)
        self.logger.info(f"{ad['name']} CONFIRMED {ad['tradeType']} {ad['change']} {ad['asset']} FOR {ad['price']} {ad['currency']}")
    
    for i in range(sells):
      ad = self.sell_stacks[user.id].pop()
      if ad:
        # print(ad)
        self.logger.info(f"{ad['name']} CONFIRMED {ad['tradeType']} {ad['change']} {ad['asset']} FOR {ad['price']} {ad['currency']}")
    
    
  def log_user_changes(self, user, new_data):
    cp = user.check_counterparty(new_data)
    ttl_buy = user.check_total_buy(new_data)
    ttl_sell = user.check_total_sell(new_data)
    mth_buy = user.check_month_buy(new_data)
    mth_sell = user.check_month_sell(new_data)
    buys, sells = 0, 0
    
    if ttl_buy or mth_buy:
      buys = max(ttl_buy, mth_buy)
      # print(f"{user.name} has {str(buys)} new buys")
    if ttl_sell or mth_sell:
      sells = max(ttl_sell, mth_sell)
      # print(f"{user.name} has {str(sells)} new sells")
      
    
    if cp:
      self.logger.info(f"{user.name} has {cp} new counterparty")
    
    return buys, sells
  
  def update_user_ad_changes(self, user, new_data):
    buy_listed, sell_listed = user.check_ads_listed(new_data)
    buy_delisted, sell_delisted = user.check_ads_delisted(new_data)
    buy_increased, sell_increased = user.check_ads_increased(new_data)
    buy_decreased, sell_decreased = user.check_ads_decreased(new_data)
    
    for sold in sell_delisted + sell_decreased:
      self.sell_stacks[user.id].add(sold)
    
    for bought in buy_delisted + buy_decreased:
      self.buy_stacks[user.id].add(bought)

      

class stack:
  def __init__(self, size=5) -> None:
    self.size = size
    self.stack = []
  
  def add(self, item):
    while len(self.stack) >= self.size:
      self.stack.pop(0)
    self.stack.append(item)
  
  def pop(self):
    if self.stack:
      return self.stack.pop()
    return None

if __name__ == "__main__":
  s = stack()
  for i in range(10):
    s.add(i)
  for i in range(10):
    print(s.pop())