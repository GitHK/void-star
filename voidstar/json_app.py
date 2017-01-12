from aiohttp import web
import traceback


def make_response(status, payload, error):
    data = dict(status=status, payload=payload, error=error)
    return web.json_response(data=data, status=status)


async def json_middleware(app, handler):
    async def middleware_handler(request):
        try:
            payload = await handler(request)

            if type(payload) is not dict:
                error_message = "Method should always return dict instance, not '%s'" % type(payload).__name__
                return make_response(status=400, payload=None, error=error_message)

            response = make_response(status=200, payload=payload, error=None)
            if response.status != 200:
                return make_response(status=response.status, payload=None, error=str(response))
            return response
        except web.HTTPException as ex:
            if ex.status != 200:
                return make_response(status=ex.status, payload=None, error=str(ex))
            raise
        except Exception as ex:
            if app['debug']:
                traceback.print_exc()
            error_message = "Internal serve error '%s: %s'" % (type(ex).__name__, str(ex))
            return make_response(status=500, payload=None, error=error_message)

    return middleware_handler


def make_app(middlewares=None, debug=True):
    app = web.Application(
        middlewares=[json_middleware] if middlewares is None else middlewares.append(json_middleware))
    app['debug'] = debug
    return app
