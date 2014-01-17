import os

import urlparse

class RequestError(Exception):
	"""Base class for errors in the request module."""
	pass

class InputError(RequestError):

	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)



class Request(object):
	
	"""docstring for request"""
	
	PARSED_OBJECT = "PARSED_OBJECT"
	ENDPOINT = "ENDPOINT"
	COMMAND = "COMMAND"
	QUERY = "QUERY"


	def __init__(self, url):
		self.url = url
		self.dict = {}

	def build_request(self):

		if not self.url:
			self.set_is_valid(False)
			raise InputError("no url input")

		self.dict[Request.PARSED_OBJECT] = urlparse.urlparse(self.url)

		command_end_index = self.__extract_command()
		self.__extract_endpoint(command_end_index) 


	def __get_parsed(self):
		if not self.dict[Request.PARSED_OBJECT]:
			self.set_is_valid(False)
			raise InputError("request not parsed yet")

		return self.dict[Request.PARSED_OBJECT]
		
	def get_endpoint(self):

		if not self.dict[Request.ENDPOINT]:
			self.set_is_valid(False)
			raise InputError("no endpoint available for url: " + self.url)

		return self.dict[Request.ENDPOINT]

	def __extract_command(self):
		"""Extracts commands from the url.

		Commands are the last part in an path specification of the url.
		They must start with an underscore and end before the query string start (?).
		
		For example, below are valid commands:
		GET app.com/resource/_find?q=something  (find is the command here)
		GET app.com/resource/subresource/_process?q=abc (process is the command here)

		And the below ones are invalid/empty commands
		GET app.com/command?q=something (a command always starts with underscore)
		GET app.com/resource/command?q=something (same as above)

		"""

		path = self.__get_parsed().path

		if '/' not in path:
			self.set_is_valid(False)
			raise InputError("no endpoint available for url: " + self.url)

		index = path.rfind('/')
		if index == -1 or index == len(path)-1:	# slash not found or nothing after the slash
			self.set_is_valid(False)
			raise InputError("Invalid command "+self.url)

		possible_command = path[index+1:len(path)]
		
		if possible_command is None or possible_command == "" or possible_command[0] != '_': # all commands must begin with an underscore
			self.set_is_valid(False)
			raise InputError("Command name does not begin with underscore: "+self.url)

		self.dict[Request.COMMAND] = possible_command
		return path[:index+1]


	def __extract_endpoint(self, end_index):
		"""endpoint resource and subresource(s) extracter.

		The path needs to have the resource and sub-resources name in between the slashes
		For example:
		GET app.com/resource/ (NOTE the ending forward slash)
		GET app.com/resource/subresource/ (NOTE the ending forward slash)

		Examples for invalid resource:

		GET app.com 
		GET app.com/
		GET app.com//
		GET app.com///
		GET app.com/resource (NOTE: No ending forward slash)
		GET app.com/resource/subresource (NOTE: No ending forward slash)

		"""

		path = end_index #self.dict[Request.ENDPOINT] #self.__get_parsed().path

		if path[0] != '/' or path[-1] != '/':			
			self.set_is_valid(False)
			raise InputError("resource path not enclosed in forward slashes: "+path)


		path_check = path[1:-1] 	#trim the enclosing slashes

		if not path_check:		#if we just had a single / or // 
			self.set_is_valid(False)
			raise InputError("empty resource request: "+path)

		# if we have any more forward slashes in the beginning or end, then we have a bad request 
		if path_check[0] == '/' or path_check[-1] == '/':
			self.set_is_valid(False)
			raise InputError("additional forward slashes in resource path " + path)

		self.dict[Request.ENDPOINT] = path  #.split('/')
		
		return

	def __extract_query_details(self):
		"""query parts extracter.

		sample:
		q=google&oq=goo&aqs=chrome.1.69i57j0j69i60l2j0l2.3532j0j4&sourceid=chrome&espv=210&es_sm=91&ie=UTF-8

		"""


		q = self.__get_parsed().query

		if '&' not in q: #single param=value pair 			
			if '=' not in q:
				self.set_is_valid(False)
				raise InputError("Invalid query: "+q)

			(k, v) = q.split('=')
			self.dict[Request.QUERY] = {}
			self.dict[Request.QUERY][k] = v

		else:
			l = [t.split('=') for t in q.split('&')]
			self.dict[Request.QUERY] = dict(l)
	


	def get_command(self):
		return self.dict[Request.COMMAND]


	def set_is_valid(self, val):
		self.is_valid = val

	def criteria(self):
		return None

	def is_valid(self):
		return False



