from waitress import serve

# response = 'Hello world'.encode()
#
#
# class WSGIApp:
#
#     def __init__(self, environ, start_fn):
#         self.environ = environ
#         self.start_fn = start_fn
#
#     def __iter__(self):
#         status = '200 OK'
#         headers_list = [('Content-Type', 'text/plain')]
#         self.start_fn(status, headers_list)
#         yield response
#


# def wsgi_app(environ, start_fn):
#     status = '200 OK'
#     headers_list = [('Content-Type', 'text/plain')]
#     start_fn(status, headers_list)
#     response_body = "Hello world2".encode('utf-8')
#     return [response_body]
#
#
# serve(wsgi_app, host='localhost', port=8080)
# serve(WSGIApp, host='localhost', port=8080)



# Определение WSGI-приложения
# def app(environ, start_response):
#     status = '200 OK'
#     response_headers = [('Content-type', 'text/plain')]
#     start_response(status, response_headers)
#     return [b"Hello, world4"]
#
# # Запуск Waitress-сервера
# if __name__ == '__main__':
#     serve(app, host='0.0.0.0', port=8080)
