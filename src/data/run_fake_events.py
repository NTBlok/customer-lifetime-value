import fake_events
from random import randint

DAYS=14
N_CUSTOMERS=50
MAX_EVENTS=5

EVENTS = []
for i in range(N_CUSTOMERS):
    customer_key = fake_events.fake_key()
    customer = fake_events.fake_customer(key=customer_key,days=DAYS)
    for j in range(randint(1,MAX_EVENTS)):
        site_visit = fake_events.fake_site_vist(customer_key=customer_key,days=DAYS)
        image_upload = fake_events.fake_image_upload(customer_key=customer_key,days=DAYS)
        customer_order = fake_events.fake_order(customer_key=customer_key,days=DAYS)
        EVENTS.append(customer)
        EVENTS.append(site_visit)
        EVENTS.append(image_upload)
        EVENTS.append(customer_order)

lines = '\n'.join(EVENTS)
with open('../../input/input.txt','w') as f:
    f.write(lines)
