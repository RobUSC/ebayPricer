item_list = [
    {'publisher': 'Image', 'series_title': 'Invincible', 'issue_number': '1', 'graded': 'true',
     'Professional Grader': 'CGC', 'Grade': '9.6'},
    {'publisher': 'Marvel', 'series_title': 'Amazing Spider-Man', 'issue_number': '300', 'Professional Grader': 'CGC',
     'graded': 'true',
     'Grade': '9.2'},
    {'publisher': 'DC', 'series_title': 'Batman', 'issue_number': '423', 'graded': 'false', 'Grade': ''},
    {'publisher': 'Marvel', 'series_title': 'Incredible Hulk', 'issue_number': '181', 'graded': 'false',
     'Grade': '9.0'},
    {'publisher': 'Image', 'series_title': 'Invincible', 'issue_number': '2', 'graded': 'false', 'Grade': ''},
    {'publisher': 'Image', 'series_title': 'Invincible', 'issue_number': '3', 'graded': 'false', 'Grade': ''},
    {'publisher': 'Image', 'series_title': 'Invincible', 'issue_number': '4', 'graded': 'false', 'Grade': ''},
    {'publisher': 'Marvel', 'series_title': 'Invincible', 'issue_number': 'X', 'graded': 'true', 'Grade': ''},
    {'publisher': 'Marvel', 'series_title': 'Batman', 'issue_number': '999999', 'graded': 'false',
     'Professional Grader': 'CGC', 'Grade': '9.8'}

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

conditional_fields = ['Certification Number',
                      'Professional Grader',
                      'Grade']

exact_match_fields = ['publisher', 'series_title', 'issue_number']

excluded_search_terms = ['homage', '"cgc it"']

decider_field = 'graded'

category_id = 29504

menulist = """
           1. Upload Items
           2. Price Items
           3. Price Items by Filter
           4. Price Items by Id
           5. Export All Prices
           9. Quit
           """

param_list = [
    {'field': 'decider_field', 'msg': "Which field should be true to use conditional fields? e.g. 'graded'",
     'default': decider_field},
    {'field': 'category_id', 'msg': "Which category should we limit the keyword search to?",
     'default': category_id},
    {'field': 'important_fields', 'msg': "Which fields are important for matching?",
     'default': important_fields},
    {'field': 'conditional_fields', 'msg': "Which fields are important if the decider field is true?",
     'default': conditional_fields},
    {'field': 'exact_match_fields', 'msg': "Which field should be used determine exact matches?",
     'default': exact_match_fields},
    {'field': 'excluded_search_terms', 'msg': "Which terms should be explicitly excluded from the keyword search?",
     'default': excluded_search_terms}

]

filter_param = {'field': 'filter', 'msg': "Provide filter string for item_list", 'default': ''}
id_param = {'field': 'id', 'msg': "Provide id for item_list", 'default': ''}
