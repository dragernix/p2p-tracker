from collections import defaultdict
from abc import ABC, abstractmethod

class User(ABC):
  
  @property
  @abstractmethod
  def data(self):
    pass
  
  @abstractmethod
  def check_counterparty(self, data):
    pass
  
  @abstractmethod
  def check_total_buy(self, data):
    pass
  
  @abstractmethod
  def check_total_sell(self, data):
    pass
  
  @abstractmethod
  def check_month_buy(self, data):
    pass
  
  @abstractmethod
  def check_month_sell(self, data):
    pass
  
  @abstractmethod
  def check_ads_listed(self, data):
    pass
  
  @abstractmethod
  def check_ads_delisted(self, data):
    pass
  
  @abstractmethod
  def check_ads_decreased(self, data):
    pass
  
  @abstractmethod
  def check_ads_increased(self, data):
    pass


class BinanceUser(User):
  def __init__(self, data, id=None) -> None:
    self._data = data
    self.id = data["userNo"]
    self.name = data["nickName"]
    self.counterparty = data["counterpartyCount"]
    self.total_buy_count = data["completedBuyOrderNum"]
    self.total_sell_count = data["completedSellOrderNum"]
    self.month_buy_count = data["completedBuyOrderNumOfLatest30day"]
    self.month_sell_count = data["completedSellOrderNumOfLatest30day"]
    self.total_buy_amt_btc = data["completedBuyOrderTotalBtcAmount"]
    self.total_sell_amt_btc = data["completedSellOrderTotalBtcAmount"]
    self.buy_list = data["buy_list"]
    self.sell_list = data["sell_list"]
  
  @property
  def data(self):
    return self._data
  
  @data.setter
  def data(self, data):
    self.counterparty = data["counterpartyCount"]
    self.total_buy_count = data["completedBuyOrderNum"]
    self.total_sell_count = data["completedSellOrderNum"]
    self.month_buy_count = data["completedBuyOrderNumOfLatest30day"]
    self.month_sell_count = data["completedSellOrderNumOfLatest30day"]
    self.total_buy_amt_btc = data["completedBuyOrderTotalBtcAmount"]
    self.total_sell_amt_btc = data["completedSellOrderTotalBtcAmount"]
    self.buy_list = data["buy_list"]
    self.sell_list = data["sell_list"]
    self._data = data
    
  def check_counterparty(self, data):
    return data["counterpartyCount"] - self.counterparty
  
  def check_total_buy(self, data):
    if data["completedBuyOrderNum"] - self.total_buy_count > 0:
        return data["completedBuyOrderNum"] - self.total_buy_count
    return 0
  
  def check_total_sell(self, data):
    if data["completedSellOrderNum"] - self.total_sell_count > 0:
      return data["completedSellOrderNum"] - self.total_sell_count
    return 0
  
  def check_month_buy(self, data):
    if data["completedBuyOrderNumOfLatest30day"] - self.month_buy_count > 0:
      return data["completedBuyOrderNumOfLatest30day"] - self.month_buy_count
    return 0
  
  def check_month_sell(self, data):
    if data["completedSellOrderNumOfLatest30day"] - self.month_sell_count > 0:
      return data["completedSellOrderNumOfLatest30day"] - self.month_sell_count
    return 0
  
  def check_ads_listed(self, data):
    new_buy = data["buy_list"]
    new_sell = data["sell_list"]
    buy_changed = []
    sell_changed = []
    for ad_no in new_buy:
      if ad_no not in self.buy_list:
        buy_changed.append({"name": self.name,
                            "adNo": new_buy[ad_no],
                            "asset": new_buy[ad_no]["asset"],
                            "currency": new_buy[ad_no]["fiatUnit"],
                            "price": new_buy[ad_no]["price"],
                            "quantity": new_buy[ad_no]["tradableQuantity"],
                            "tradeType": new_buy[ad_no]["tradeType"]
                            })
    
    for ad_no in new_sell:
      if ad_no not in self.sell_list:
        sell_changed.append({"name": self.name,
                            "adNo": new_sell[ad_no],
                            "asset": new_sell[ad_no]["asset"],
                            "currency": new_sell[ad_no]["fiatUnit"],
                            "price": new_sell[ad_no]["price"],
                            "quantity": new_sell[ad_no]["tradableQuantity"],
                            "tradeType": new_sell[ad_no]["tradeType"]
                            })

    if buy_changed or sell_changed:
      return buy_changed, sell_changed
    return [], []
    
  
  def check_ads_delisted(self, data):
    new_buy = data["buy_list"]
    new_sell = data["sell_list"]
    buy_changed = []
    sell_changed = []
    
    for ad_no in self.buy_list:
      if ad_no not in new_buy:
        buy_changed.append({"name": self.name,
                            "adNo": self.buy_list[ad_no],
                            "asset": self.buy_list[ad_no]["asset"],
                            "currency": self.buy_list[ad_no]["fiatUnit"],
                            "price": self.buy_list[ad_no]["price"],
                            "quantity": self.buy_list[ad_no]["tradableQuantity"],
                            "tradeType": self.buy_list[ad_no]["tradeType"]
                            })
    
    for ad_no in self.sell_list:
      if ad_no not in new_sell:
        sell_changed.append({"name": self.name,
                            "adNo": self.sell_list[ad_no],
                            "asset": self.sell_list[ad_no]["asset"],
                            "currency": self.sell_list[ad_no]["fiatUnit"],
                            "price": self.sell_list[ad_no]["price"],
                            "quantity": self.sell_list[ad_no]["tradableQuantity"],
                            "tradeType": self.sell_list[ad_no]["tradeType"]
                            })
    
    if buy_changed or sell_changed:
      return buy_changed, sell_changed
    return [], []

  
  def check_ads_decreased(self, data):
    new_buy = data["buy_list"]
    new_sell = data["sell_list"]
    buy_changed = []
    sell_changed = []
    
    for ad_no in new_buy:
      if ad_no not in self.buy_list:
        continue
      decrease = float(self.buy_list[ad_no]["tradableQuantity"]) - float(new_buy[ad_no]["tradableQuantity"])
      if decrease > 0:
        buy_changed.append({"name": self.name,
                            "adNo": new_buy[ad_no],
                            "asset": new_buy[ad_no]["asset"],
                            "currency": new_buy[ad_no]["fiatUnit"],
                            "price": new_buy[ad_no]["price"],
                            "quantity": new_buy[ad_no]["tradableQuantity"],
                            "tradeType": new_buy[ad_no]["tradeType"],
                            "change": decrease
                            })
    
    for ad_no in new_sell:
      if ad_no not in self.sell_list:
        continue
      decrease = float(self.sell_list[ad_no]["tradableQuantity"]) - float(new_sell[ad_no]["tradableQuantity"])
      if decrease > 0:
        sell_changed.append({"name": self.name,
                            "adNo": new_sell[ad_no],
                            "asset": new_sell[ad_no]["asset"],
                            "currency": new_sell[ad_no]["fiatUnit"],
                            "price": new_sell[ad_no]["price"],
                            "quantity": new_sell[ad_no]["tradableQuantity"],
                            "tradeType": new_sell[ad_no]["tradeType"],
                            "change": decrease
                            })

    if buy_changed or sell_changed:
      return buy_changed, sell_changed
    return [], []
  
  
  def check_ads_increased(self, data):
    new_buy = data["buy_list"]
    new_sell = data["sell_list"]
    buy_changed = []
    sell_changed = []
    
    for ad_no in new_buy:
      if ad_no not in self.buy_list:
        continue
      increase = float(new_buy[ad_no]["tradableQuantity"]) - float(self.buy_list[ad_no]["tradableQuantity"])
      if increase > 0:
        buy_changed.append({"name": self.name,
                            "adNo": new_buy[ad_no],
                            "asset": new_buy[ad_no]["asset"],
                            "currency": new_buy[ad_no]["fiatUnit"],
                            "price": new_buy[ad_no]["price"],
                            "quantity": new_buy[ad_no]["tradableQuantity"],
                            "tradeType": new_buy[ad_no]["tradeType"],
                            "change": increase
                            })
    
    for ad_no in new_sell:
      if ad_no not in self.sell_list:
        continue
      increase = float(new_sell[ad_no]["tradableQuantity"]) - float(self.sell_list[ad_no]["tradableQuantity"])
      if increase > 0:
        sell_changed.append({"name": self.name,
                            "adNo": new_sell[ad_no],
                            "asset": new_sell[ad_no]["asset"],
                            "currency": new_sell[ad_no]["fiatUnit"],
                            "price": new_sell[ad_no]["price"],
                            "quantity": new_sell[ad_no]["tradableQuantity"],
                            "tradeType": new_sell[ad_no]["tradeType"],
                            "change": increase
                            })

    if buy_changed or sell_changed:
      return buy_changed, sell_changed
    return [], []


