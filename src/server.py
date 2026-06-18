import socket
import threading
import select
from src.store import RedisStore
from src.persistence import AOF

CAPACITY = 10
MODE = 'select'
aof = AOF('./data/data.aof')
store = RedisStore(CAPACITY, aof)
lock = threading.Lock()

def execute(command):
    cmd = command[0].upper()
    match cmd:
        case "SET":
            aof.log(command)
            store.set(command[1], command[2])
            return "+OK\n"
        case "GET":
            val = store.get(command[1])
            return f"+{val}\n" if val else "$None\n"
        case "DEL":
            aof.log(command)
            store.delete(command[1])
            return "+OK\n"
        case "INCR":
            aof.log(command)
            val = store.incr(command[1])
            return f"+{val}\n"
        case "EXISTS":
            val = store.exists(command[1])
            return f"+{val}\n"
        case "LPUSH":
            aof.log(command)
            store.lpush(command[1], command[2])
            return "+OK\n"
        case "RPUSH":
            aof.log(command)
            store.rpush(command[1], command[2])
            return "+OK\n"
        case "LPOP":
            aof.log(command)
            val = store.lpop(command[1])
            return f"+{val}\n" if val else "$None\n"
        case "RPOP":
            aof.log(command)
            val = store.rpop(command[1])
            return f"+{val}\n" if val else "$None\n"
        case "LRANGE":
            val = store.lrange(command[1], int(command[2]), int(command[3]))
            return f"+{val}\n" if val else "$None\n"
        case "LTRIM":
            aof.log(command)
            store.ltrim(command[1], int(command[2]), int(command[3]))
            return "+OK\n"
        case "HSET":
            aof.log(command)
            store.hset(command[1], command[2], command[3])
            return "+OK\n"
        case "HGET":
            val = store.hget(command[1], command[2])
            return f"+{val}\n" if val else "$None\n"
        case "HDEL":
            aof.log(command)
            val = store.hdel(command[1], command[2])
            return f"+{val}\n"
        case "HGETALL":
            h_map = store.hgetall(command[1])
            # if not h_map:
            #     return "$None\n"
            # st = ''
            # for k in h_map.keys():
            #     st += f"{k} => {h_map[k]}, "
            return f"+{val}\n" if val else "$None\n"
        case "SADD":
            aof.log(command)
            store.sadd(command[1], command[2])
            return "+OK\n"
        case "SISMEMBER":
            val = store.sismember(command[1], command[2])
            return f"+{val}\n"
        case "SREM":
            aof.log(command)
            val = store.srem(command[1], command[2])
            return f"+{val}\n"
        case "SMEMBERS":
            val = store.smembers(command[1])
            return f"+{val}\n" if val else "$None\n"
        case "ZADD":
            aof.log(command)
            store.zadd(command[1], float(command[2]), command[3])
            return "+OK\n"
        case "ZREM":
            aof.log(command)
            val = store.zrem(command[1], float(command[2]), command[3])
            return f"+{val}\n"
        case "ZRANGE":
            val = store.zrange(command[1], int(command[2]), int(command[3]))
            return f"+{val}\n" if val else "$None\n"
        case "EXPIRE":
            aof.log(command)
            store.expire(command[1], int(command[2]))
            return "+OK\n"
        case "TTL":
            val = store.ttl(command[1])
            return f"+{val}\n"
        case _:
            return "-ERR unknown command\n"
        

def handle_client(conn):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        command = data.decode().strip().split()
        if not command:
            continue
        try:
            # lock.acquire()
            # result = execute(command)
            # lock.release()
            with lock:
                result = execute(command)
        except (IndexError, KeyError, ValueError) as e:
            result = f"-ERR {e}\n"
        conn.send(result.encode())
    conn.close()

def run_threading(server):
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,))
        thread.start()

def run_select(server):
    sockets_list = [server]
    while True:
        ready = select.select(sockets_list, [], [])[0]
        for sock in ready:
            if sock == server:
                conn, addr = server.accept()
                sockets_list.append(conn)
            else:
                data = sock.recv(1024)
                if not data:
                    sock.close()
                    sockets_list.remove(sock)
                    continue
                command = data.decode().strip().split()
                if not command:
                    continue
                try:
                    result = execute(command)
                except (IndexError, KeyError, ValueError) as e:
                    result = f"-ERR {e}\n"
                sock.send(result.encode())



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# server.bind(("localhost", 6379))
server.bind(("0.0.0.0", 6379))
server.listen()
print('Server Ready')
aof.replay(execute)
if MODE == "threading":
    run_threading(server)
else:
    run_select(server)
    
