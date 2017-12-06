#pip install flask
#pip install flask-restful
#

from flask import Flask, send_from_directory
from flask import jsonify
from flask import request
from flask.ext.restful import Api, Resource
from flask.ext.restful import reqparse
import copy
from server import nlp
import uuid
from flask_socketio import SocketIO

import traceback
from server import updateProcessor

import os

import logging
from logging.handlers import RotatingFileHandler
formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)

msg_id = 0

logging.basicConfig(level=logging.DEBUG,
					format='%(asctime)s %(levelname)s %(message)s',
					filename='app.log',
					filemode='w')


first_response = [
{
        'category': 'Bloomberg',
        'id': 1,
        'message': 'So, I want to axe the 23s 5% in lnm holdings',
        'from': 'Josh',
        'to': 'Harold',
        'timestamp': '18-Oct-2017 3:24 PM'
    },
    {
        'category': 'Runz',
        'id': 5,
        'message': 'Might be trying to get one sold to Barkley Management',
        'from': 'Josh',
        'to': 'Harold',
        'timestamp': '18-Oct-2017 3:24 PM'
    },
    {
        'category': 'Chat/IM',
        'id': 7,
        'message': "Market is pricing the current 5 year OTR 2bps cheap. Maybe buy eh? ",
        'from': 'Josh',
        'to': 'Harold',
        'timestamp': '18-Oct-2017 3:24 PM'
    },
        {
        'category': 'Chat/IM',
        'id': 8,
        'message': "I want to offload my position in apple. You want to check with the client? ",
        'from': 'Josh',
        'to': 'Baseball Jim',
        'timestamp': '18-Oct-2017 3:24 PM'
    },
        {
        'category': 'Chat/IM',
        'id': 9,
        'message': "Can we buy HCL @ 123.10",
        'from': 'Josh',
        'to': 'Harold',
        'timestamp': '18-Oct-2017 3:24 PM'
    }
]

def get_msgid():
	global msg_id
	msg_id = msg_id + 1
	return msg_id


static_folder_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui")
app = Flask(__name__, static_folder='ui')
app.logger.addHandler(handler)

log = logging.getLogger('main')

update_processor = updateProcessor.getProcessor()
update_processor.setDaemon(True)
update_processor.start()



# class UpdateProcessor(threading.Thread):

# 	def __init__(self, engine_name, command_queue = None):
# 		threading.Thread.__init__(self, name = engine_name)

# 		self.isRunning = False

# 		if not command_queue:
# 			self.command_queue = Queue()

# 		self.result_queue = result_collector

# 		self.engine_name = engine_name

# 	def set_sockio(self, sockio):
# 		self.sockio = sockio

# 	def post_message(self, message):
# 		self.command_queue.put(message)
# 		print "posting to queue.."

# 	def shutdown(self):
# 		self.isRunning = False

# 	def run(self):

# 		if not self.isRunning:
# 			self.isRunning = True
# 			self._process_queued_messages()

# 		print "\nrun method completed"

# 	def _process_queued_messages(self):

# 		while self.isRunning:
# 			print "inside realtime update command processor. waiting for commands"
# 			workFound = False

# 			try:

# 				update_message = self.command_queue.get(True, 5) #should block until someone has posted some command on the queue
# 				workFound = True #hack to avoid exception within finally block
# 				socketio.emit('updates', update_message, broadcast=True)

# 			except Empty as timeout:
# 				logging.debug("Timeout..no input commands")

# 			except Exception as e:
# 				import traceback, os.path
# 				top = traceback.extract_stack()[-1]
# 				logging.error(', '.join([type(e).__name__, os.path.basename(top[0]), str(top[1])]))
# 				logging.error("error processing command %s", str(e))

# 			finally:
# 				if workFound:
# 					self.command_queue.task_done()


# update_processor = UpdateProcessor('realtime')
# update_processor.setDaemon(True)
# update_processor.start()

##########################################################################################

"""
"""

# class Hello(object):
# 	def init(self):
# 		self.sg = docManager.NetX("hello")
# 		self.sg.load_from_json('server/force2.json')
# 	def get_hello_world(self):
# 		if self.sg is not None:
# 			return self.sg
# 		return None



# hello = Hello()
#hello.init()

"""
Now load the processing engines

"""

socketio = None

ep = nlp.EnginePool()
ep.start_engines()


results_collector = nlp.results_collector


#########################################################################################

