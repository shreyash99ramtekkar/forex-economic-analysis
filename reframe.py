import pandas as pd
import numpy as np
from datetime import datetime ,timedelta


CURRENCY = 'GBPUSD'
HOURS_BEFORE=3
HOURS_AFTER=24
CURRENCY_INDEXES= ['-'+str(i)+'h' for i in range(1,HOURS_BEFORE)][::-1].extend([ str(i)+'h' for i in range(0,HOURS_AFTER+1)])

# def attach_price(row):
#     print(type(row.name))
    

economic_events =  pd.read_csv('./data/economic_events.csv',header=0,parse_dates=['time'],index_col='time',date_format='%y-%m-%d %H:%M:%S')
currency_data =  pd.read_csv('./data/'+ CURRENCY+'.csv',header=0,parse_dates=['time'],index_col='time',date_format='%y-%m-%d %H:%M:%S')


economic_events_currency = economic_events[economic_events['currency'].isin([CURRENCY[0:3],CURRENCY[3:]])]
currency_data.index = pd.to_datetime(currency_data.index)
# economic_events.index = pd.to_datetime(economic_events.index)
# economic_events.apply(attach_price,axis=1)

def get_currency_prices_for_event(event_time, currency_prices, hours_before=5, hours_after=24):
    start_time = event_time - timedelta(hours=hours_before)
    end_time = event_time + timedelta(hours=hours_after)
    print(event_time)
    start_to_event = currency_prices[start_time:event_time].close.values.tolist()
    event_to_end = currency_prices[event_time:end_time].close.values.tolist()
    print(start_to_event)
    print(event_to_end)
    # if start_to_event is None :
    #     start_to_event = [None] * hours_before
    #     # print(start_to_event)
    # if(len(start_to_event) < hours_before):
    #     print(currency_prices[start_time:event_time])
    #     print([None]*(hours_before-len(start_to_event)))
    #     print(([None]*(hours_before-len(start_to_event))).append(start_to_event))
    #     start_to_event = ([None]*(hours_before-len(start_to_event))).extend(start_to_event)
    # elif(len(start_to_event) > hours_before):
    #     start_to_event = start_to_event[:hours_before]
    # # 
    
    # if(len(event_to_end) < hours_after):
    #     final_data.append(start_to_event.extend([None]*(hours_after-len(event_to_end))))
    #     print(start_to_event)
    # else:
    #     final_data.append(event_to_end)
   
    return start_to_event.extend(event_to_end)


def attach_currency_data(row):
    # print(row.name)
    # print(row)
    event_time = datetime.strptime(row.name, "%Y-%m-%d %H:%M:%S")
    prices = get_currency_prices_for_event(event_time, currency_data,hours_before=HOURS_BEFORE,hours_after=HOURS_AFTER)
    return pd.Series(prices, index=CURRENCY_INDEXES)
# Create a list to store results
# Iterate through each economic event
# for idx, event in economic_events.iterrows():
#     event_time = datetime.strptime(event.name,'%Y-%m-%d %H:%M:%S')  # The index is the event time
#     event_currency = event['currency']
    
#     # Get the currency prices for the specified time range
#     prices = get_currency_prices_for_event(event_time, currency_data,hours_before=HOURS_BEFORE,hours_after=HOURS_AFTER)
#     prices = prices.values.flatten()
    
#     # Create a DataFrame for the event with the corresponding price
    
#     event_with_prices = pd.concat([pd.DataFrame([event]*len(prices), index=index), prices], axis=0)
#     # Append the result to the list
#     print(event_with_prices)
#     break
#     results.append(event_with_prices)


print(economic_events_currency.head())
columns = economic_events_currency.apply(attach_currency_data,axis=1)
# Combine all results into a single DataFrame
print(columns)
final_df =  pd.concat([economic_events, columns], axis=1)

# Display the combined DataFrame
print(final_df)







