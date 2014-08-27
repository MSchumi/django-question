#coding=utf-8
import re

from celery.task import task
from celery import current_task

from account.models import User,UserFollow
from quest.models import Question,Answer,AnswerEvaluation,QustionFollow
from feed.models import Activity
from quest.signals import  question_submit_done,answer_submit_done,vote_submit_done,follow_question_done
from account.signals import register_user_done,follow_user_done
from feed.tasks import insert_activity,delete_activity,cancel_follow,insert_activity_by_userid
from quest.tasks import insert_solr,delete_solr

def submit_question(obj,user,**kwargs):
    """ 发布问题后向好友分发,同事插入solr """
    try:
      task_id=insert_activity.delay(0,obj.id,user.id)
      task_id=insert_solr.delay('question',id=obj.id,title=remove_htmltag(obj.title),user_id=user.id)
      return task_id
    except Exception,e:
        print e

def submit_answer(obj,user,**kwarg):
    """ 回答问题后向好友分发,同事插入solr """
    try:
        task_id=insert_activity.delay(1,obj.id,user.id)
        #import pdb;pdb.set_trace()
        #task_id=insert_solr.delay('answer',{'id':obj.id,'content':obj.content,'question_id':obj.question_id,'user_id':obj.user_id})
        #task_id=insert_solr.delay('answer',obj.id,obj.content,obj.question_id,obj.user_id)
        task_id=insert_solr.delay('answer',id=obj.id,content=remove_htmltag(obj.content),question_id=obj.question_id,\
                user_id=obj.user_id)
        return task_id
    except Exception,e:
        print e

def submit_vote(instance,user,optype,**kwarg):
    """ 评价回答后向好友分发"""
    try:
        if optype=="delete":
            task_id=delete_activity.delay(3,instance,user.id)
        else:
            task_id=insert_activity.delay(3,instance.id,user.id)
        return task_id
    except Exception,e:
        print e

def follow_question(instance,user,optype,**kwarg):
    """关注问题后向好友分发 """
    try:
        if optype=="delete":
            task_id=delete_activity.delay(2,instance,user.id)
        else:
            task_id=insert_activity.delay(2,instance.id,user.id)
        return task_id
    except Exception,e:
        print e

def register_user(instance,**kwargs):
    """新用户注册 插入solr """
    task_id=insert_solr.delay('user',id=instance.id,name=instance.name,surname=instance.surname)

def remove_htmltag(html_str):
    pattern=re.compile(r'<.*?>')
    value=pattern.sub("",html_str,0)
    return value

def follow_user(fuserid,tuserid,optype,**kwargs):
    """关注或者取消关注好友操作动态表 """
    task_id=None
    if optype=="0":
        task_id=insert_activity_by_userid.delay(fuserid,tuserid)
    else:
        task_id=cancel_follow.delay(fuserid,tuserid)
    return task_id


question_submit_done.connect(submit_question,sender=Question)
answer_submit_done.connect(submit_answer,sender=Answer)
vote_submit_done.connect(submit_vote,sender=AnswerEvaluation)
follow_question_done.connect(follow_question,sender=QustionFollow)
register_user_done.connect(register_user,sender=User)
follow_user_done.connect(follow_user,sender=UserFollow)
