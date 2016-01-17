import sys
sys.path.append("watchdog-0.8.3/src/")
import time
import logging
from watchdog import *
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import subprocess

class MyHandler(PatternMatchingEventHandler):
	patterns = ["/var/log/auth.log"]

	def process(self, event):
		"""
		event.event_type 
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
		print event.src_path, event.event_type  # print now only for degug

		#IF this event triggers, provide output of the latest line added to said file.
		#Maybe need to confirm wall is installed.
		p = subprocess.Popen(["tail", "-n", "1", "/var/log/auth.log"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		output = p.stdout.read()


		p = subprocess.Popen(["wall", output], stdin=subprocess.PIPE, stdout=subprocess.PIPE)





	def on_modified(self, event):
		self.process(event)

	def on_created(self, event):
		self.process(event)


if __name__ == '__main__':
	args = sys.argv[1:]
	observer = Observer()
	observer.schedule(MyHandler(), path=args[0] if args else '/var/log')
	observer.start()

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()

	observer.join()