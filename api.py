from ebaysdk.finding import Connection as finding
import schedule
from data.users import User
from data import db_session


# keywords = ''
# api = finding(appid='', config_file=None)
# api_request = {'keywords': keywords,
#                'outputSelector': 'UnitPriceInfo'
#                }
# response = api.execute('findItemsByKeywords', api_request)
# items = response.dict()["searchResult"]["item"]
# for item in items:
#     print(item["sellingStatus"]["currentPrice"]["value"], item["viewItemURL"])

def find_product_price(keywords):
    api = finding(appid='', config_file=None)
    api_request = {'keywords': keywords,
                   'outputSelector': 'UnitPriceInfo'
                   }
    response = api.execute('findItemsByKeywords', api_request)
    items = response.dict()["searchResult"]["item"]
    return items


def check_price():
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        for product in user.products:
            user_price = int(product.price)
            items = find_product_price(product.product)
            for item in items:
                if int(item["sellingStatus"]["currentPrice"]["value"]) <= user_price:
                    print(item["viewItemURL"])
                    break


schedule.every().day.at("10:00").do(check_price)

while True:
    schedule.run_pending()
