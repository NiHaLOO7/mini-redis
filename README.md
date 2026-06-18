# Mini Redis

A Redis implementation from scratch in Python — no external libraries used.

Built as part of a series of open-source system design projects.

## Features

- **22+ commands** — SET, GET, DEL, INCR, LPUSH, RPUSH, LPOP, RPOP, LRANGE, LTRIM, HSET, HGET, HDEL, HGETALL, SADD, SISMEMBER, SREM, SMEMBERS, ZADD, ZREM, ZRANGE, EXPIRE, TTL, EXISTS
- **TCP server** — custom protocol over raw sockets
- **Multi-client support** — threading mode and select (I/O multiplexing) mode, switchable
- **Thread safety** — `threading.Lock` for concurrent access
- **TTL & Expiry** — lazy deletion via MinHeap-based cleanup
- **AOF Persistence** — append-only file with base64 encoding, replay on restart
- **Docker & Kubernetes** — containerized and deployable

## Data Structures (all built from scratch)

| Structure | Used For |
|-----------|----------|
| **HashMap** | Key-value store, hash sets, hash maps |
| **DoublyLinkedList** | Lists (LPUSH, RPUSH, LPOP, RPOP, LRANGE, LTRIM) |
| **LRU Cache** | Eviction when capacity exceeded |
| **MinHeap** | TTL expiry tracking (earliest expiry on top) |
| **SkipList** | Sorted sets (ZADD, ZREM, ZRANGE) |

## Supported Commands

### Strings
| Command | Description |
|---------|-------------|
| `SET key value` | Set a key-value pair |
| `GET key` | Get value by key |
| `DEL key` | Delete a key |
| `INCR key` | Increment integer value by 1 |
| `EXISTS key` | Check if key exists |

### Lists
| Command | Description |
|---------|-------------|
| `LPUSH key value` | Push to head of list |
| `RPUSH key value` | Push to tail of list |
| `LPOP key` | Pop from head |
| `RPOP key` | Pop from tail |
| `LRANGE key start end` | Get elements in range |
| `LTRIM key start end` | Trim list to range |

### Hash Maps
| Command | Description |
|---------|-------------|
| `HSET key field value` | Set field in hash |
| `HGET key field` | Get field from hash |
| `HDEL key field` | Delete field from hash |
| `HGETALL key` | Get all fields and values |

### Sets
| Command | Description |
|---------|-------------|
| `SADD key value` | Add to set |
| `SISMEMBER key value` | Check membership |
| `SREM key value` | Remove from set |
| `SMEMBERS key` | Get all members |

### Sorted Sets
| Command | Description |
|---------|-------------|
| `ZADD key score value` | Add with score |
| `ZREM key score value` | Remove element |
| `ZRANGE key start end` | Get elements by rank |

### TTL / Expiry
| Command | Description |
|---------|-------------|
| `EXPIRE key seconds` | Set expiry on key |
| `TTL key` | Get remaining TTL (-1 = no expiry, -2 = expired) |

## How to Run

### Local

```bash
cd mini-redis
python3 -m src.server
```

Server starts on port `6379`. Connect with any TCP client:

```bash
echo "SET name nihal" | nc localhost 6379
echo "GET name" | nc localhost 6379
```

### Docker

```bash
docker compose up --build
```

Runs on port `6380` (mapped from container's 6379).

### Kubernetes (minikube)

```bash
minikube start
eval $(minikube docker-env)
docker build -t mini-redis .
kubectl apply -f deployment.yml
kubectl apply -f service.yml
minikube service mini-redis-service
```

## Multi-Client Modes

Switch between modes by changing `MODE` in `server.py`:

### Threading Mode
- One thread per client connection
- True parallelism for I/O-bound work
- `threading.Lock` protects shared state

### Select Mode (I/O Multiplexing)
- Single thread handles all clients
- `select.select()` blocks until activity on any socket
- No context switching overhead
- Better for many idle connections

## Persistence (AOF)

All write commands are logged to `data/data.aof` using base64 encoding. On server restart, the AOF file is replayed to restore state.

- Commands are flushed immediately (no data loss)
- Base64 prevents issues with special characters
- Replay uses a `replaying` flag to avoid re-logging during restore

## Architecture

```
Client → TCP Socket → Server (threading/select)
                         ↓
                    execute(command)
                         ↓
                    RedisStore ──→ HashMap (main store)
                       │         → LRUCache (eviction)
                       │         → MinHeap (TTL tracking)
                       │         → DoublyLinkedList (lists)
                       │         → SkipList (sorted sets)
                       ↓
                    AOF (persistence)
```

## Used By

- [url-shortener](https://github.com/NiHaLOO7/url-shortener) — caching + distributed ID generation
- [rate-limiter](https://github.com/NiHaLOO7/rate-limiter) — distributed sliding window + token bucket

## Project Structure

```
mini-redis/
├── src/
│   ├── hash_map.py       # HashMap with chaining
│   ├── linked_list.py    # DoublyLinkedList with trim_left/trim_right
│   ├── lru_cache.py      # LRU Cache (HashMap + DoublyLinkedList)
│   ├── min_heap.py       # MinHeap for TTL expiry
│   ├── skip_list.py      # SkipList for sorted sets
│   ├── store.py          # RedisStore (all commands)
│   ├── server.py         # TCP server (threading + select)
│   └── persistence.py    # AOF with base64 encoding
├── tests/
├── data/                  # AOF file stored here
├── Dockerfile
├── docker-compose.yml
├── deployment.yml         # Kubernetes deployment (3 replicas)
└── service.yml            # Kubernetes NodePort service
```

## Future Improvements

- Pub/Sub support
- Pipelining (batch commands)
- Cluster mode (sharding)
- RESP protocol compatibility
- Connection pooling
