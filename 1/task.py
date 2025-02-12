import psycopg2
from multiprocessing import Process
import time

def reset_counter(connection, cursor):
    cursor.execute("UPDATE lab1 SET Counter = 0 WHERE USER_ID = 1;")
    connection.commit()

def lost_update():
    conn = psycopg2.connect(database = "bd", user = "postgres", password = "12345678")
    cur = conn.cursor()
    for i in range(1, 10001):
        cur.execute("SELECT Counter FROM lab1 WHERE USER_ID = 1")
        counter = cur.fetchone()[0]
        counter = counter + 1
        cur.execute("UPDATE lab1 SET Counter = %s WHERE USER_ID = %s", (counter, 1))
        conn.commit()
    cur.close()
    conn.close()

def inplace_update():
    conn = psycopg2.connect(database = "bd", user = "postgres", password = "12345678")
    cur = conn.cursor()
    for i in range(1, 10001):
        cur.execute("UPDATE lab1 SET Counter = Counter + 1 WHERE USER_ID = 1")
        conn.commit()
    cur.close()
    conn.close()

def row_level_locking():
    conn = psycopg2.connect(database = "bd", user = "postgres", password = "12345678")
    cur = conn.cursor()
    for i in range(1, 10001):
        cur.execute("SELECT Counter FROM lab1 WHERE USER_ID = 1 FOR UPDATE")
        counter = cur.fetchone()[0]
        counter = counter + 1
        cur.execute("UPDATE lab1 SET Counter = %s WHERE USER_ID = %s", (counter, 1))
        conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    # Preparing
    conn = psycopg2.connect(database = "bd", user = "postgres", password = "12345678")
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS lab1(USER_ID serial PRIMARY KEY, Counter INTEGER, Version INTEGER);")
    cur.execute("SELECT * FROM lab1;")
    if len(cur.fetchall()) == 0:
        cur.execute("INSERT INTO lab1 VALUES (1, 0, 1);")
    else:
        cur.execute("UPDATE lab1 SET Counter = 0 WHERE USER_ID = 1;")
    conn.commit()

    # Варіант Lost-update
    start = time.time()

    processes = []
    for i in range(10):
        p = Process(target=lost_update)
        processes.append(p)
        p.start()
    
    while len(processes) > 0:
        processes = [p for p in processes if p.is_alive()]
        time.sleep(0.25)

    end = time.time()
    timer = end - start

    print(f"Lost-update variant took {timer} seconds")
    cur.execute("SELECT Counter FROM lab1 WHERE USER_ID = 1")
    print(f"Counter: {cur.fetchone()[0]}\n")

    reset_counter(conn, cur)

    # Варіант In-place update
    start = time.time()

    processes = []
    for i in range(10):
        p = Process(target=inplace_update)
        processes.append(p)
        p.start()
    
    while len(processes) > 0:
        processes = [p for p in processes if p.is_alive()]
        time.sleep(0.25)

    end = time.time()
    timer = end - start

    print(f"In-place update variant took {timer} seconds")
    cur.execute("SELECT Counter FROM lab1 WHERE USER_ID = 1")
    print(f"Counter: {cur.fetchone()[0]}\n")

    reset_counter(conn, cur)

    # Варіант Row-level locking
    start = time.time()

    processes = []
    for i in range(10):
        p = Process(target=row_level_locking)
        processes.append(p)
        p.start()
    
    while len(processes) > 0:
        processes = [p for p in processes if p.is_alive()]
        time.sleep(0.25)

    end = time.time()
    timer = end - start

    print(f"Row-level locking variant took {timer} seconds")
    cur.execute("SELECT Counter FROM lab1 WHERE USER_ID = 1")
    print(f"Counter: {cur.fetchone()[0]}\n")

    reset_counter(conn, cur)

    cur.close()
    conn.close()