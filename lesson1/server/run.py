# -*- coding: utf-8 -*-
import socket
import os


def full_response(text, code, comment):
    response = 'HTTP/1.1 %s %s\nContent-Type: text/html\nContent-Length: %d\nConnection: keep-alive\n\n%s' % (code, comment, len(text), text)
    print response
    return response


def get_response(request):
    dictionary = {}
    lines = request.split('\r\n')
    first = lines[0].split()
    dictionary["METHOD"] = first[0]
    dictionary["URI"] = first[1]
    dictionary["HTTPVERSION"] = first[2]
    for i in lines[1:]:
        if i != '':
            words = i.split (': ')
            dictionary [words[0]] = words[1]
    if dictionary["URI"] == "/":
        return full_response('Hello Mister!\nYou are:' + dictionary["User-Agent"], 200, "OK")
    elif dictionary["URI"] == "/media/":
        mystring = '\n'.join(os.listdir("../files"))
        return full_response(mystring, 200, "OK")
    elif dictionary["URI"][:7] == "/media/":
        if dictionary["URI"][7:] in os.listdir("../files"):
            f = open("../files/" + dictionary["URI"][7:])
            mystring = f.read()
            f.close()
            return full_response(mystring, 200, "OK")
        else:
            return full_response('File not Found', 404, "Not Found")
    elif dictionary["URI"] == "/test/":
        return request
    else:
        return full_response("Page not found", 404, "Not Found")


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 8000))  #связываем сокет с хостом(localhost) и портом(8000) с помощью метода bind
server_socket.listen(0)  #запустим для сокета режим прослушивания, ставим размер очереди 0, т.е. если кто то еще будет одновременно делать запросы, то его пошлют)

print 'Started'

while 1:
    try:
        (client_socket, address) = server_socket.accept()
        print 'Got new client', client_socket.getsockname()  #печатает адрес клиента и его порт
        request_string = client_socket.recv(2048)  #будем получать данные небольшими порциями (т.к не знаем сколько пошлет данных), читаем порциями по 2048 байт
        client_socket.send(get_response(request_string))  #посылаем ответ на сервер
        client_socket.close()
    except KeyboardInterrupt:  #обрабатывание прерывания while
        print 'Stopped'
        server_socket.close()  #закрываем соединение
        exit()
