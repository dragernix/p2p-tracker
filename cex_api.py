import requests
import math
from abc import ABC, abstractmethod

class API(ABC):
  
  @abstractmethod
  def get_ad_list(self):
    """
    Returns a pair of list, ([buy_ads], [sell_ads])
    Each ad in list is a dict that contains props of ad AND advertiser 
    """
    pass
  
  @abstractmethod
  def get_user(self, user_id):
    """
    Returns a dict representing the user
    dict should contain all user props AND sellList and buyList of user
    key should be sellList, buyList respectively
    """
    pass

class BinanceAPI(API):
  binance_ad_url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
  binance_user_url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/user/profile-and-ads-list"
  
  headers = {
      "Accept": "*/*",
      "Accept-Encoding": "gzip, deflate, br",
      "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
      "Cache-Control": "no-cache",
      "Connection": "keep-alive",
      "Content-Length": "123",
      "content-type": "application/json",
      "Host": "p2p.binance.com",
      "Origin": "https://p2p.binance.com",
      "Pragma": "no-cache",
      "TE": "Trailers",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
  }

  payload = {"fiat":"BND","page":1,"rows":10,"tradeType":"BUY","asset":"USDT","countries":[],"proMerchantAds":False,"shieldMerchantAds":False,"publisherType":None,"payTypes":[],"classifies":["mass","profession"]}
  
  user_props = ["userNo", "nickName", "userStatsRet", "onlineStatus", "lastActiveTime", "activeTimeInSecond"]
  
  sell_props = ["advNo", "tradeType", "asset", "fiatUnit", "advStatus", "priceType", "priceFloatingRatio", "rateFloatingRatio", "currencyRate", "price", "initAmount", "surplusAmount", "amountAfterEditing", "maxSingleTransAmount", "minSingleTransAmount", "remarks", "createTime", "advUpdateTime", "dynamicMaxSingleTransAmount", "minSingleTransQuantity", "maxSingleTransQuantity", "dynamicMaxSingleTransQuantity", "tradableQuantity"]
  
  def _get_ad_list(self, **kwargs):
    """
    Returns:
        {adv:{}, advertiser:{}}
    """    
    data = self.payload.copy()
    for key, val in kwargs.items():
      data[key] = val
    req = requests.post(self.binance_ad_url, headers=self.headers, json=data)
    return req.json()
  
  def get_ad_list(self, **kwargs):
    buy_ads, sell_ads = [], []
    total, pg, rows = 1000, 1, 10
    while pg <= math.ceil(total/rows):
      buy_res = self._get_ad_list(tradeType="BUY", page=pg, **kwargs)
      buy_ads += buy_res["data"]
      total = buy_res["total"]
      pg += 1
    
    total, pg, rows = 1000, 1, 10
    while pg <= math.ceil(total/rows):
      sell_res = self._get_ad_list(tradeType="SELL", page=pg, **kwargs)
      sell_ads += sell_res["data"]
      total = sell_res["total"]
      pg += 1
      
    for i, ad in enumerate(buy_ads):
      for key in ad["advertiser"]:
        ad["adv"][key] = ad["advertiser"][key]
      ad["adv"]["rank"] = i
      buy_ads[i] = ad["adv"]

    for i, ad in enumerate(sell_ads):
      for key in ad["advertiser"]:
        ad["adv"][key] = ad["advertiser"][key]
      ad["adv"]["rank"] = i
      sell_ads[i] = ad["adv"]
      
    return buy_ads, sell_ads
  
  def _get_user(self, user_id):
    req = requests.get(self.binance_user_url, {"userNo":user_id})
    if not req.json()["success"]:
      raise Exception("Error getting user data")
    
    return req.json()["data"]
  
  def get_user(self, user_id):
    data = self._get_user(user_id)
    user, sell_list, buy_list = data['userDetailVo'], data['sellList'], data['buyList']
    
    user_stats = user["userStatsRet"]
    for key, item in user_stats.items():
      user[key] = item
    
    buy_dict = {ad["advNo"]: ad for ad in buy_list}
    sell_dict = {ad["advNo"]: ad for ad in sell_list}
    
    user["buy_list"] = buy_dict
    user["sell_list"] = sell_dict
    return user


