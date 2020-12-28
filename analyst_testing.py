
from datetime import datetime

date = '02 December 2020'

date = datetime.strptime(date, '%d %B %Y')
print(date)

date = datetime.strftime(date, '%d/%m/%Y')
print(date)
