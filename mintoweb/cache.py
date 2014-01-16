import os
import pprint

pp = pprint.PrettyPrinter(indent=4)

class EndpointHandler(object):
	CACHE = {}

	@staticmethod
	def add(path, func):
		EndpointHandler.CACHE[path] = func

	@staticmethod
	def handler(path):
		return EndpointHandler.CACHE[path]

	@staticmethod
	def cache():
		return EndpointHandler.CACHE

	@staticmethod
	def dump_cache():
		pp.pprint(EndpointHandler.CACHE)



