import platform
import aiohttp
import asyncio
import sys
from datetime import timedelta
from datetime import date

async def fetch_currency(session, days):
   currencies = []
   for day in range(days, 0, -1):
      today = date.today() - timedelta(days=day)
      formatted_date = today.strftime('%d.%m.%Y')
      async with session.get(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={formatted_date}') as response:
         data = await response.json()
         eur = data['exchangeRate'][8]
         eur_format = {"EUR": {"sale": eur['saleRateNB'], "purchase": eur['purchaseRateNB']}}
         usd = data['exchangeRate'][23]
         usd_format = {"USD": {"sale": usd['saleRateNB'], "purchase": usd['purchaseRateNB']}}
         currencies.append({formatted_date: {"EUR": eur_format["EUR"], "USD": usd_format["USD"]}})
   return currencies 

async def main(days):
   async with aiohttp.ClientSession() as session:
      return await fetch_currency(session, days) 


if __name__ == "__main__":
   if len(sys.argv) != 2:
      print("Enter days (form 1 to 10)")
   
   try:
      days = int(sys.argv[1])
   except:
      print("Days must be integer")
      sys.exit(1)
      
   if days > 10 and days < 1:
      print("days must be form 1 to 10")

   if platform.system() == 'Windows':
      asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
   r = asyncio.run(main(days))
   print(r)
