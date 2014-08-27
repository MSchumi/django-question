#coding=utf-8
from django.db import models,connection
from django.db import models

from quest.models import Answer,Question,AnswerEvaluation
from account.models import User

class ActivityManager(models.Manager):
    """
    用于操作动态
    """
    def get_activeities(self,uid,skip,limit):
        activity_list=super(ActivityManager,self).select_related('from_user','to_user').filter(to_user_id=uid)[skip,limit]

    def merge_contentid(self,activity_list):
        """
        暂时废弃
        """
        id_dict=dict().fromkeys(['0','1','2','3','5'],[])
        for activity in activity_list:
            if activity["eventtype"]==0:
                id_dict["0"].append(activity["contentid"])
            elif activity["eventtype"]==1:
                id_dict["1"].append(activity["contentid"])
            elif activity["eventtype"]==2:
                id_dict["2"].append(activity["contentid"])
            elif activity["eventtype"]==3:
                id_dict["3"].append(activity["contentid"])
            elif activity["eventtype"]==4:
                id_dict["4"].append(activity["contentid"])
        return id_dict
    def __query_activities(self,id_dict):
        for key in id_dict.keys():
            if key=="0":
                if len(para_dict["0"])>0:
                    question_list=Question.objects.filter(pk__in=(para_dict["0"]))#follow
                    para_dict["0"]=question_list
                else:
                    para_dict["0"]=[]
            if key=="1":
                if len(para_dict["1"])>0:
                    answer_list=Answer.objects.select_related("question").filter(pk__in=(para_dict["1"]))
                    para_dict["1"]=answer_list
                else:
                    para_dict["1"]=[]
            if key=="2":
                if len(para_dict["2"])>0:
                    question_list=Question.objects.select_related("answer","answer__question").filter(pk__in=\
                            (para_dict["2"]))
                    para_dict["2"]=question_list
                else:
                    para_dict["2"]=[]
            if key=="3":
                if len(para_dict["3"])>0:
                    evaluate_list=AnswerEvaluation.objects.select_related("answer","answer__question").filter(pk__in\
                            =(para_dict["3"]))
                    para_dict["3"]=evaluate_list
                else:
                    para_dict["3"]=[]
            if key=="4":
                if len(para_dict["4"])>0:
                    question_list=Question.objects.filter(pk__in=(para_dict["4"]))
                    para_dict["4"]=question_list
                else:
                    para_dict["4"]=[]
        return para_dict

    def bulk_insert_ignore(self,fields,value_list,print_sql=False):
        """主要解决mysql重复数据过滤的问题 加入了 ignore 关键词"""
        db_table = self.model._meta.db_table
        values_sql="(%s)" %(','.join([" %s " for _ in range(len(fields))]))
        base_sql = "INSERT IGNORE INTO %s (%s) VALUES " % (db_table, ",".join(fields))
        sql = """%s %s""" % (base_sql, values_sql)
        from django.db import connection,transaction
        cursor = connection.cursor()
        try:
            cursor.executemany(sql, value_list)
            transaction.commit_unless_managed()
            return True
        except Exception as e:
            print e
            return False

    def get_activity_list(self,userid,**kwargs):
        """获取好友最新动态 使用了存储过程 目前动态有0、1、2、3四类 分别代表 提问、回答问题、关注问题、赞或反对问题 """
        activity_list=[]
        question_submit_count=0
        answer_count=0
        page=kwargs.pop('page',1)
        pagecount=kwargs.pop('pagecount',15)
        cursor=connection.cursor()
        cursor.callproc("sp_friendactiviy",(userid,(page-1)*15,pagecount))
        for row in cursor.fetchall():
            #import pdb;pdb.set_trace()
            if row[0]==0:
                question=Question(id=row[13],title=row[14])
                user=User(id=row[15],name=row[16],surname=row[17],avatar=row[18])
                question.user=user
                activity_list.append({'activitytype':row[0],'addtime':row[1],"data":question,"fuser":User(id=row[20],name=row[21],\
                        surname=row[22],avatar=row[23])})
                question_submit_count+=1
            elif row[0]==1:
                answer=Answer(id=row[3],content=row[4],addtime=row[5],commentcount=row[6],favorcount=row[7],opposecount=row[8])
                answer.user=User(id=row[9],name=row[10],surname=row[11],avatar=row[12])
                answer.question=Question(id=row[13],title=row[14],user=User(id=row[15],name=row[16],surname=row[17],avatar=row[18])) 
                activity_list.append({'activitytype':row[0],'addtime':row[1],"data":answer,"fuser":User(id=row[20],name=row[21],\
                        surname=row[22],avatar=row[23])})
                answer_count +=1
            elif row[0]==2:
                follow=QustionFollow(id=row[19])
                question=Question(id=row[13],title=row[14])
                user=User(id=row[15],name=row[16],surname=row[17],avatar=row[18])
                question.user=user
                follow.question=question
                activity_list.append({'activitytype':row[0],'addtime':row[1],"data":follow,"fuser":User(id=row[20],name=row[21],\
                        surname=row[22],avatar=row[23])})
            elif row[0]==3:
                evalue=AnswerEvaluation(status=row[2])
                answer=Answer(id=row[3],content=row[4],addtime=row[5],commentcount=row[6],favorcount=row[7],opposecount=row[8])
                answer.user=User(id=row[9],name=row[10],surname=row[11],avatar=row[12])
                answer.question=Question(id=row[13],title=row[14],user=User(id=row[15],name=row[16],surname=row[17],avatar=row[18]))
                evalue.answer=answer
                activity_list.append({'activitytype':row[0],'addtime':row[1],"data":evalue,"fuser":User(id=row[20],name=row[21],\
                        surname=row[22],avatar=row[23])})
        return {"activity_list":activity_list,"statistics":{"submit_question":question_submit_count,"answer":answer_count}}


class Activity(models.Model):
    """
    用于存储好友动态
    """
    activitytype=models.IntegerField()
    contentid=models.IntegerField()
    from_user=models.ForeignKey(User,related_name="fromuser")
    to_user=models.ForeignKey(User,related_name="touser")
    addtime=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    activityobjects=ActivityManager()

    class Meta:
        ordering=['-addtime']
        unique_together = ('contentid', 'activitytype','to_user')  

