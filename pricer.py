import decimal
import re

import oauth_refresh_token

from ebaysdk.finding import Connection as Connection_finding
from oauth_shopping_connection import OAuthShoppingConnection as Connection_shopping
from statistics import mean, median, mode


def compareMaps(map1, map2, keys):
    for key in keys:
        if map1[key] != map2[key]:
            if not map1[key].__contains__(map2[key]):
                return False
    return True


class EbayPricer:

    def __init__(self):
        self.finding_api = None
        self.shopping_api = None
        self.list_value = {}

    def getPrivatePaginatedListing(self, args):
        self.finding_api = Connection_finding(config_file='ebay.yaml', siteid="EBAY-US")
        self.shopping_api = Connection_shopping(config_file='ebay.yaml', https=True)
        self.list_value = {'mean': 0, 'median': 0, 'mode': 0, 'low': 0, 'high': 0}
        exact_match_fields = args.get('exact_match_fields', [])
        item_list = args.get('item_list', [])
        important_fields = args.get('important_fields', [])
        conditional_fields = args.get('conditional_fields', [])
        category_id = args.get('category_id', 29504)
        decider_field = args.get('decider_field', None)

        token = oauth_refresh_token.OAuthRefreshToken.get_token()
        for item in item_list:
            match = False

            keyword = ''

            if decider_field is not None and bool(item[decider_field]):
                for field in conditional_fields:
                    try:
                        keyword += item[field] + ' '
                    except KeyError as e:
                       # Not all conditional fields will be supplied, but we want tyo fetch them anyway for mining
                       pass

            for field in exact_match_fields:
                try:
                    keyword += item[field] + ' '
                except Exception as e:
                    print(e)

            print('Searching for %s' % keyword)
            request = {
                'keywords': keyword,
                'itemFilter': [
                    {'name': 'categoryId', 'value': category_id},
                ],
                'paginationInput': {
                    'entriesPerPage': 20,
                    'pageNumber': 1
                },
                # 'sortOrder': 'PricePlusShippingLowest'
            }

            response = self.finding_api.execute('findItemsAdvanced', request)

            high = decimal.Decimal(0)
            low = decimal.Decimal(99999999999.99)
            prices = []
            item_id_list = []

            size = 0
            try:
               size = len(response.reply.searchResult.item)
            except AttributeError as e:
                #Sometimes, there are no items
                pass

            if size > 0:
                for found_item in response.reply.searchResult.item:

                    if found_item is not None:
                        price = decimal.Decimal(found_item.sellingStatus.currentPrice.value)
                        if price > high:
                            high = price
                            high_item = found_item

                        if price < low:
                            low = price
                            low_item = found_item

                        prices.append(price)
                        item_id_list.append(found_item.itemId)
                        # Save the itemId and price to DB for future fetch

                if high_item is not None and high_item != low_item:
                    print('High item price is % and located at %s' % (high, high_item.viewItemURL))
                    print('Low item price is % and located at %s' % (low, low_item.viewItemURL))

                r = {
                    'ItemID': item_id_list,
                    'IncludeSelector': 'ItemSpecifics',
                    'token': token['access_token']
                }

                shopping_response = self.shopping_api.execute('GetMultipleItems', data=r, )
                if shopping_response.reply.Ack == 'Success':
                    for shopping_item in shopping_response.reply.Item:
                        try:
                            specifics = shopping_item.ItemSpecifics
                            if specifics is not None:
                                itemMap = {}
                                match_map = {}

                                if (isinstance(specifics.NameValueList, list)) and len(specifics.NameValueList) > 0:
                                    matched_fields = exact_match_fields.copy()
                                    for entry in specifics.NameValueList:
                                        if entry.Name in important_fields:
                                            itemMap[entry.Name] = entry.Value
                                        if bool(item[decider_field]) and entry.Name in conditional_fields:
                                            itemMap[entry.Name] = entry.Value
                                            matched_fields.append(entry.Name)

                                        if entry.Name in exact_match_fields:
                                            match_map[entry.Name] = entry.Value

                                    if all(elem in match_map.keys() for elem in exact_match_fields) \
                                            and compareMaps(itemMap, item, matched_fields):
                                        # print('Exact Match! %s' % shopping_item.Title)
                                        # print(shopping_item.ConvertedCurrentPrice)
                                        match = True
                                    else:
                                        # TODO: Remove comic specific handling and take from a supplied list of blockwords
                                        # This is a fuzzy match from ebay. We'll try to parse the details from the listing title
                                        # and whatever values are supplied in the itemSpecifics.
                                        # Things to consider: Facsimile, Homages (not the studio), Lots, Trades
                                        shopping_item_title = shopping_item.Title
                                        if not re.search(shopping_item_title, 'facsimile', re.IGNORECASE) \
                                                and not re.search(shopping_item_title, 'homage', re.IGNORECASE):
                                            # print('eBay Match %s' % shopping_item_title)
                                            match = True

                        except AttributeError:
                            pass
                        except KeyError:
                            pass

                if match and len(prices) > 0:
                    mean_price = mean(prices)
                    median_price = median(prices)
                    mode_price = mode(prices)

                    self.list_value['mean'] = self.list_value['mean'] + mean_price
                    self.list_value['median'] = self.list_value['median'] + median_price
                    self.list_value['mode'] = self.list_value['mode'] + mode_price
                    self.list_value['low'] = self.list_value['low'] + low
                    self.list_value['high'] = self.list_value['high'] + high

            else:
                print('Not found: %s', request['keywords'])
                break

            print('Comic %s has pricing of mean: %s median: %s mode: %s low: %s high: %s' %
                  (item, mean_price, median_price, mode_price, low, high))
            print('=======================================================================')

        print('final pricing:\n%s' % self.list_value)

    @classmethod
    def getPaginatedListing(cls, args):
        return cls.getPrivatePaginatedListing(cls, args)
