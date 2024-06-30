import pandas as pd
from datetime import datetime
print(pd.date_range(end=datetime.strptime('2024-03-01 22:00:00','%Y-%m-%d %H:%M:%S'), periods=1, freq='h')[0])