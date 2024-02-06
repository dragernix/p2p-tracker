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
      self.logger.info(f"{listed['name']} LISTED {listed['tradeType']} order of {listed['quantity']} {listed['asset']} for {listed['price']} {listed['currency']}")

    for delisted in buy_delisted + sell_delisted:
      self.logger.info(f"{delisted['name']} DELISTED {delisted['tradeType']} order of {delisted['quantity']} {delisted['asset']} for {delisted['price']} {delisted['currency']}")

    for increased in buy_increased + sell_increased:
      self.logger.info(f"{increased['name']} ADDED {increased['change']} {increased['asset']} to {increased['tradeType']} order of {increased['price']} {increased['currency']}. New Total: {increased['quantity']} {increased['asset']}")

    for decreased in buy_decreased + sell_decreased:
      self.logger.info(f"{decreased['name']} DEPLETED {decreased['change']} {decreased['asset']} to {decreased['tradeType']} order of {decreased['price']} {decreased['currency']}. New Total: {decreased['quantity']} {decreased['asset']}")
