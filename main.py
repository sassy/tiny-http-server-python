#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import re

def response_ok(version: str) -> str:
    ret = version + " 200 OK\r\n"
    ret += "Content-Type: text/html\r\n"
    ret += "\r\n"
    ret += "<h1>Hello World!!</h1>\r\n"
    return ret

def response_not_found(version: str) -> str:
    ret = version + " 404 Not Found\r\n"
    ret += "Content-Type: plain/text\r\n"
    ret += "Connection: close\r\n"
    ret += "\r\n"
    ret += "Not Found"
    return ret

def parse_header(data) -> str:
    string = data.decode(encoding='utf-8')
    lines = string.splitlines()
    m = re.match(r'^(.+)\s(.+)\s(.+)$', lines[0])
    if m[1] == "GET" and m[2] == "/":
        return response_ok(m[3])
    else:
        return response_not_found(m[3])
    

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 50001))
        s.listen(1)

        while True:
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    ret = parse_header(data)
                    print(ret)
                    conn.send(ret.encode(encoding='utf-8'))
            conn.close()
                    


if __name__ == '__main__':
    main()