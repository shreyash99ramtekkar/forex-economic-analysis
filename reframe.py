import pandas as pd
import numpy as np
from datetime import datetime ,timedelta


CURRENCY = 'EURUSD'
HOURS_BEFORE=4
HOURS_AFTER=20
# CURRENCY_INDEXES= ['-'+str(i)+'h' for i in range(0,HOURS_BEFORE)][::-1].extend([ str(i)+'h' for i in range(1,HOURS_AFTER+1)])

# def attach_price(row):
#     print(type(row.name))
    

economic_events =  pd.read_csv('./data/economic_events.csv',header=0,parse_dates=['time'],index_col='time',date_format='%y-%m-%d %H:%M:%S')
currency_data =  pd.read_csv('./data/'+ CURRENCY+'.csv',header=0,parse_dates=['time'],index_col='time',date_format='%y-%m-%d %H:%M:%S')


economic_events_currency = economic_events[economic_events['currency'].isin([CURRENCY[0:3],CURRENCY[3:]])]
currency_data.index = pd.to_datetime(currency_data.index)
# economic_events.index = pd.to_datetime(economic_events.index)
# economic_events.apply(attach_price,axis=1)



def get_currency_prices_for_event(event_time, currency_prices, hours_before=5, hours_after=24):
    # print('event time before' + event_time.strftime('%y-%m-%d %H:%M:%S'))
    # flag=False
    # if (event_time == datetime.strptime('2024-03-01 22:30:00', "%Y-%m-%d %H:%M:%S")):
    #     print('event time before' + event_time.strftime('%y-%m-%d %H:%M:%S'))
    #     flag=True
    event_time = event_time.replace(minute=00)
    start_time = event_time - timedelta(hours=hours_before-1)
    end_time = event_time + timedelta(hours=hours_after)
    start_to_event = currency_prices[start_time:event_time].close.values.flatten()
    if len(start_to_event) < hours_before:
        start_to_event = add_missing_times(currency_prices[start_time:event_time],event_time,hours_before).close.values.flatten()
        # print(start_to_event)
        # start_to_event = np.concatenate([([None]*(hours_before-len(start_to_event))),start_to_event])
        # latest_value = pd.date_range(end=event_time, periods=hours_before, freq='h')[0]
        # if (start_to_event is not None) and (latest_value == currency_prices[start_time:event_time].index[-1]):
        #     print('asalamvalikum')
        #     start_to_event = np.concatenate([start_to_event,([None]*(hours_before-len(start_to_event)))])
        # else:
        #     print('valikum salam')
        #     start_to_event = np.concatenate([([None]*(hours_before-len(start_to_event))),start_to_event])
        # if flag:
        #     print('start to event '+ str(len(start_to_event)))
        #     print('printing something')
        #     print(start_to_event)
        #     print(currency_prices[start_time:event_time])
        #     flag=True
    event_to_end = currency_prices[event_time:end_time].close.values.flatten()[1:]
    if len(event_to_end) < hours_after:
        event_to_end = add_missing_times(currency_prices[event_time:end_time],event_time,hours_after,True).close.values.flatten()[1:]
        # event_to_end = np.concatenate([event_to_end,([None]*(hours_after-len(event_to_end)))])
        # if flag:
        #     print('event to end')
        #     print(currency_prices[event_time:end_time][1:])
        #     flag=True

    start_to_end = np.concatenate([start_to_event,event_to_end],axis=0)
    # if flag:
    #     print('start to event '+ str(len(start_to_event)))
    #     print(currency_prices[start_time:event_time])
    #     print('event time after' +  event_time.strftime('%y-%m-%d %H:%M:%S'))
    #     print('start to event '+ str(len(start_to_event)))
    #     print(currency_prices[start_time:event_time])
    #     print('event to end')
    #     print(currency_prices[event_time:end_time][1:])
    #     print('whole')
    #     print(start_to_end)
    #     print(pd.Series(start_to_end,index=[str(index)+'h' for index in range(-hours_before+1,hours_after+1)]))
    return pd.Series(start_to_end,index=[str(index)+'h' for index in range(-hours_before+1,hours_after+1)])

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
   

def add_missing_times(df, event_time, hours,start=False):
    # Generate the expected time intervals
    if start:
        expected_times = pd.date_range(start=event_time, periods=hours+1, freq='h')    
    else:
        expected_times = pd.date_range(end=event_time+timedelta(hours=1), periods=hours+1, freq='h')[:-1]
    
   
    # Create a DataFrame with the expected times
    expected_df = pd.DataFrame(index=expected_times)
    
    
    # Merge the original DataFrame with the expected times DataFrame
    combined_df = expected_df.join(df)
    # if start:
    #     print('combined dataframe')
    #     print(df)
    #     print('expected times dataframe')
    #     print(expected_df)
    #     print(combined_df.head(10))
    return combined_df


def attach_currency_data(row):
    # print(row.name)
    # print(row)
    event_time = datetime.strptime(row.name, "%Y-%m-%d %H:%M:%S")
    prices = get_currency_prices_for_event(event_time, currency_data,hours_before=HOURS_BEFORE,hours_after=HOURS_AFTER)
    return pd.Series(prices, index=prices.index)
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
print(columns.shape)
# Combine all results into a single DataFrame
print(economic_events_currency.shape)
final_df =  pd.concat([economic_events_currency, columns], axis=1)

# Display the combined DataFrame
final_df.to_csv('./data/economic_events_new_'+ CURRENCY +'.csv')

final_df.loc[final_df.index==datetime.strptime('2024-03-01 22:30:00', "%Y-%m-%d %H:%M:%S")]







