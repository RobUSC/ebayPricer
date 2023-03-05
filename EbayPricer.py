#!/usr/bin/env python3
import decimal
import re
import oauth_refresh_token

from ebaysdk.finding import Connection as Connection_finding
from oauth_shopping_connection import OAuthShoppingConnection as Connection_shopping
from statistics import mean, median, mode


class EbayPricer(object):
    finding_api = Connection_finding(config_file='ebay.yaml', siteid="EBAY-US")
    shopping_api = Connection_shopping(config_file='ebay.yaml', https=True)

    comic_list = [
        {'publisher': 'Image', 'title': 'Invincible', 'issue_number': '1', 'graded': 'true', 'grade': '9.6'},
        {'publisher': 'Marvel', 'title': 'Amazing Spider-Man', 'issue_number': '300', 'graded': 'true', 'grade': '9.2'},
        {'publisher': 'DC', 'title': 'Batman', 'issue_number': '423', 'graded': 'false', 'grade': ''},
        {'publisher': 'Marvel', 'title': 'Incredible Hulk', 'issue_number': '181', 'graded': 'false', 'grade': '9.0'},
        {'publisher': 'Image', 'title': 'Invincible', 'issue_number': '2', 'graded': 'false', 'grade': ''},
        {'publisher': 'Image', 'title': 'Invincible', 'issue_number': '3', 'graded': 'false', 'grade': ''},
        {'publisher': 'Image', 'title': 'Invincible', 'issue_number': '4', 'graded': 'false', 'grade': ''},
        {'publisher': 'Marvel', 'title': 'Invincible', 'issue_number': 'X', 'graded': 'true', 'grade': ''},
        {'publisher': 'Marvel', 'title': 'Batman', 'issue_number': '999999', 'graded': 'false', 'grade': '9.8'},
        {'publisher': 'Marvel', 'title': 'X-Force', 'issue_number': '1', 'graded': 'true', 'grade': '9.8'}
    ]

    important_fields = ['Series Title',
                        'Issue Number',
                        'Publisher',
                        'Publication Year',
                        'Unit of Sale',
                        'Variant Type',
                        'Type',
                        'Format',
                        'Era']
    graded_fields = ['Certification Number',
                     'Professional Grader',
                     'Grade']

    start = decimal.Decimal(0)
    category_id = 259104
    collection_value = {'mean': start, 'median': start, 'mode': start, 'low': start, 'high': start}

    def getPrices(self):
        token = oauth_refresh_token.OAuthRefreshToken.get_token(oauth_refresh_token.OAuthRefreshToken)
        for comic in self.comic_list:
            match = False
            grade = ''
            graded = comic['graded'] == 'true'
            publisher = comic['publisher']
            title = comic['title']
            issue_number = comic['issue_number']

            if graded:
                grade = 'cgc ' + comic['grade']

            keyword = '%s %s %s %s' % (publisher, title, issue_number, grade)
            print('Searching for %s' % keyword)
            request = {
                'keywords': keyword,
                'itemFilter': [
                    {'name': 'categoryId', 'value': self.category_id},
                    {'name': 'categoryId', 'value': '259104'},
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
            itemId_list = []

            if int(response.reply.searchResult._count) > 0:
                for item in response.reply.searchResult.item:

                    if item is not None:
                        price = decimal.Decimal(item.sellingStatus.currentPrice.value)
                        if price > high:
                            high = price
                            high_item = item

                        if price < low:
                            low = price
                            low_item = item

                        prices.append(price)
                        itemId_list.append(item.itemId)
                        # Save the itemId and price to DB for future fetch

                if high_item is not None and high_item != low_item:
                    print('High item price is % and located at %s' % (high, high_item.viewItemURL))
                    print('Low item price is % and located at %s' % (low, low_item.viewItemURL))

                r = {
                    'ItemID': itemId_list,
                    'IncludeSelector': 'ItemSpecifics',
                    'token': token['access_token']
                }

                shopping_response = self.shopping_api.execute('GetMultipleItems', data=r,)
                if shopping_response.reply.Ack == 'Success':
                    for shopping_item in shopping_response.reply.Item:
                        try:
                            specifics = shopping_item.ItemSpecifics
                            if specifics is not None:
                                itemMap = {}
                                nameValueList = shopping_item.ItemSpecifics.NameValueList
                                for entry in nameValueList:
                                    if entry.Name in self.important_fields:
                                        itemMap[entry.Name] = entry.Value
                                    if graded and entry.Name in self.graded_fields:
                                        itemMap[entry.Name] = entry.Value
                                    if entry.Name == 'Publisher':
                                        shopping_item_publisher = entry.Value
                                    if entry.Name == 'Series Title':
                                        shopping_item_series_title = entry.Value
                                    if entry.Name == 'Issue Number':
                                        shopping_item_issue_number = entry.Value

                                if shopping_item_series_title is not None \
                                        and shopping_item_publisher is not None \
                                        and shopping_item_issue_number is not None \
                                        and re.search(shopping_item_publisher, publisher, re.IGNORECASE) \
                                        and re.search(shopping_item_series_title, title, re.IGNORECASE) \
                                        and issue_number == shopping_item_issue_number:
                                    print('Exact Match! %s' % shopping_item.Title)
                                    # print('Details %s' % itemMap)
                                    print(shopping_item.ConvertedCurrentPrice)
                                    match = True
                                else:
                                    # This is a fuzzy match from ebay We'll try to parse the details from the listing title
                                    # and whatever values are supplied in the itemSpecifics
                                    # Things to consider: Facsimile, Homages (not the studio), Lots, Trades
                                    shopping_item_title = shopping_item.Title
                                    if not re.search(shopping_item_title, 'facsimile', re.IGNORECASE) \
                                            and not re.search(shopping_item_title, 'homage', re.IGNORECASE):
                                        print('eBay Match %s' % shopping_item_title)
                                        # print('Details %s' % itemMap)
                                        # print(shopping_item.ConvertedCurrentPrice)

                                        # if re.search(title, shopping_item_title, re.IGNORECASE):
                                        # print('List Title %s contains search title %s'
                                        #       % (shopping_item_title, title))

                                        # if re.search(issue_number, shopping_item_title, re.IGNORECASE):
                                        # print('List Title %s contains issue number %s'
                                        #       % (shopping_item_title, issue_number))
                                        match = True

                        except Exception as e:
                            print(e)

                if match and len(prices) > 0:
                    mean_price = mean(prices)
                    median_price = median(prices)
                    mode_price = mode(prices)

                    self.collection_value['mean'] = self.collection_value['mean'] + mean_price
                    self.collection_value['median'] = self.collection_value['median'] + median_price
                    self.collection_value['mode'] = self.collection_value['mode'] + mode_price
                    self.collection_value['low'] = self.collection_value['low'] + low
                    self.collection_value['high'] = self.collection_value['high'] + high

            else:
                print('Not found: %s', request['keywords'])
                break

            print('Comic %s has pricing of mean: %s median: %s mode: %s low: %s high: %s' %
                  (comic, mean_price, median_price, mode_price, low, high))
            print('=======================================================================')

        print('final pricing:\n%s' % self.collection_value)
