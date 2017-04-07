
import json
from datetime import datetime, timedelta

def customer_key_to_id(line):
    event = json.loads(line)
    if event['type'] == 'CUSTOMER':
        customer_id = event['key']
    else:
        customer_id = event['customer_id']
    return customer_id



def sort_events_by_datetime(events_list):
    time_event_tuples = [(json.loads(event)['event_time'],event) for event in events_list]
    time_event_tuples.sort()
    return time_event_tuples

def parse_event_time(event_time):
    dt,tm = event_time.strip('Z').split('T')
    t = ':'.join(tm.split(':')[:3])
    hms = t.split('.')[0]
    ymd_hms = ' '.join([dt,hms])
    return dt,t,ymd_hms

def dt_to_day(dt,fmt="%Y-%m-%d"):
    return datetime.strptime(dt,fmt).strftime('%A')

def str_to_dt_var(str_dt,fmt="%Y-%m-%d %H:%M:%S"):
    return datetime.strptime(str_dt,fmt)

def dt_var_to_str(dt_var,fmt="%Y-%m-%d %H:%M:%S"):
    return datetime.strftime(dt_var,fmt)

def week_start_end(week_range):
    list_of_week_start_end = []
    start = week_range[0]
    end = dt_var_to_str(str_to_dt_var(start,fmt="%Y-%m-%d")+timedelta(days=6),
                        fmt="%Y-%m-%d")
    list_of_week_start_end.append((start,end))
    while end < week_range[-1]:
        start = dt_var_to_str(str_to_dt_var(end,fmt="%Y-%m-%d")+timedelta(days=1),
                        fmt="%Y-%m-%d")
        end = dt_var_to_str(str_to_dt_var(start,fmt="%Y-%m-%d")+timedelta(days=6),
                        fmt="%Y-%m-%d")
        list_of_week_start_end.append((start,end))
    return list_of_week_start_end

def week_is_number(date,list_of_week_start_end):
    dt_var = str_to_dt_var(date,fmt="%Y-%m-%d")
    week_number = [i for i in range(len(list_of_week_start_end))
                   if dt_var >= str_to_dt_var(list_of_week_start_end[i][0],fmt="%Y-%m-%d")
                     and dt_var <= str_to_dt_var(list_of_week_start_end[i][1],fmt="%Y-%m-%d")][0]
    return week_number

def sessionize_datetime_data(session_data,minute_window=30,
                             week_def={'Sunday':0,
                                   'Monday':1,
                                   'Tuesday':2,
                                   'Wednesday':3,
                                   'Thursday':4,
                                   'Friday':5,
                                   'Saturday':6},
                             hdr=['date','day','session_start','prior_session_start'
                                  ,'minutes_since_prior_session']):



    week_numbers = [0]
    initial_day = dict(zip(hdr,session_data[0][0]))['day']
    initial_date = dict(zip(hdr,session_data[0][0]))['date']
    final_date = dict(zip(hdr,session_data[-1][0]))['date']
    week_range = [initial_date,final_date]
    n = 0
    session_numbers = [n]

    # For initial week, back up start to the defined week start day if the day is not already week start day
    """ TODO:  Use algorithm to scroll integers for a given week start day, then populated week definition dict
    See Example:
     In[]   idx = [x for x in range(7)]
     In[]   print idx
     [0, 1, 2, 3, 4, 5, 6]
     In[]   for i in range(len(idx)):
                print i,[(x-i)%len(idx) for x in idx]
     0 [0, 1, 2, 3, 4, 5, 6]
     1 [6, 0, 1, 2, 3, 4, 5]
     2 [5, 6, 0, 1, 2, 3, 4]
     3 [4, 5, 6, 0, 1, 2, 3]
     4 [3, 4, 5, 6, 0, 1, 2]
     5 [2, 3, 4, 5, 6, 0, 1]
     6 [1, 2, 3, 4, 5, 6, 0]
     """

    for k,v in week_def.items():
        if v == 0:
            week_start = k
    if initial_day != week_start:
        initial_dt_var = str_to_dt_var(initial_date,fmt="%Y-%m-%d")-timedelta(days=week_def[initial_day])
        week_range[0] = dt_var_to_str(initial_dt_var,fmt="%Y-%m-%d")
    list_of_week_start_end = week_start_end(week_range)
    for i in range(1,len(session_data)):
        session_dict = dict(zip(hdr,session_data[i][0]))
        minutes_since_prior_session = session_dict['minutes_since_prior_session']
        if minutes_since_prior_session <= minute_window:
            session_numbers.append(n)
        else:
            n += 1
            session_numbers.append(n)
        date = session_dict['date']
        week_number = week_is_number(date,list_of_week_start_end)
        week_numbers.append(week_number)

    return week_numbers,session_numbers






