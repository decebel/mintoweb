
import os, sys; sys.path.insert(0, os.path.join(".."))
import unittest
import time
import warnings


from mintoweb import http_parser
from mintoweb import request


class TestQueryValidator(unittest.TestCase):
	"""Testing bad/invalid/incomplete http requests"""

	def setUp(self):
		pass

	def test_url_header(self):
		pass


	def test_url_get_invalid(self):
		"""test the URL with no endpoint.

		1. GET /
		2. GET //

		"""

		#url = "/"

		request1 = request.Request("http://app.com/")
		self.assertRaises(request.RequestError, request1.build_request)

		# url="//"
		request2 = request.Request("http://app.com//")
		self.assertRaises(request.RequestError, request2.build_request)

		# invalid resource (no closing slash /)
		request3 = request.Request("http://app.com/marketplace")
		self.assertRaises(request.RequestError, request3.build_request)

		# invalid resource (extra closing slash /)
		request4 = request.Request("http://app.com/marketplace//")
		self.assertRaises(request.RequestError, request4.build_request)	

		# invalid resource (missing closing slash / on subresource)
		request5 = request.Request("http://app.com/marketplace/channel")
		self.assertRaises(request.RequestError, request5.build_request)	


	def test_url_valid_resource(self):


		# returns a resource named resource1
		request1 = request.Request("http://app.com/marketplace/_find")
		request1.build_request()
		self.assertEquals(request1.get_endpoint(), "/marketplace/")
		self.assertEquals(request1.get_command(), "_find")

		# valid subresource request
		request2 = request.Request("http://app.com/marketplace/channel/_command")
		request2.build_request()
		self.assertEquals(request2.get_endpoint(), "/marketplace/channel/")
		self.assertEquals(request2.get_command(), "_command")


	# def test_url_get_criteria(self):
	# 	"""criteria object in url query string.

	# 	1. no criteria object
	# 	2. criteria object incomplete
	# 	3. criteria object valid and present in the beginning after endpoint
	# 	4. criteria object valid and present at random location in the url

	# 	"""

	# 	url1 = "http://app.com/resource/"
	# 	request1 = http_parser.parse(url1)
	# 	criteria1 = request1.criteria()
	# 	self.assertIsNone(criteria1)

	# 	url2 = "http://app.com/resource/criteria" # incomplete criteria 
	# 	request2 = http_parser.parse(url2)
	# 	criteria2 = request1.criteria()
	# 	self.assertIsNone(criteria2)

	# 	url3 = "http://app.com/mp/channel/criteria={}" # default to find command with empty criteria
	# 	request3 = http_parser.parse(url3)
	# 	criteria3 = request3.criteria()
	# 	self.assertIsNone(criteria3)

	# 	url4 = "http://app.com/mp/channel/_find?criteria={}" # find command with empty criteria
	# 	request4 = http_parser.parse(url4)
	# 	criteria4 = request4.criteria()
	# 	self.assertIsNone(criteria4)

	# 	pass

	def test_url_get_fields(self):
		pass

	def test_url_get_sort(self):
		pass

	def test_url_get_batch_size(self):
		pass


class TestErrorResponse(unittest.TestCase):

	def test_url_get_error_response(self):
		pass


class TestDefaultInputs(unittest.TestCase):
	"""Test all defaults with given requests"""

	def test_url_default_params(self):
		"""we should populate defaults for missing fields that are defaults"""
		pass	



class TestMarketRequests(unittest.TestCase):

	def test_url_marketplace(self):
		"""identify the marketplace in the url"""
		pass

	def test_url_marketchannel(self):
		"""identify the marketplace and the channel from the url.

		1. Invalid url
		2. Valid url
		"""
		pass



def suite():
	suite = unittest.TestSuite()
	suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestQueryValidator))
	return suite

if __name__ == "__main__":
	unittest.TextTestRunner(verbosity=1).run(suite())








	

#-------------------------
#class TestMarketplace(unittest.TestCase):
#	"""get a list of available markets.


#	"""
#	return gabu.process(request, header, criteria)


#class TestMarketChannel(unittest.TestCase):
#	"""docstring for Test unittest.TestCasesNameunittest.TestCase"""
#	pass


#class TestMarketChannelMessages(unittest.TestCase):
#	"""docstring for TestMarketChannelMessages"""
#	pass


