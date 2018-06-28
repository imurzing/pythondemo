import datetime


begin = datetime.date(2018, 1, 1)
end = datetime.date(2018, 6, 13)
for i in range((end - begin).days+1):
    day = begin + datetime.timedelta(days=i)
    print("union SELECT '{days}' as day,count(distinct member_id) as amount  FROM `order` "
          "WHERE `status` =1 and `gmt_created` <date_add('{days}',interval +1 day) and `gmt_created` >='{days}' "
          .format(days=str(day)))
