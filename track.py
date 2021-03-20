import requests
import json
from apscheduler.schedulers.blocking import BlockingScheduler
import sys 

schedule = BlockingScheduler()
#ask for the  target gas price then run a sched job to keep checking for the price
print("Enter your target gas/gwei price: ")
price=int(input())

#when the target price is met send a notification
@schedule.scheduled_job('interval', seconds=5) #api has a rate of 5calls/second 
def checkgas():
    response = requests.get("https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=<YOURAPIKEYHERE>")
    data=response.json()
#print all data gathered from the API
    print("#============================================#")
    print("Last block: " + data['result']['LastBlock'])
    print("Safe gas price: " + data['result']['SafeGasPrice'])
    print("Proposed gas price: " + data['result']['ProposeGasPrice'])
    print("Fast gas price: " + data['result']['FastGasPrice'])
    print("#============================================#")

    currentgwei = int(data['result']['SafeGasPrice'])
    response2 = requests.get("https://api.etherscan.io/api?module=stats&action=ethprice&apikey=<YOURAPIKEYHERE>")
    data2=response2.json()
    ethusd = data2['result']['ethusd']

    #print current ethereum price in USD
    print("ETH: " + str(ethusd)+"USD")
    gweiusdprice = float((10**-9) * float(currentgwei) * float(ethusd))

    #print gwei usd price
    print("gwei: " + str(gweiusdprice) + "USD")
    if price == currentgwei:
      #alert if condition met
      
	  #DOSOMETHING/Send alert,do whatever you want
	  print("BEEP BOOP")
      #kill the thread
      sys.exit() 


checkgas()
schedule.start()