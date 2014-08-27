# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field follower on 'Question'
        m2m_table_name = db.shorten_name(u'quest_question_follower')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm[u'quest.question'], null=False)),
            ('user', models.ForeignKey(orm[u'account.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['question_id', 'user_id'])


    def backwards(self, orm):
        # Removing M2M table for field follower on 'Question'
        db.delete_table(db.shorten_name(u'quest_question_follower'))


    models = {
        u'account.user': {
            'Meta': {'object_name': 'User'},
            'addTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'follower': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'userfollow'", 'symmetrical': 'False', 'through': u"orm['account.UserFollow']", 'to': u"orm['account.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'})
        },
        u'account.userfollow': {
            'Meta': {'object_name': 'UserFollow'},
            'addtime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tuser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_user'", 'to': u"orm['account.User']"}),
            'ufollow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_user'", 'to': u"orm['account.User']"})
        },
        u'quest.answer': {
            'Meta': {'object_name': 'Answer'},
            'addtime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'commentcount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'edittime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'favorcount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opposecount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quest.Question']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.User']"})
        },
        u'quest.answerevaluation': {
            'Meta': {'object_name': 'AnswerEvaluation'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quest.Answer']"}),
            'edittime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.User']"})
        },
        u'quest.comment': {
            'Meta': {'object_name': 'Comment'},
            'addtime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quest.Answer']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'edittime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'favorcount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'touser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'tuser'", 'to': u"orm['account.User']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'fuser'", 'to': u"orm['account.User']"})
        },
        u'quest.commentevaluation': {
            'Comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quest.Comment']"}),
            'Meta': {'object_name': 'CommentEvaluation'},
            'edittime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.User']"})
        },
        u'quest.event': {
            'Meta': {'ordering': "['-addtime']", 'object_name': 'Event'},
            'addtime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'contentid': ('django.db.models.fields.IntegerField', [], {}),
            'eventtype': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isdelete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.User']"})
        },
        u'quest.eventcontent': {
            'Meta': {'object_name': 'EventContent'},
            'addtime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'event': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['quest.Event']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'quest.question': {
            'Meta': {'object_name': 'Question'},
            'addtime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'answercount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'browsecount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'edittime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'follower': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'questions'", 'symmetrical': 'False', 'to': u"orm['account.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'topics': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['quest.Topic']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['account.User']"})
        },
        u'quest.topic': {
            'Meta': {'object_name': 'Topic'},
            'addtime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'edittime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.User']"})
        }
    }

    complete_apps = ['quest']