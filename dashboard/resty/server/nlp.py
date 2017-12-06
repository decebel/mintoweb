from collections import defaultdict
from heapq import nlargest
from string import punctuation
from collections import deque, defaultdict
from Queue import Queue, Full, Empty # thread-safe queue
import threading
import time
import os
import sys
from collections import Counter
import os
from flask import jsonify
import numpy as np
import updateProcessor



import logging
log = logging.getLogger('nlp')

BASE_DIR = '.' #..'
CUSTOM_DATA_DIR = BASE_DIR + '/em_data/'
update_processor = updateProcessor.getProcessor()


class ClassifierResults(object):
	def __init__(self):
		self.queue = Queue()

	def put(self, data):
		self.queue.put(data)

	def get(self):
		return self.queue

	def copy(self):
		qsz = self.queue.qsize()
		temp = []
		ids = {}
		for i in range(qsz):
			msg = self.queue.get()
			msg_id = msg['id']

			if msg_id not in ids:
				ids[msg_id] = msg
				msg['category'] = 'Bloomberg'
				temp.append(msg)


			else:
				old_msg = ids[msg_id]
				old_label = old_msg['category']
				new_label = msg['category']
				if old_label != new_label:
					logging.error(' labels are different for id: %s'.msg_id)


		# print("size of list1")
		# print(len(temp))

		for i in range(len(temp)):
			self.queue.put(temp[i])

		# print("size of list2")
		# print(len(temp))

		return temp



class SVCBasedModel(threading.Thread):

	def __init__(self, result_collector, command_queue = None):
		threading.Thread.__init__(self, name = 'svc')
		self.isRunning = False
		if not command_queue:
			self.command_queue = Queue()
		else:
			self.command_queue = command_queue

		self.result_queue = result_collector ##ClassifierResults()

	def set_sockio(self, sockio):
		self.sockio = sockio

	def load(self):

		(label_text, label_indexs, index_to_label) = load_custom_data()
		training_data, training_label_ids = prepare_for_training(label_text, label_indexs)
		self.index_to_label = index_to_label

		print ("using tf-idf vectorizer")
		self.vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, stop_words='english')
		X_train = self.vectorizer.fit_transform(training_data)

		self.clf = MultinomialNB(alpha=.01)
		self.clf.fit(X_train, training_label_ids)


	def onEMMessage(self, message):
		self.command_queue.put(CommandInfo("EM", message ))

	def onIMMessage(self, message):
		self.command_queue.put(CommandInfo("IM", message ))


	def post_message(self, tableId, schema):
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
			print "inside svc command processor. waiting for commands"
			workFound = False

			try:

				commandInfo = self.command_queue.get(True, 5) #should block until someone has posted some command on the queue
				workFound = True #hack to avoid exception within finally block

				#todo: should we do a dispatch table. they seem to be static methods ?
				if commandInfo.get_command() == "EM":
					self._process_em(commandInfo)

				elif commandInfo.get_command() == "IM":
					self._process_im(commandInfo)


			except Empty as timeout:
				logging.debug("Timeout..no input commands")

			except Exception as e:
				import traceback, os.path
				top = traceback.extract_stack()[-1]
				logging.error(', '.join([type(e).__name__, os.path.basename(top[0]), str(top[1])]))
				logging.error("error processing command %s", str(e))

			finally:
				if workFound:
					self.command_queue.task_done()

	def _process_em(self, commandInfo):
		log.info("processing EM command. message: {}".format(commandInfo.get_payload()))
		payload_dict = commandInfo.get_payload()
		update_processor.post_message(payload_dict)
		return

		try:
			payload_message = payload_dict['message']
			logging.info("svc classifying : {} ".format(payload_message))

			phrases_list = phrases_generator([payload_message])
			phrases_line = " ".join(phrases_list)
			logging.info("phrases: {}".format(phrases_line))

			payload_message_with_phrases = payload_message + " " + phrases_line


			
			smatrix = self.vectorizer.transform([payload_message_with_phrases])
			Y_pred = self.clf.predict(smatrix)
			print Y_pred
			pred_label = self.index_to_label[Y_pred[0]]
			payload_dict['category'] = pred_label
			self.result_queue.put(payload_dict)

			update_processor.post_message(payload_dict)

			logging.info("svc predicted label %s"%pred_label)


		except Exception as e:
			print e
			import traceback, os.path
			top = traceback.extract_stack()[-1]
			logging.error(', '.join([type(e).__name__, os.path.basename(top[0]), str(top[1])]))
			logging.error("error processing command %s", str(e))


	def _process_im(self, commandInfo):
		log.info("TODO. processing IM command. message: {}".format(commandInfo.get_payload()))




class CommandInfo(object):

	"""Commands posted to the DataServer.

	All commands are processed sequentially by the server
	"""

	def __init__(self, name, args):
		self.name = name
		self.args = args

	def get_command(self):
		return self.name

	def get_val(self, arg):

		if arg in self.args:
			return self.args[arg]

	def get_payload(self):
		return self.args



results_collector = ClassifierResults()

def svcmodel_engine():
	svc = SVCBasedModel(results_collector)
	return svc

	svc.load()
	return svc

MODELS = {
	'svc' : svcmodel_engine(),

}

SERVERS = {

}




class EnginePool(threading.Thread):

	def __init__(self, models = [ 'svc']):
		threading.Thread.__init__(self)
		self.models = models
		self.isRunning = False

	def start_engines(self):


		for model in self.models:
			if model not in SERVERS:
				if model not in MODELS:
					continue
				SERVERS[model] = nlp_service = MODELS.get(model)
			if not nlp_service.isRunning:
				nlp_service.setDaemon(True)
				nlp_service.start()

	def set_sockio(self, sockio):
		for model in SERVERS:
			nlp_service = SERVERS.get(model)
			print "setting up sockio for {}".format(model)
			nlp_service.set_sockio(sockio)

	def stop_engines(self):
		"""Not a forceful shutdown. """
		for model in self.models:
			m = SERVERS[model]
			m.shutdown()

	def stop_driver(self):
		self.isRunning = False

	def run(self):
		self.isRunning = True

		while self.isRunning:
			time.sleep(2)
			self.post_message('test message')
			# for model in self.models:
			# 	log.info("posting message to the nlp engine: {}".format(model))
			# SERVERS[model].onEMMessage('test message')
			logging.debug('running')



	def post_message(self, message, dest_models = None):
		if dest_models is None:
			dest_models_to_post = self.models
		else:
			dest_models_to_post = dest_models

		for model in dest_models_to_post:
			if model in SERVERS:
				SERVERS[model].onEMMessage(message)
			else:
				log.error("model name is not valid: {}".format(model))



def engine_pool_tester():
	ep = EnginePool(sockio)
	ep.start_engines()

	try:
		ep.start()
		log.info("started pool..")

	except Exception as ex:
		log.warn("received exception: {}".format(ex.message))
		ep._Thread__stop() #not sure
		ep.stop_engines()

		sys.exit(1)








def  main():
	build_vocab_test()



if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG,
					format='%(asctime)s (%(threadName)-2s) %(message)s',
					)
	main()