class HtxAPI:
  ad_url = "https://www.htx.com/-/x/otc/v1/data/trade-market"
  user_url = "https://www.htx.com/-/x/otc/v1/user/{}/info"
  user_adlist_url = "https://www.htx.com/-/x/otc/v1/data/trade-list/{}?tradeType={}"
  
  ad_queries = {"coinId":2, "currency":3, "tradeType":"sell", "currPage":1, "payMethod":0, "acceptOrder":0, "country":None, "blockType":"general", "online":1, "range":0, "amount":None, "onlyTradable":False, "isFollowed":False}
  
  adlist_queries = {"tradeType": "SELL"}
  
  currency_list = { 1: "CNY", 2: "USD", 3: "SGD", 4: "INR", 5: "VND", 6: "CAD", 7: "AUD", 8: "KRW", 9: "CHF", 10: "TWD", 11: "RUB", 12: "GBP", 13: "HKD", 14: "EUR", 15: "NGN", 16: "IDR", 17: "PHP", 18: "KHR", 19: "BRL", 20: "SAR", 21: "AED", 22: "MYR", 23: "TRY", 24: "NZD", 25: "MMK", 26: "ZAR", 27: "NOK", 28: "DKK", 29: "SEK", 30: "ARS", 31: "THB", 32: "COP", 33: "VES", 34: "KES", 35: "PEN", 36: "BGN", 37: "CZK", 38: "HUF", 39: "ILS", 40: "JPY", 41: "MAD", 42: "MXN", 43: "PLN", 44: "RON", 45: "UAH", 46: "ALL", 47: "BAM", 48: "HRK", 49: "MDL", 50: "RSD", 51: "MKD", 52: "AZN", 53: "CLP", 54: "CRC", 55: "DOP", 56: "GEL", 57: "KZT", 58: "NAD", 59: "QAR", 60: "UYU", 61: "UZS", 65:"BDD", 67: "BDT"}
  
  coin_list = {2: "USDT", 1: "BTC", 3: "ETH", 4: "HT", 5: "EOS", 7: "XRP", 8: "LTC", 10: "BCH", 11: "ETC", 12: "BSV", 13: "DASH", 14: "HPT", 16: "LINK", 17: "DOT", 19: "FIL", 22: "TRX", 23: "ZEC", 24: "ADA", 25: "NEO", 26: "XLM", 27: "XMR", 28: "VET", 29: "DOGE", 30: "YFI", 31: "UNI", 32: "ALGO", 33: "XTZ", 38: "ICP", 39: "BRL", 40: "BAT", 41: "MANA", 42: "CHZ", 43: "SOL", 44: "LUNA", 45: "MATIC", 46: "AVAX", 47: "THETA", 48: "ATOM", 49: "AAVE", 50: "GRT", 51: "AXS", 52: "1INCH", 53: "CRV", 54: "NEAR", 55: "SHIB", 56: "COMP", 57: "SNX", 58: "DYDX", 59: "TRY"}
  
  trade_type_list = {0: "BUY", 1:"SELL"}

  
  def get_ad_list(self, **kwargs):
    payload = self.ad_queries.copy()
    for key, val in kwargs.items():
      payload[key] = val
    
    sell_ads, buy_ads = [], []
    
    # pg, nof_pg= 1, 100
    # payload["tradeType"] = "BUY"
    # payload["currPage"] = pg
    # while pg <= nof_pg:
    #   payload["currPage"] = pg
    #   buy_res = requests.get(self.ad_url, payload).json()
    #   buy_ads += buy_res["data"]
    #   nof_pg = buy_res["totalPage"]
    #   pg += 1
    
    pg, nof_pg= 1, 100
    payload["tradeType"] = "SELL"
    payload["currPage"] = pg
    while pg <= nof_pg:
      payload["currPage"] = pg
      sell_res = requests.get(self.ad_url, payload).json()
      sell_ads += sell_res["data"]
      nof_pg = sell_res["totalPage"]
      pg += 1

    return buy_ads, sell_ads
    
  def get_user(self, user_id):
    user = self._get_user(user_id)
    buy_list, sell_list = self._get_user_adlist(user_id)
    for ad in buy_list + sell_list:
      ad["tradeType"] = self.trade_type_list[ad["tradeType"]]
      ad["coinId"] = self.coin_list.get(ad["coinId"]) if self.coin_list.get(ad["coinId"]) else ad["coinId"]
      ad["currency"] = self.currency_list.get(ad["currency"]) if self.currency_list.get(ad["currency"]) else ad["currency"]
      ad["id"] = str(ad["id"])
      ad["uid"] = str(ad["uid"])
    buy_dict = {ad["id"]: ad for ad in buy_list}
    sell_dict = {ad["id"]: ad for ad in sell_list}
    user["buy_list"] = buy_dict
    user["sell_list"] = sell_dict
    return user
    
  def _get_user(self, user_id):
    res = requests.get(self.user_url.format(user_id))
    if not res.json()["success"]:
      raise Exception("Error getting user data! ")
    return res.json()["data"]
  
  def _get_user_adlist(self, user_id):
    sell_res = requests.get(self.user_adlist_url.format(user_id, "SELL"))
    buy_res = requests.get(self.user_adlist_url.format(user_id, "BUY"))
    if not sell_res.json()["success"] or not buy_res.json()["success"]:
      raise Exception("Error getting user's ad data!")
    return buy_res.json()["data"], sell_res.json()["data"]
  
  
if __name__ == "__main__":
  # bapi = BinanceAPI()
  # b, s = bapi.get_ad_list()
  # for ad in b:
  #   print("advNo", ad["advNo"])
  #   print("nickName", ad["nickName"])
  #   print("tradeType", ad["tradeType"])
  #   print("initAmount", ad["initAmount"])
  #   print("surplusAmount", ad["surplusAmount"])
  #   print("amountAfterEditing", ad["amountAfterEditing"])
  #   print("minSingleTransAmount", ad["minSingleTransAmount"])
  #   print("maxSingleTransAmount", ad["maxSingleTransAmount"])
  #   print("dynamicMaxSingleTransAmount", ad["dynamicMaxSingleTransAmount"])
  #   print("minSingleTransQuantity", ad["minSingleTransQuantity"])
  #   print("maxSingleTransQuantity", ad["maxSingleTransQuantity"])
  #   print("dynamicMaxSingleTransQuantity", ad["dynamicMaxSingleTransQuantity"])
  #   print("tradableQuantity", ad["tradableQuantity"])
  #   print("createTime", ad["createTime"])
  #   print("advUpdateTime", ad["advUpdateTime"])
  #   print()
  # u = bapi.get_user(b[0]["userNo"])
  # print(u["nickName"])
  # print(u["sell_list"])
  
  api = HtxAPI()
  b, s = api.get_ad_list()
  for ad in b+s:
    u = api.get_user(ad["uid"])
    print(u["userName"], len(u["buy_list"]), len(u["sell_list"]))
  # u = api.get_user("472994019")
  # for a in u["sell_list"]:
  #   print(a)
  # b, s = api.get_ad_list()
  # for ad in b:
  #   print(ad["userName"])
  #   print(ad["tradeType"])
  # print(len(b))
  # u = a[0]["uid"]
  # a = api.get_user(u)
  # print(a)
  # a = api.get_user_adlist(u)
  # print(a)