import redis

# 测试连接redis
"""
if __name__ == '__main__':
    conn = redis.Redis(host='127.0.0.1', port=6379)
    if conn:
        print('ok')
    else:
        print('error')
"""
# 测试session是否保存在redis中
"""
if __name__ == '__main__':
    conn = redis.Redis(host='127.0.0.1', port=6379, password='foobared')
    print(conn.keys())
"""
"""
[
    b'session:eyJjc3JmX3Rva2VuIjoiNWNhMTdiYzJlOGFkZjc5NDZjODA0ODkzNzk4NTY2NzIxYjBkNWVmNiIsInVzZXIiOiJlcmljcyIsInVzZXJfaWQiOjF9.Xw2bFQ.tYod_F02MDofFCLR3aUs5BBEKQs',
    b'session:eyJjc3JmX3Rva2VuIjoiNWNhMTdiYzJlOGFkZjc5NDZjODA0ODkzNzk4NTY2NzIxYjBkNWVmNiIsInVzZXJfaWQiOjF9.Xwt53A.ucQMG-hSprAb8YMhWep-lY2RqCE'
]
"""
