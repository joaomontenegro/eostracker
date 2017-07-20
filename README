INSTALL

Set $EOS_TRACKER_HOME
Unpack eostracker under $EOS_TRACKER_HOME
Add eostracker/bin to $PATH
Run eostracker/bin/initdirs
Run 'crontab -e' and add:

* * * * * [EOS_TRACKER_HOME]/eostracker/bin/paritygo > [EOS_TRACKER_HOME]/logs/paritygo.out.log 2> [EOS_TRACKER_HOME]/logs/paritygo.err.log
* * * * * python3 [EOS_TRACKER_HOME]/eostracker/python/status.py > [EOS_TRACKER_HOME]/html/status.html 2> [EOS_TRACKER_HOME]/logs/status.err.log
* * * * * python3 [EOS_TRACKER_HOME]/eostracker/python/logjson.py > [EOS_TRACKER_HOME]/logs/logjson.out.log 2> [EOS_TRACKER_HOME]/logs/logjson.err.log

where [EOS_TRACKER_HOME] is $EOS_TRACKER_HOME value

