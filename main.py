from pricer import EbayPricer

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
conditional_fields = ['Certification Number',
                      'Professional Grader',
                      'Grade']


def main():
    args = {'item_list': comic_list, 'important_fields': important_fields, 'conditional_fields': conditional_fields,
            'category_id': 29504}
    EbayPricer.getPaginatedListing(args)


if __name__ == "__main__":
    main()
