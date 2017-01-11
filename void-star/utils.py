async def get_params(request):
    method = request.method
    if method == 'POST':
        params = await request.post()
    elif method == 'GET':
        params = request.rel_url.query
    else:
        raise ValueError("Unsupported HTTP method: %s" % method)

    return params
