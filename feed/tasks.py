#coding=utf-8
from time import sleep
from datetime import datetime

from django.db.models import Q

from celery.task import task
from celery import current_task

from feed.models import Activity
from account.models import UserFollow
from quest.models import Event

@task()
def insert_activity(activitytype,contentid,fuserid):
    sleep(5)
    fields=['activitytype','contentid','from_user_id','to_user_id','addtime']
    addtime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    follows=UserFollow.objects.filter(tuser_id=fuserid).values("ufollow_id")
    #Activity_list=[Activity(activitytype=activitytype,contentid=contentid,from_user_id=fuserid,to_user_id=userid)for follow in\
    #        follows for userid in follow.values() ]
    Activity_list=[(activitytype,contentid,fuserid,userid,addtime)for follow in follows for userid in follow.values() ]
    if Activity_list:
        Activity.activityobjects.bulk_insert_ignore(fields,Activity_list)
    return addtime

@task()
def delete_activity(activitytype,contentid,fuserid):
    #sleep(5)
    #follows=UserFollow.objects.filter(tuser_id=fuserid).values("ufollow_id")
    Activity.objects.filter(activitytype=activitytype,contentid=contentid,from_user_id=fuserid).delete()
    return True

@task()
def insert_activity_by_userid(fuserid,touserid):
    try:
        fields=['activitytype','contentid','from_user_id','to_user_id','addtime']
        events=Event.objects.filter(user_id=touserid,eventtype__in=[0,1,2,3]).values("eventtype","contentid","addtime")
        Activity_list=[(event["eventtype"],event["contentid"],fuserid,touserid,event["addtime"])for event in events]
        if Activity_list:
            Activity.activityobjects.bulk_insert_ignore(fields,Activity_list)
        return True
    except Exception,e:
        print e

@task()
def cancel_follow(fuserid,touserid):
    Activity.objects.filter(from_user=fuserid,to_user=touserid).delete()


