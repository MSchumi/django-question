#coding=utf-8
from account.models import UserFollow,User,Register_Temp
from account.signals import  register_user_done,follow_user_done


def follow_user(tuserid,ftype,user):
    if ftype=="0":
        UserFollow.objects.create(ufollow=user,tuser_id=tuserid)
    else:
        UserFollow.objects.filter(ufollow=user,tuser__id=tuserid).delete()
    follow_user_done.send(sender=UserFollow,fuserid=user.id,tuserid=tuserid,optype=ftype)
    return True

def create_user(email,password,name,surname,activecode):
    user=User.objects.create_user(email=email,password=password,name=name,surname=surname)
    temp=Register_Temp.objects.create(email=email,activecode=activecode)
    register_user_done.send(sender=User,instance=user)
    return True