class MessageProcessingUtil(object):
	def __init__(self):
		pass

	@staticmethod
	def process_email_address(emailAddress):
		(username, emaildomain) = emailAddress.split("@")
		#(corp, domain) = emaildomain.split(".")
		return (username, emaildomain, "NA")

	@staticmethod
	def process_From_parameters(fromItem):
		return fromItem

		"""There can be exceptions here that we dont want to handle here."""
		d = {}
		email_address = fromItem['EmailAddress']
		(emailUserId, emaildomain, corp) = MessageProcessingUtil.process_email_address(email_address)
		d['EmailAddress'] = fromItem['EmailAddress']
		d['Username'] = fromItem['Username']
		d['Corp'] = corp
		d['EmailDomain'] = emaildomain
		d['EmailUserId'] = emailUserId
		return d



	@staticmethod
	def process_To_parameters(toItem):
		return toItem
		"""There can be exceptions here that we dont want to handle here."""

		to_email_list = []
		for item in toItem:
			to_email = item['EmailAddress']['Address']
			(emailUserId, emaildomain, corp) = MessageProcessingUtil.process_email_address(to_email)
			d = {}
			d['EmailAddress'] = to_email
			d['Username'] = item['EmailAddress']['Username']
			d['Corp'] = corp
			d['EmailDomain'] = emaildomain
			d['EmailUserId'] = emailUserId
			to_email_list.append(to_email)


		return to_email_list


class AppMessageAPI(Resource):

	def __init__(self):
		self.postParser = reqparse.RequestParser()
		self.postParser.add_argument('from', type = str,  required=True, help="From user is missing", location = 'json')
		self.postParser.add_argument('to', type = str,  required=True, help="To user is missing", location = 'json')
		self.postParser.add_argument('message', type = str,  required=True, help="to user is missing", location = 'json')
		super(AppMessageAPI, self).__init__()


	def post(self):
		args = self.postParser.parse_args()
		#sg = hello.get_hello_world()
		try:
			fromItem = args['from']
			toItem = args['to']
			message = args['message']

			fromParams = MessageProcessingUtil.process_From_parameters(fromItem)
			toParams   = MessageProcessingUtil.process_To_parameters(toItem)
			messageSubject = message #message['subject']
			messageBody = message #message['Body']['Content']
			mid = get_msgid() #uuid.uuid4()


			# post a message to the NLP processing engine
			ep.post_message({'from' : fromItem, 'to' : toItem, 'subject' : messageSubject,
				'message' : messageBody, 'id' : mid})


			return jsonify( { 'status': "ok", 'from' : fromParams,
			'to' : toParams, 'subject' : messageSubject, 'message' : messageBody, 'id' : mid} )
		except Exception as ex:
			tb = traceback.format_exc()
			log.error("trace: {}".format(tb))
			return jsonify( { 'status': "error", 'payload' : ex.message } )

class AppFeedbackAPI(Resource):

	def __init__(self):
		self.postParser = reqparse.RequestParser()
		self.postParser.add_argument('id', type = str,  required=True, help="message id is missing", location = 'json')
		self.postParser.add_argument('include', type = str,  required=True, help="yes to include or no to exclude", location = 'json')

		self.getParser = reqparse.RequestParser()
		# self.getParser.add_argument('from', type = str,  required=True, help="from user is missing", location = 'args')
		# self.getParser.add_argument('to', type = str,  required=True, help="to user is missing", location = 'args')
		# self.getParser.add_argument('length', type = int,  default=6, location='args')


		super(AppFeedbackAPI, self).__init__()

	def get(self):
		args = self.getParser.parse_args()
		sg = hello.get_hello_world()
		fromId = args['from']
		toId = args['to']
		length = args['length']
		return jsonify( { 'status': "error", 'payload' : "not implemented" } )

		# try:
		# 	paths = sg.k_shortest_path(fromId, toId, length, weight='weight')
		# 	return jsonify( { 'status': "ok", 'payload' : paths } )
		# except Exception as ex:
		# 	return jsonify( { 'status': "error", 'payload' : ex.message } )

	def post(self):
		args = self.postParser.parse_args()
		#sg = hello.get_hello_world()
		fromId = args['id']
		toId = args['include']

		try:
			# paths = sg.k_shortest_path(fromId, toId, length, weight='weight')
			return jsonify( { 'status': "done", 'payload' : "ok" } )
		except Exception as ex:
			tb = traceback.format_exc()
			log.error("trace: {}".format(tb))
			return jsonify( { 'status': "error", 'payload' : ex.message } )


"""
post data:

{"from" : "as", "to" : "go", "info" : {"type" : "official", "frequency" : 100}}
{"from" : "as", "to" : "go", "info" : {}}
"""



