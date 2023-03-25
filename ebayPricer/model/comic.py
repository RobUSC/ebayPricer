from beanie import Document, Indexed, init_beanie

# Example Comic:
# {'Publisher': 'Image', 'Series Title': 'Invincible', 'Issue Number': '1', 'graded': 'true',
# 'Professional Grader': 'CGC', 'Grade': '9.6'}
class Comic(Document):
  Publisher: str
  Series_Title: str
  Issue_Number : str
  graded : bool
  Professional_Grader: str
  Grade: str
  Variant: str
