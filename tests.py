from datetime import datetime
from datetime import timedelta

pastDate = datetime.fromisoformat('2022-05-01 01:08:49.016151')

if (datetime.now() - pastDate).days > 1:
    print('24 hours have passed')
else:
    print('Date is within 24 hours!')