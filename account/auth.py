#coding:utf-8
from models import User
import traceback
from django.core.exceptions import ObjectDoesNotExist

class UserAuth(object):
    """用户验证"""
    def authenticate(self,email=None,password=None,auth_by_email=False):
        try:
            user=User.objects.filter(email=email)
            if len(user)>0:
                if auth_by_email:
                    return user[0]
                else:
                    if user[0].check_password(password):
                        return user[0]
                    else:
                        return None
            else:
                return None
        except Exception,e:
            print traceback.print_exc()
            return None
    
    def get_user(self,user_id):
        "注意is_active的影响"
        try:
            user=User.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None
