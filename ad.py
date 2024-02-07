class Ads:
  def __init__(self, data) -> None:
    self.data = None
    self.id = str(data["id"] if data.get("id") else data["advNo"])
    self.user_id = str(data["uid"] if data.get("uid") else data["userNo"])
    self.user_name = data["userName"] if data.get("userName") else data["nickName"]