def sessionize(time_event_tuples):
    session_data = []
    initial_event_time,initial_event = time_event_tuples[0]
    initial_dt,initial_t,initial_ymd_hms = parse_event_time(initial_event_time)
    initial_d = dt_to_day(initial_dt)
    session_data.append(([initial_dt,initial_d,initial_t,None,None],initial_event))
    for i in range(1,len(time_event_tuples)):
        event_time,event = time_event_tuples[i]
        prior_event_time,prior_event = time_event_tuples[i-1]
        dt,t,ymd_hms = parse_event_time(event_time)
        d = dt_to_day(dt)
        prior_dt,prior_t,prior_ymd_hms = parse_event_time(prior_event_time)
        tdelta = (str_to_dt_var(ymd_hms,fmt="%Y-%m-%d %H:%M:%S")
                                 -str_to_dt_var(prior_ymd_hms,fmt="%Y-%m-%d %H:%M:%S"))
        seconds_since_prior_t = tdelta.seconds + tdelta.days * 86400.0
        minutes_since_prior_t = seconds_since_prior_t / 60.0
        session_data.append(([dt,d,t,prior_t,minutes_since_prior_t],event))

    week_numbers,session_numbers = sessionize_datetime_data(session_data)
    events = [session_events[1] for session_events in session_data]
    return [zip(week_numbers,session_numbers,events)]


def mapCustomerSession_to_Rows(byCustomerSession_tuples):
    rows = []
    customer_id,session_data = byCustomerSession_tuples
    session_data = session_data[0]
    for event_tup in session_data:
        row = []
        row.append(customer_id)
        week_id = event_tup[0]
        row.append(week_id)
        visit_id = event_tup[1]
        row.append(visit_id)
        event_dict = json.loads(event_tup[2])
        event_type = event_dict['type']
        if event_type == 'ORDER':
            amount = float(event_dict['total_amount'].split()[0])
            eventIsOrder = True
        else:
            amount = 0.0
            eventIsOrder = False
        row.append(eventIsOrder)
        row.append(amount)
        rows.append(row)
    return rows


def toCSV(data):
    return ','.join([str(d) for d in data])


QUERY_SELECT_VISIT_AMOUNTS = """select _1 as customer_id,
                                _2 as week_id,
                                _3 as visit_id,
                                _4 as isOrder,
                                _5 as amount
                                from visit_amounts
                        """
QUERY_SELECT_LTV_PRELIM = """select customer_id,
                                week_id,
                                count(distinct visit_id) as visits_per_wk,
                                sum(amount) as amount_per_wk
                                from t1
                                group by customer_id, week_id
                                order by customer_id, week_id
                        """

QUERY_SELECT_LTV_ADD = """select customer_id,
                                week_id,
                                visits_per_wk,
                                amount_per_wk,
                                amount_per_wk/visits_per_wk as amount_per_visit
                                from t2
                                order by customer_id, week_id
                        """



QUERY_SELECT_LTV_FINAL = """select customer_id,
                            52*(sum(amount_per_wk)/sum(visits_per_wk))*10 as customer_ltv
                                from t3
                                group by customer_id
                                order by customer_ltv desc
                        """
