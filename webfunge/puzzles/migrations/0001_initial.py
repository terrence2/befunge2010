# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Puzzle'
        db.create_table('puzzles_puzzle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('goals', self.gf('django.db.models.fields.TextField')()),
            ('board', self.gf('django.db.models.fields.TextField')()),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('puzzles', ['Puzzle'])


    def backwards(self, orm):
        
        # Deleting model 'Puzzle'
        db.delete_table('puzzles_puzzle')


    models = {
        'puzzles.puzzle': {
            'Meta': {'object_name': 'Puzzle'},
            'board': ('django.db.models.fields.TextField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'goals': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['puzzles']
