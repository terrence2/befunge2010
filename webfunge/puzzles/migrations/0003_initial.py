# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'User'
        db.create_table('puzzles_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('pw_hash', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('puzzles', ['User'])

        # Adding model 'Puzzle'
        db.create_table('puzzles_puzzle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('goals', self.gf('django.db.models.fields.TextField')()),
            ('board', self.gf('django.db.models.fields.TextField')()),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='puzzles', null=True, to=orm['puzzles.User'])),
        ))
        db.send_create_signal('puzzles', ['Puzzle'])


    def backwards(self, orm):
        
        # Deleting model 'User'
        db.delete_table('puzzles_user')

        # Deleting model 'Puzzle'
        db.delete_table('puzzles_puzzle')


    models = {
        'puzzles.puzzle': {
            'Meta': {'object_name': 'Puzzle'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'puzzles'", 'null': 'True', 'to': "orm['puzzles.User']"}),
            'board': ('django.db.models.fields.TextField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'goals': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'puzzles.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pw_hash': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['puzzles']
