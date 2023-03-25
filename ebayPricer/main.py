from bson import ObjectId

from ebayPricer import constants, data_objects
from ebayPricer.file_loader import ingest_excel_sheets
from pricer import EbayPricer


def price_items(args):
    return EbayPricer.get_paginated_listing(args)


def get_pricing_params():
    params = {}
    for param in constants.param_list:
        try:
            params[param['field']] = input('%s Default: %s' % (str(param['msg']), str(param['default'])))
            if params[param['field']] is None or params[param['field']] == '':
                params[param['field']] = param['default']
        except Exception as e:
            print(e)

    return params


def get_pricing_params_by_filter():
    params = get_pricing_params()
    # Common filter menu maybe? Publisher, Grading Authority, etc....
    params[constants.filter_param['field']] = input(
        '%s Default: %s' % (str(constants.filter_param['msg']), str(constants.filter_param['default'])))
    return params


def get_pricing_params_by_id():
    params = get_pricing_params()
    params[constants.id_param['field']] = ObjectId(
        input('%s Default: %s' % (str(constants.id_param['msg']), str(constants.id_param['default']))))
    return params


def main():
    goodbye = False

    while goodbye is False:
        print(constants.menulist)
        ans = input("What would you like to do? ")
        priced_items = None


        if ans == "1":
            files = ingest_excel_sheets()
            print("Loaded %s files " % len(files['loaded']))
            for file in files['loaded']:
                print(file)

            print("ignored %s files " % len(files['ignored']))
            for file in files['ignored']:
                print(file)

        elif ans == "2":
            params = get_pricing_params()
            items = data_objects.get_item_lists_from_db(None)
            args = {'item_list': items, 'important_fields': params['important_fields'],
                    'conditional_fields': params['conditional_fields'],
                    'category_id': params['category_id'], 'exact_match_fields': params['exact_match_fields'],
                    'decider_field': params['decider_field'],
                    'excluded_search_terms': params['excluded_search_terms']}
            priced_items = price_items(args)

        elif ans == "3":
            params = get_pricing_params_by_filter()
            args = {'item_list': params['item_list'], 'important_fields': params['important_fields'],
                    'conditional_fields': params['conditional_fields'],
                    'category_id': params['category_id'], 'exact_match_fields': params['exact_match_fields'],
                    'decider_field': params['decider_field'],
                    'excluded_search_terms': params['excluded_search_terms']}
            priced_items = price_items(args)

        elif ans == "4":
            params = get_pricing_params_by_id()
            items = [data_objects.get_item_list_from_db({'_id': params['_id']})]
            args = {'item_list': items, 'important_fields': params['important_fields'],
                    'conditional_fields': params['conditional_fields'],
                    'category_id': params['category_id'], 'exact_match_fields': params['exact_match_fields'],
                    'decider_field': params['decider_field'],
                    'excluded_search_terms': params['excluded_search_terms']}
            priced_items = price_items(args)

        # elif ans == "5":
        #     files = update_excel_sheets()
        #     print("Updated %s files " % len(files['loaded']))
        #     for file in files['loaded']:
        #         print(file)
        #
        #     print("ignored %s files " % len(files['ignored']))
        #     for file in files['ignored']:
        #         print(file)

        elif ans == "9":
            goodbye = True
            print("good bye")

        if priced_items is not None:
            data_objects.add_item_list_records(priced_items)


if __name__ == "__main__":
    main()
