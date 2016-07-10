import logging; logging.basicConfig(level=logging.INFO)
# single process multiple IO
import asyncio, os, json, time
from datetime import datetime
# an http asyncio io framework
from aiohttp import web

# define the response page,simply an html page
# a request handler is a coroutine that accept a Request instance as parameter 
# and returns a Response instance
def index(request):
	text = "<h1>Hello World!</h1>"
	return web.Response(body=text.encode('utf-8'))

# function to start the server
# event loop used for processing HTTP requests
async def init(loop):
	# create an application instance 
	app = web.Application(loop=loop)
	# use GET method, combine index page with path
	# register the request handler with the application's router
	app.router.add_route('GET','/',index)
	# after that, we can run the application by 
	# web.run_app(app)

	# create a TCP server
	srv = await loop.create_server(app.make_handler(),'127.0.0.1',9000)
	logging.info('server started at http://127.0.0.1:9000...')
	return srv

loop = asyncio.get_event_loop()
# BaseEventLoop.run_until_complete(future). Run until the Future is done.
loop.run_until_complete(init(loop))
# BaseEventLoop.run_forever(). Run until stop() is called.
loop.run_forever()