class GetSnapshot(Resource):

	def __init__(self):
		self.postParser = reqparse.RequestParser()
		# self.postParser.add_argument('from', type = str,  required=True, help="from user is missing", location = 'json')
		# self.postParser.add_argument('to', type = str,  required=True, help="to user is missing", location = 'json')
		# self.postParser.add_argument('info', type = dict,  default={}, location='json')

		self.getParser = reqparse.RequestParser()
		# self.getParser.add_argument('from', type = str,  required=True, help="from user is missing", location = 'args')
		# self.getParser.add_argument('to', type = str,  required=True, help="to user is missing", location = 'args')
		# self.getParser.add_argument('info', type = dict,  default={}, location='args')

		super(GetSnapshot, self).__init__()

	def get(self):
		# args = self.getParser.parse_args()
		# sg = hello.get_hello_world()
		# result = self._process(args, sg)
		return jsonify( { 'status': "error", 'payload' : "not implemented" } )

	def post(self):
		args = self.postParser.parse_args()
		#sg = hello.get_hello_world()
		result = self._process(args, None)
		return result

	def _process(self, args, sg):

		# fromId = args['from']
		# toId = args['to']
		# info = args['info']

		try:
			result_data = []


			dummy = {'id': 123, 'Category' : 'front-running', 'message' : 'Buy me a gift',
			'from' : 'user@corp.com', 'to' : 'user2@corp.com', 'Timestamp' : '11.40 am EST 20160927'}
			#result_data.append(dummy)

			result_data = results_collector.copy()
			result_data.extend(first_response)
			print "result_data"
			print result_data

			# for datum in list(results_collector.get()):
			# 	result_data.append(datum)

			# return jsonify( result_data  )
			return result_data

			# d = {}
			# if info is dict:
			# 	d = info
			# else:
			# 	for k in info:
			# 		d[k] = info[k]

			# log.info("from: {} 'to' : {} data: {}".format(fromId, toId, d))

			# edgeInfo = docManager.Edge(d)
			# before = sg.get_edge_info(fromId, toId)
			# before = copy.deepcopy(before)
			# log.info("'from' : {} 'to' : {} dataBefore: {}".format(fromId, toId, before))

			# # what if either from or to user is not present?
			# sg.update_edge_info(fromId, toId, edgeInfo)
			# after = sg.get_edge_info(fromId, toId)
			# log.info("from: {} 'to' : {} dataAfter: {}".format(fromId, toId, after))

			#return jsonify( { 'status': "ok", 'payload' : {'before' : before, 'after' : after} } )
		except Exception as ex:
			tb = traceback.format_exc()
			log.error("trace: {}".format(tb))
			return jsonify( { 'status': "error", 'payload' : ex.message } )



"""
returns the list of users in the system (user=all)
returns info for a specific user (user=<username>)
"""
class HelloListAPI(Resource):

	def __init__(self):

		self.getParser = reqparse.RequestParser()
		self.getParser.add_argument('user', type = str,  required=True, help="user is missing. If set to all returns a list of all users. Otherwise returns info for a specific user", location = 'args')
		self.getParser.add_argument('length', type = int,  default=6, location='args')
		super(HelloListAPI, self).__init__()

	def get(self):
		args = self.getParser.parse_args()
		sg = hello.get_hello_world()
		user = args['user']
		length = args['length']

		try:
			if user == "all":
				listofusers = sg.get_node_names()
				return jsonify( { 'status': "ok", 'payload' : listofusers } )
			else:
				log.info("requesting info for user: {}".format(user))
				userinfo = sg.get_node_data(user)
				log.info("Found info for user: {}".format(userinfo))

				return jsonify( { 'status': "ok", 'payload' : userinfo } )
		except Exception as ex:
			tb = traceback.format_exc()
			log.error("trace: {}".format(tb))
			return jsonify( { 'status': "error", 'payload' : ex.message } )


"""
returns a serialized view of the world
"""
class HelloWorldViewAPI(Resource):

	def __init__(self):
		super(HelloWorldViewAPI, self).__init__()

	def get(self):
		try:
			sg = hello.get_hello_world()
			serialized = sg.get_as_json()
			return serialized
		except Exception as ex:
			tb = traceback.format_exc()
			log.error("trace: {}".format(tb))
			return jsonify( { 'status': "error", 'payload' : ex.message } )



socketio = SocketIO(app)
ep.set_sockio(socketio)
update_processor.set_sockio(socketio)

@socketio.on('connect')
def connect():
   socketio.emit('connect', {'data': 'Connected'})
   log.info ('Connected...awesome')

@socketio.on('disconnect')
def disconnect():
   #socketio.emit('disconnect', {'data': 'Disconnected'})
   log.info ('Disconnected...awesome')

@socketio.on('updates')
def broadcast_json(data):
   socketio.emit('updates', data, broadcast=True)


api = Api(app)
api.add_resource(AppFeedbackAPI, '/feedback', endpoint = 'feedbackinfo')
api.add_resource(HelloListAPI, '/list', endpoint = 'hellolist')
api.add_resource(HelloWorldViewAPI, '/worldview', endpoint = 'helloworldview')
api.add_resource(GetSnapshot, '/getsnapshot', endpoint = 'getsnapshotinfo')
api.add_resource(AppMessageAPI, '/submitchat', endpoint = 'submitchatinfo')

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

def  main():
	print "folder: {}".format(static_folder_root)
	# app.run(host='0.0.0.0', port=2222, debug=False)
	#socketio = SocketIO(app)
	socketio.run(app, host='0.0.0.0', port=5000, debug=False)
	#socketio.on_event('my event', my_function_handler, namespace='/test')
	# socketio.run(host='0.0.0.0', port=2222, debug=False)

	pass


if __name__ == '__main__':
	log.info("starting app")
	main()
