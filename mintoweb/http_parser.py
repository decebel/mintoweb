import os
import sys


from request import Request, RequestError


BASE_URL = "http://appengine.com/"
RESOURCE_SEPARATOR = "/"


def get_url_endpoint(url):
	if not url:
		return None



	if RESOURCE_SEPARATOR not in url:
		return None

	parts = url.split("/")
	if not parts or not parts[0]:
		return None

	return parts[0]


def parse(url):
	"""the url is expected to be url decoded input.

	parses the url and returns a request object
	"""

	r = Request(url)
	try:
		r.build_request()
	except RequestError as err:
		print "yes"
		print err
		raise err

		
	return r





