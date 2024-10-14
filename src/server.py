from waitress import serve

# response = 'Hello world'.encode()



def app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [b"Hello, world4"]

# Запуск Waitress-сервера
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
