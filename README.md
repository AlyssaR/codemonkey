# codemonkey
Some things are so easy a monkey with a keyboard could do it. So we're automating it and giving the jobs back to code monkeys.
(This is what happens when you let me create the repo, Russell.)

# structure
framework
|- backup
   |- srvc_name1.py
   |- srvc_name2.py
   |- linux_dirs.py
   |- win_dirs.py
|- setup
   |- srvc_name1.py
   |- srvc_name2.py
   |- iptables.py
   |- win_firewall.py
   |- splunk.py
   |- logstash.py
|- install
   |- srvc_name1.py
   |- srvc_name2.py
   |- iptables.py
   |- win_firewall.py
   |- splunk.py
   |- logstash.py
|- restore
   |- srvc_name1.py
   |- srvc_name2.py
   |- linux_dirs.py
   |- win_dirs.py
|- clean
   |- all.py
   |- backups.py
   |- sched_jobs.py
   |- installs.py
|- config
   |- backups.py
   |- sched_jobs.py
   |- installs.py
|- gotime.py
