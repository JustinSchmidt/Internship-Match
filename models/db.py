# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

#########################################################################
## NOTES/CHANGES:
##  - Created initial tables (Tom, 1/21)
##  - Added auth.signature to most tables. Allows easier referencing when
##    manipulating the db. (Jeff, 1/22)
##  - Added some requirements to the student table fields to demonstrate
##    how to use requires with Web2py (Jeff, 1/22)
#########################################################################

db.define_table("company",
      Field("name", "string", length=50, notnull=True, default=None),
      Field("address", "string", length=50, notnull=True, default=None),
      Field("industry", "string", length=50, notnull=True, default=None),
      Field("qsrt", "string", length=50, notnull=True, default=None), #needs to be number format
      auth.signature)
    
    
db.define_table("job_references",
      Field("name", "string", length=50, notnull=True, default=None),
      Field("phone", "string", length=12, notnull=True, default=None),
      Field("company", "string", length=50, notnull=True, default=None),
      auth.signature)

db.define_table("work_history",
      Field("company", "string", length=50, notnull=True, default=None),
      Field("start_date", "date", notnull=True, default=None),
      Field("end_date", "date", default=None), #need to default to current date?
      Field("title", "string", length=50, notnull=True, default=None),
      Field("duties", "text", notnull=True, default=None),
      auth.signature)

db.define_table("school_history",
      Field("school", "string", length=50, notnull=True, default=None),
      Field("start_date", "date", notnull=True, default=None),
      Field("end_date", "date", default=None), #need to default to current date?
      Field("major", "string", length=50, notnull=True),
      Field("gpa", "string", notnull=True, default=None),
      auth.signature)
      
db.define_table("student",
      Field("first_name", "string", length=50, requires=IS_NOT_EMPTY(), notnull=True, default=None),
      Field("last_name", "string", length=50, requires=IS_NOT_EMPTY(), notnull=True, default=None),
      Field("zip_code", "integer", requires=IS_NOT_EMPTY(), requires=IS_MATCH('^\d{5}(-\d{4})?$'), default=None),
      Field("date_of_birth", "date", requires=IS_NOT_EMPTY(), default=None),
      Field("race", "string", length=50, default=None), #could use IS_IN_SET
      Field("gender", requires=IS_IN_SET(['Male', 'Female', 'Other']), default=None),
      Field("school_year", "string", length=50, requires=IS_NOT_EMPTY(), notnull=True, default=None),
      Field("major", "string", length=50, requires=IS_NOT_EMPTY(), notnull=True, default=None), #could use IS_IN_SET
      Field("preferred_industry", 'string', length=50, default=None), #could use IS_IN_SET
      Field("school_history", 'list:reference school_history', ondelete='CASCADE'),
      Field("work_history", 'list:reference work_history', ondelete='CASCADE'),
      Field("skills", "text", notnull=True, default=None),
      Field("languages", "text", notnull=True, default=None),
      Field("awards", "text", default=None),
      Field("hobbies", "text", default=None),
      Field("job_references", 'list:reference job_references', ondelete='CASCADE'),
      Field("phone", "string", length=12, requires=IS_MATCH('^1?((-)\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$'), notnull=True, default=None), #Should use a better regex here
      Field("email", "string", length=50, requires=IS_EMAIL(error_message='Please enter a valid email.'), notnull=True, default=None),
      Field("qsrt", "integer", notnull=True, default=None), #needs to be number format
      auth.signature)


## after defining tables, uncomment below to enable auditing
auth.enable_record_versioning(db)


