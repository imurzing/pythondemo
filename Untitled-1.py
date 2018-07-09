import datetime


begin = datetime.date(2018, 6, 1)
end = datetime.date(2018, 7, 6)
for i in range((end - begin).days+1):
    day = begin + datetime.timedelta(days=i)
    print("union SELECT '{days}' as day,count(distinct member_id) ,sum(invest_amount)  FROM `order` "
          "WHERE `status` =1 and `gmt_created` <date_add('{days}',interval +1 day) and `end_date` >'{days}' "
          .format(days=str(day)))
