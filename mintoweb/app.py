import sys
import pprint
from httpd import MintoHTTPServer

from cache import EndpointHandler

__all__ = ['route', 'serve']


def route(path):	

	def func_wrapper(func):

		def callable_func(req):
			return func(req)
		
		EndpointHandler.add(path, callable_func)

		return callable_func

	return func_wrapper


def serve():
	MintoHTTPServer.serve_forever()




# def test_endpoints():

# 	@route("/abc/ep1")
# 	def handler1(req):
# 		print "I am from handler1"

# 	@route("/abc/ep2")
# 	def handler2(req):
# 		print "I am from handler2"


# def testcache():	
# 	test_endpoints()
# 	EndpointHandler.dump_cache()
# 	EndpointHandler.handler("/abc/ep1")("")
# 	EndpointHandler.handler("/abc/ep2")("")

# if __name__ == '__main__':
# 	testcache()