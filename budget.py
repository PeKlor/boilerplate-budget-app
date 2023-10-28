class Category:

  category_name = ""
  ledger = []
  
  def __init__(self, category_name):
    self.category_name = category_name
    self.ledger = []

  def deposit(self, amount, description = ""):
    self.ledger.append({"amount": amount, "description": description})

  def withdraw(self, amount, description = ""):
    if self.check_funds(amount):
      self.ledger.append({"amount": (-1) * amount, "description": description})
      return True
    return False

  def get_balance(self):
    total_balance = 0
    for dict in self.ledger:
      total_balance = total_balance + dict["amount"]
    return total_balance
      

  def transfer(self, amount, another_category):
    if self.check_funds(amount):
      other_description = "Transfer to " + another_category.category_name
      self.ledger.append({"amount": (-1) * amount, "description": other_description})

      another_category.deposit(amount, "Transfer from " + self.category_name)
      return True
    return False 

  def check_funds(self, amount):
    if amount > self.get_balance():
      return False
    return True

  def __str__(self):
    
    title_line_string = "{:*^30}".format(self.category_name) + "\n"

    ledger_item_lines = ""
    total_amount = 0
    for transaction in self.ledger:
      number = "{:>7.2f}".format(transaction["amount"])
      if len(transaction["description"]) > 23:
        line = f"{transaction['description']:.23}" + number
      else:
        line = "{:<23}".format(transaction["description"]) + number
      ledger_item_lines += line + "\n"
      total_amount += float(number)
    
    total_line = "Total: " + str(total_amount)

    all_strings = title_line_string + ledger_item_lines + total_line
    
    return all_strings


  def calculate_spend(self):
    total_money_spend = 0
    for dict in self.ledger:
      if dict["amount"] < 0:
        total_money_spend += dict["amount"]*(-1)

    return total_money_spend
      

def create_spend_chart(categories):

  output = "Percentage spent by category\n"
  perc = 100
  perc_lines = ""
  
  spend_bars = []
  total_spend = 0
  for cat in categories:
    category_spend = cat.calculate_spend()
    spend_bars.append(category_spend)
    total_spend += category_spend

  perc_bars = []
  for amount in spend_bars:
    perc_bars.append(100*amount//total_spend)

  while perc >= 0:
    perc_lines += "{:>3}".format(perc) + "| "
    for bar in perc_bars:
      if bar >= perc:
        perc_lines += "o  "
      else:
        perc_lines += "   "
    perc_lines += "\n"
    perc -= 10

  output += perc_lines + "    -" + len(categories)*"---"

  names = []
  for category in categories:
    names.append(category.category_name)

  max_name_length = 0
  for name in names:
    if len(name) > max_name_length:
      max_name_length = len(name)
  
  name_lines = ""
  
  letter = 0
  done = False
  while not done:
    name_lines += "\n     "
    for name in names:
      if letter < len(name):
        name_lines += name[letter] + "  "
      else:
        name_lines += "   "
    letter += 1
    if letter == max_name_length:
      done = True

  output += name_lines

  return output