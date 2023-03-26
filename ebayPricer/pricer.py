import decimal
import os

from bson.decimal128 import Decimal128

import oauth_refresh_token

from ebaysdk.finding import Connection as Connection_finding

from ebayPricer.data_objects import update_item_list_record
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
        self.finding_api = None
        self.shopping_api = None
        self.exact_match_fields = None
        self.item_list = None
        self.important_fields = None
        self.conditional_fields = None
        self.excluded_search_terms = None
        self.category_id = None
        self.decider_field = None
        self.token = None

    def set_args(self, args):
        CONF_FILE = os.path.join(os.getcwd(), 'config', 'ebay.yaml')
        self.token = oauth_refresh_token.OAuthRefreshToken.get_token(config_file=CONF_FILE)
        self.finding_api = Connection_finding(config_file=CONF_FILE, siteid="EBAY-US")
        self.shopping_api = Connection_shopping(config_file=CONF_FILE, https=True)
        self.exact_match_fields = args.get('exact_match_fields', [])
        self.item_list = args.get('item_list', [])
        self.important_fields = args.get('important_fields', [])
        self.conditional_fields = args.get('conditional_fields', [])
        self.excluded_search_terms = args.get('excluded_search_terms', [])
        self.category_id = args.get('category_id', 29504)
        self.decider_field = args.get('decider_field', None)

    def get_private_paginated_listing(self, args):
        self.set_args(self, args)

        # TODO: Break this up into batches of 20s
        for item in self.item_list:
            list_value = {}
            keyword = ''
            ebay_matches = []

            if self.decider_field is not None and bool(item[self.decider_field]):
                for field in self.conditional_fields:
                    try:
                        keyword += item[field] + ' '
                    except KeyError as e:
                        # Not all conditional fields will be supplied, but we want to fetch them anyway for mining
                        pass

            for field in self.exact_match_fields:
                try:
                    keyword += item[field] + ' '
                except Exception as e:
                    print(e)

            # Apply not logic in the keyword search field for terms we want to exclude
            if len(self.excluded_search_terms) > 0:
                keyword += '-(' + ','.join(self.excluded_search_terms) + ')'

            print('Searching for %s' % keyword)
            request = {
                'keywords': keyword,
                'itemFilter': [
                    {'name': 'categoryId', 'value': self.category_id},
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
                # Sometimes, there are no items
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
                        item_details = {'title': found_item.title,
                                        'url': found_item.viewItemURL,
                                        'price': Decimal128(found_item.sellingStatus.convertedCurrentPrice.value),
                                        'currency': found_item.sellingStatus.convertedCurrentPrice._currencyId,
                                        'galleryUrl': found_item.galleryURL}
                        ebay_matches.append(item_details)

                        # Save the itemId and price to DB for future fetch

                if high_item is not None and high_item != low_item:
                    item['high'] =  {'title': high_item.title,
                                     'url': high_item.viewItemURL,
                                     'price': Decimal128(high_item.sellingStatus.convertedCurrentPrice.value),
                                     'currency': high_item.sellingStatus.convertedCurrentPrice._currencyId,
                                     'galleryUrl': high_item.galleryURL}
                    item['low'] = {'title': low_item.title,
                                   'url': low_item.viewItemURL,
                                   'price': Decimal128(low_item.sellingStatus.convertedCurrentPrice.value),
                                   'currency': low_item.sellingStatus.convertedCurrentPrice._currencyId,
                                   'galleryUrl': low_item.galleryURL}

                r = {
                    'ItemID': item_id_list,
                    'IncludeSelector': 'ItemSpecifics',
                    'token': self.token['access_token']
                }

                shopping_response = self.shopping_api.execute('GetMultipleItems', data=r)
                if shopping_response.reply.Ack == 'Success':
                    for shopping_item in shopping_response.reply.Item:
                        exact_matches = []
                        fuzzy_matches = []

                        try:
                            specifics = shopping_item.ItemSpecifics
                            if specifics is not None:
                                itemMap = {}
                                match_map = {}

                                if (isinstance(specifics.NameValueList, list)) and len(specifics.NameValueList) > 0:
                                    matched_fields = self.exact_match_fields.copy()
                                    for entry in specifics.NameValueList:
                                        if entry.Name in self.important_fields:
                                            itemMap[entry.Name] = entry.Value
                                        if bool(item[self.decider_field]) and entry.Name in self.conditional_fields:
                                            itemMap[entry.Name] = entry.Value
                                            matched_fields.append(entry.Name)

                                        if entry.Name in self.exact_match_fields:
                                            match_map[entry.Name] = entry.Value

                                    if all(elem in match_map.keys() for elem in self.exact_match_fields) \
                                            and compareMaps(itemMap, item, matched_fields):
                                        # print('Exact Match! %s' % shopping_item.Title)
                                        # print(shopping_item.ConvertedCurrentPrice)
                                        item_details = {'title': shopping_item.Title,
                                                        'url': shopping_item.ViewItemURLForNaturalSearch,
                                                        'price': Decimal128(shopping_item.ConvertedCurrentPrice.value)}

                                        exact_matches.append(item_details)

                                    else:
                                        item_details = {'title': shopping_item.Title,
                                                        'url': shopping_item.ViewItemURLForNaturalSearch,
                                                        'price': Decimal128(shopping_item.ConvertedCurrentPrice.value)}
                                        fuzzy_matches.append(item_details)

                        except AttributeError:
                            pass
                        except KeyError:
                            pass

                if len(prices) > 0:
                    mean_price = mean(prices)
                    median_price = median(prices)
                    mode_price = mode(prices)
                    comps = {'exact_matches': exact_matches, 'fuzzy_matches': fuzzy_matches,
                             'ebay_matches': ebay_matches}

                    list_value['mean'] = Decimal128(str(mean_price))
                    list_value['median'] = Decimal128(str(median_price))
                    list_value['mode'] = Decimal128(str(mode_price))
                    list_value['low'] = Decimal128(str(low))
                    list_value['high'] = Decimal128(str(high))

                    item['comps'] = comps
                    item['price_data'] = {'pricing_summary': list_value}
                    update_item_list_record(item)

            else:
                print('Not found: %s', request['keywords'])
                break

    @classmethod
    def get_paginated_listing(cls, args):
        return cls.get_private_paginated_listing(cls, args)
