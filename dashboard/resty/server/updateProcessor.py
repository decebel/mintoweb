from collections import defaultdict
from heapq import nlargest
# from nltk.tokenize import word_tokenize, sent_tokenize
# from nltk.corpus import stopwords
# from string import punctuation
# from nltk.corpus import sentiwordnet as swn
# from nltk.stem.porter import PorterStemmer
from collections import deque, defaultdict
from Queue import Queue, Full, Empty # thread-safe queue
import threading
import time
import os
import sys
# import gensim
# from gensim.models import Phrases
from collections import Counter
import os
from flask import jsonify

import logging
logging = logging.getLogger('updates')


class UpdateProcessor(threading.Thread):

	def __init__(self, engine_name, command_queue = None):
		threading.Thread.__init__(self, name = engine_name)

		self.isRunning = False

		if not command_queue:
			self.command_queue = Queue()

		self.engine_name = engine_name

	def set_sockio(self, sockio):
		self.sockio = sockio

	def post_message(self, message):
		self.command_queue.put(message)
		print "posting to queue.."

	def shutdown(self):
		self.isRunning = False

	def run(self):

		if not self.isRunning:
			self.isRunning = True
			self._process_queued_messages()

		print "\nrun method completed"

	def _process_queued_messages(self):

		while self.isRunning:
			print "inside realtime update command processor. waiting for commands"
			workFound = False

			try:

				update_message = self.command_queue.get(True, 5) #should block until someone has posted some command on the queue
				workFound = True #hack to avoid exception within finally block
				to_send = {}
				print "RAW MESSAGE: {}".format(update_message)
				# for k in update_message:
				print "new.."
				to_send = update_message
				to_send['category'] = 'Bloomberg'
				print "alerting message: {}".format(to_send)
				self.sockio.emit('updates', to_send, broadcast = True)
				logging.info('emitting Bloomberg')
				print "alerted message: {}".format(to_send)


			except Empty as timeout:
				logging.debug("Timeout..no input commands")

			except Exception as e:
				print "some error..... "
				import traceback, os.path
				top = traceback.extract_stack()[-1]
				logging.error(', '.join([type(e).__name__, os.path.basename(top[0]), str(top[1])]))
				logging.error("error processing command %s", str(e))

			finally:
				if workFound:
					self.command_queue.task_done()


update_processor = UpdateProcessor('realtime')
def getProcessor():
	return update_processor
