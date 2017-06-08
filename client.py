import socket, select, string, sys

if(len(sys.argv) < 3) :
    print 'Usage: client hostname port (example -> client 127.0.0.1 5000)'
    sys.exit()

def prompt():
    sys.stdout.write(alias + ': ')
    sys.stdout.flush()

# Main function
if __name__ == "__main__":

    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # Connect to remote host
    try:
        s.connect((host, port))
    except:
        print 'Unable to connect.'
        sys.exit()
    print 'Successfully connected.'
    alias = raw_input('Please enter your desired username: ')
    prompt()

    while 1:
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

        for sock in read_sockets:
            # Incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data:
                    print '\nDisconnected from the chat server.'
                    sys.exit()
                else:
                    # Print data
                    sys.stdout.write(alias + data)
                    prompt()

            # User entered a message
            else:
                msg = sys.stdin.readline()
                s.send(alias + ': ' + msg)
                prompt()
