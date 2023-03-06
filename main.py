from pricer import EbayPricer

comic_list = [
    {'Publisher': 'Image', 'Series Title': 'Invincible', 'Issue Number': '1', 'graded': 'true',
     'Professional Grader': 'CGC', 'Grade': '9.6'},
    {'Publisher': 'Marvel', 'Series Title': 'Amazing Spider-Man', 'Issue Number': '300', 'Professional Grader': 'CGC',
     'graded': 'true',
     'Grade': '9.2'},
    {'Publisher': 'DC', 'Series Title': 'Batman', 'Issue Number': '423', 'graded': 'false', 'Grade': ''},
    {'Publisher': 'Marvel', 'Series Title': 'Incredible Hulk', 'Issue Number': '181', 'graded': 'false',
     'Grade': '9.0'},
    {'Publisher': 'Image', 'Series Title': 'Invincible', 'Issue Number': '2', 'graded': 'false', 'Grade': ''},
    {'Publisher': 'Image', 'Series Title': 'Invincible', 'Issue Number': '3', 'graded': 'false', 'Grade': ''},
    {'Publisher': 'Image', 'Series Title': 'Invincible', 'Issue Number': '4', 'graded': 'false', 'Grade': ''},
    {'Publisher': 'Marvel', 'Series Title': 'Invincible', 'Issue Number': 'X', 'graded': 'true', 'Grade': ''},
    {'Publisher': 'Marvel', 'Series Title': 'Batman', 'Issue Number': '999999', 'graded': 'false',
     'Professional Grader': 'CGC', 'Grade': '9.8'},
    {'Publisher': 'Marvel', 'Series Title': 'X-Force', 'Issue Number': '1', 'graded': 'true',
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

exact_match_fields = ['Publisher', 'Series Title', 'Issue Number']

decider_field = 'graded'

category_id = 29504


def main():
    args = {'item_list': comic_list, 'important_fields': important_fields, 'conditional_fields': conditional_fields,
            'category_id': category_id, 'exact_match_fields': exact_match_fields, 'decider_field': decider_field}
    EbayPricer.getPaginatedListing(args)


if __name__ == "__main__":
    main()