class HtxUser(User):
  trade_type = {1:"SELL", 0:"BUY"}
  def __init__(self, data, id) -> None:
    self._data = data
    self.id = id
    self.name = data["userName"]
    self.total_buy_count = data["tradeCountBuy"]
    self.total_sell_count = data["tradeCountSell"]
    self.month_buy_count = data["tradeMonthCountBuy"]
    self.month_sell_count = data["tradeMonthCountSell"]
    self.buy_list = data["buy_list"]
    self.sell_list = data["sell_list"]
  
  @property
  def data(self):
    return self._data
  
  @data.setter
  def data(self, data):
    self.total_buy_count = data["tradeCountBuy"]
    self.total_sell_count = data["tradeCountSell"]
    self.month_buy_count = data["tradeMonthCountBuy"]
    self.month_sell_count = data["tradeMonthCountSell"]
    self.buy_list = data["buy_list"]
    self.sell_list = data["sell_list"]
    self._data = data
  
  def check_counterparty(self, data):
    return 0
  
  def check_total_buy(self, data):
    if data["tradeCountBuy"] - self.total_buy_count > 0:
      return data["tradeCountBuy"] - self.total_buy_count
    return 0
  
  def check_total_sell(self, data):
    if data["tradeCountSell"] - self.total_sell_count > 0:
        return data["tradeCountSell"] - self.total_sell_count
    return 0
  
  
  def check_month_buy(self, data):
    if data["tradeMonthCountBuy"] - self.month_buy_count > 0:
      return data["tradeMonthCountBuy"] - self.month_buy_count
    return 0
  
  def check_month_sell(self, data):
    if data["tradeMonthCountSell"] - self.month_sell_count > 0:
      return data["tradeMonthCountSell"] - self.month_sell_count
    return 0
  
  def check_ads_listed(self, data):
    new_buy = data["buy_list"]
    new_sell = data["sell_list"]
    buy_changed = []
    sell_changed = []
    for ad_no in new_buy:
      if ad_no not in self.buy_list:
        buy_changed.append({"name": self.name,
                            "adNo": new_buy[ad_no],
                            "asset": new_buy[ad_no]["coinId"],
                            "currency": new_buy[ad_no]["currency"],
                            "price": new_buy[ad_no]["price"],
                            "quantity": new_buy[ad_no]["tradeCount"],
                            "tradeType": new_buy[ad_no]["tradeType"]
                            })
    
    for ad_no in new_sell:
      if ad_no not in self.sell_list:
        sell_changed.append({"name": self.name,
                            "adNo": new_sell[ad_no],
                            "asset": new_sell[ad_no]["coinId"],
                            "currency": new_sell[ad_no]["currency"],
                            "price": new_sell[ad_no]["price"],
                            "quantity": new_sell[ad_no]["tradeCount"],
                            "tradeType": new_sell[ad_no]["tradeType"]
                            })

    if buy_changed or sell_changed:
      return buy_changed, sell_changed
    return [], []
    
  
  def check_ads_delisted(self, data):
    new_buy = data["buy_list"]
    new_sell = data["sell_list"]
    buy_changed = []
    sell_changed = []
    
    for ad_no in self.buy_list:
      if ad_no not in new_buy:
        buy_changed.append({"name": self.name,
                            "adNo": self.buy_list[ad_no],
                            "asset": self.buy_list[ad_no]["coinId"],
                            "currency": self.buy_list[ad_no]["currency"],
                            "price": self.buy_list[ad_no]["price"],
                            "quantity": self.buy_list[ad_no]["tradeCount"],
                            "tradeType": self.buy_list[ad_no]["tradeType"]
                            })
    
    for ad_no in self.sell_list:
      if ad_no not in new_sell:
        sell_changed.append({"name": self.name,
                            "adNo": self.sell_list[ad_no],
                            "asset": self.sell_list[ad_no]["coinId"],
                            "currency": self.sell_list[ad_no]["currency"],
                            "price": self.sell_list[ad_no]["price"],
                            "quantity": self.sell_list[ad_no]["tradeCount"],
                            "tradeType": self.sell_list[ad_no]["tradeType"]
                            })
    
    if buy_changed or sell_changed:
      return buy_changed, sell_changed
    return [], []

  
  def check_ads_decreased(self, data):
    new_buy = data["buy_list"]
    new_sell = data["sell_list"]
    buy_changed = []
    sell_changed = []
    
    for ad_no in new_buy:
      if ad_no not in self.buy_list:
        continue
      decrease = float(self.buy_list[ad_no]["tradeCount"]) - float(new_buy[ad_no]["tradeCount"])
      if decrease > 0:
        buy_changed.append({"name": self.name,
                            "adNo": new_buy[ad_no],
                            "asset": new_buy[ad_no]["coinId"],
                            "currency": new_buy[ad_no]["currency"],
                            "price": new_buy[ad_no]["price"],
                            "quantity": new_buy[ad_no]["tradeCount"],
                            "tradeType": new_buy[ad_no]["tradeType"],
                            "change": decrease
                            })
    
    for ad_no in new_sell:
      if ad_no not in self.sell_list:
        continue
      decrease = float(self.sell_list[ad_no]["tradeCount"]) - float(new_sell[ad_no]["tradeCount"])
      if decrease > 0:
        sell_changed.append({"name": self.name,
                            "adNo": new_sell[ad_no],
                            "asset": new_sell[ad_no]["coinId"],
                            "currency": new_sell[ad_no]["currency"],
                            "price": new_sell[ad_no]["price"],
                            "quantity": new_sell[ad_no]["tradeCount"],
                            "tradeType": new_sell[ad_no]["tradeType"],
                            "change": decrease
                            })

    if buy_changed or sell_changed:
      return buy_changed, sell_changed
    return [], []
  
  
  def check_ads_increased(self, data):
    new_buy = data["buy_list"]
    new_sell = data["sell_list"]
    buy_changed = []
    sell_changed = []
    
    for ad_no in new_buy:
      if ad_no not in self.buy_list:
        continue
      increase = float(new_buy[ad_no]["tradeCount"]) - float(self.buy_list[ad_no]["tradeCount"])
      if increase > 0:
        buy_changed.append({"name": self.name,
                            "adNo": new_buy[ad_no],
                            "asset": new_buy[ad_no]["coinId"],
                            "currency": new_buy[ad_no]["currency"],
                            "price": new_buy[ad_no]["price"],
                            "quantity": new_buy[ad_no]["tradeCount"],
                            "tradeType": new_buy[ad_no]["tradeType"],
                            "change": increase
                            })
    
    for ad_no in new_sell:
      if ad_no not in self.sell_list:
        continue
      increase = float(new_sell[ad_no]["tradeCount"]) - float(self.sell_list[ad_no]["tradeCount"])
      if increase > 0:
        sell_changed.append({"name": self.name,
                            "adNo": new_sell[ad_no],
                            "asset": new_sell[ad_no]["coinId"],
                            "currency": new_sell[ad_no]["currency"],
                            "price": new_sell[ad_no]["price"],
                            "quantity": new_sell[ad_no]["tradeCount"],
                            "tradeType": new_sell[ad_no]["tradeType"],
                            "change": increase
                            })

    if buy_changed or sell_changed:
      return buy_changed, sell_changed
    return [], []

if __name__ == "__main__":

  def check_total_buy(new, old):
    return new - old

  def check_month_buy(new, old):
    if new - old > 0:
      return new - old
    return 0
  
  mth_old = 30
  mth_new = 28
  ttl_old = 30
  ttl_new = 30
  if check_month_buy(mth_new, mth_old) or check_total_buy(ttl_new, ttl_old):
    print(max(mth_new, ttl_new))
  
  diff1, diff2 = 0, -2
  if diff1 or diff2:
    print(max(diff1, diff2))
  # import copy
  # data = copy.deepcopy(data)
  # # data["completedSellOrderNum"] += 1
  # for ad in data["advList"]:
  #   # data["advList"][ad]["tradableQuantity"] = "1000000"
  #   # data["advList"][ad]["tradableQuantity"] = "10"
  #   data["advList"] = {}

  # update = usr.update(data)
  # for u in update:
  #   print(u)
  pass