# ncheel
DEPLOYMENT:

CONFIGURE!!! EMAIL in settings.py
if you use gmail -> https://support.google.com/accounts/answer/6010255

:tutorosapp -> views.py and serializers.py use mongoDB, press F3 and write MongoClient to find places where it is used

mysql Server config file -> /etc/cfg.cnf

project using SPA as client,

You can easily check project's api changing to DEBUG = True in settings.py and accesing /tutorsapp/api/

in serializers.py TestScheduleSerializer/create change message to (your www adress) + 'test/get_test?link=' + md5_sum

Be carefull with time zones, if tutor and server uses different time zones you have to modify some code

