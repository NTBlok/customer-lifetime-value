from methods_pyspark_etl.methods_pyspark_etl import *

def test_json_strings_dump_to_dict():
    event_tuple = (0,
                    0,
                    u'{"total_amount": "52.38 USD", "event_time": "2017-02-10T16:59:28.634Z", "verb": "NEW", "key": "e2ddccae25e9", "customer_id": "59e1334b00e9", "type": "ORDER"}'
                    )
    assert mapCustomerSession_to_Rows(event_tuple)


def test_timedelta_adds_seconds_and_minutes():
    time_event_tuples = [
        ([u'2017-02-10', 'Friday', u'16:59:28.634', None, None],
        u'{"total_amount": "52.38 USD", "event_time": "2017-02-10T16:59:28.634Z", "verb": "NEW", "key": "e2ddccae25e9", "customer_id": "59e1334b00e9", "type": "ORDER"}'),
        ([u'2017-02-11', 'Saturday', u'16:59:28.494', u'16:59:28.634', 0.0],
        u'{"event_time": "2017-02-11T16:59:28.494Z", "tags": {"some key": "some value"}, "verb": "NEW", "key": "19ae5aefa034", "customer_id": "59e1334b00e9", "type": "SITE_VISIT"}')
        ]
    assert sessionize(time_event_tuples)


def test_type_error_for_datetime_format_in_str_to_dt_var():
    date = '2017-02-10 16:59:28'
    #date = '2017-02-10'
    list_of_week_start_end = [('2017-02-05','2017-02-11'),
                                ('2017-02-12','2017-02-18')]
    assert week_is_number(date, list_of_week_start_end)
