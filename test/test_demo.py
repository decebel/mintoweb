
import os, sys; sys.path.insert(0, os.path.join(".."))

from mintoweb import app


@app.route("/marketplaces/")
def marketplaces(req):
	return "hello world"

@app.route("/marketplace/channels/")
def channels(req):
	return "channels"


def main():
	app.serve()


if __name__ == '__main__':
	main()