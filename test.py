import pandas as pd

df = pd.read_csv('calendar_dates.csv')
print(df.head)
print(df.service_id.unique())
print(len(df.service_id.unique()))
print(df.exception_type.unique())