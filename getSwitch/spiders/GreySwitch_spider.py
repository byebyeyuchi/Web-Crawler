import scrapy
import re
from scrapy.mail import MailSender
from twilio.rest import Client

class GreySwitch(scrapy.Spider):
    name = 'greyswitch'
    start_urls = [
        'https://www.bestbuy.ca/en-ca/product/nintendo-switch-console-with-grey-joy-con/13817626'
    ]

    def sendWhatsup(self,msg):
        TWILIO_ACCOUNT_SID="ACbf904f84a3d86d3ab355e41326f9a99f"
        TWILIO_AUTH_TOKEN="b6733f5ba23d717c129d63994eaadc72"

        client = Client()
        from_whatsapp_number = 'whatsapp:+14155238886'
        to_whatsapp_number='whatsapp:+8615107330160'

        if msg == "online":
            body = "Best Buy grey Switch is available online!!"
        if msg  == "store":
            body = "Best Buy grey Switch is available in store!!"
        
        client.messages.create(body=body, from_=from_whatsapp_number, to=to_whatsapp_number)
    

    def parse(self, response):
        online = response.xpath('/html/body/div[1]/div/div/div[4]/div[1]/div[2]/div[2]/div[5]/div/div[1]/div/div/span[2]/text()').extract() 
        store = response.xpath('/html/body/div[1]/div/div/div[4]/div[1]/div[2]/div[2]/div[5]/div/div[2]/div[1]/p/text()').extract()
    
        yield {
            'online' : ''.join(online),
            'store' : ''.join(store)
        }
        stock_online = not re.search("Sold out", ''.join(online))
        stock_store= not re.search("unavailable", ''.join(store))
        
        if stock_online:
            self.sendWhatsup('online')
        if stock_store:
            self.sendWhatsup('store')

