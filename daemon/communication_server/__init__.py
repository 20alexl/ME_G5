# Empty file

from . import server
from . import timing


def server_startup(host, post):
    try:
        myserver = server.CommunicationServer(host, post)
        myserver.start_server()
        if myserver.test():
            pass
        
    except Exception as error:
        raise error
    
def test():
        if timing.Timer.error == None and server.myserver.connected == True:
            try:
                
                status, _ = timing.status()
                if not status:
                    _, data = timing.status()
                    print("Server Test Complete: PING / ", data)
            except Exception as error:
                raise error
            

def server_begin():
    try:
        pass #being server
    except Exception as error:
        raise error