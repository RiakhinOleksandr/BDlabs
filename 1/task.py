import psycopg2
from multiprocessing import Process
import time
import random

def reset_counter(connection, cursor, version = False, id = 1, rand = False):
    """ Resetting Counter and Version(if version parameter is True) values in database"""
    if rand:
        for i in range(1, 100001):
            cursor.execute("UPDATE lab1 SET Counter = 0 WHERE USER_ID = %s;", (i,))
            if version:
                cursor.execute("UPDATE lab1 SET Version = 1 WHERE USER_ID = %s;", (i,))
    else:
        cursor.execute("UPDATE lab1 SET Counter = 0 WHERE USER_ID = %s;", (id,))
        if version:
            cursor.execute("UPDATE lab1 SET Version = 1 WHERE USER_ID = %s;", (id,))
    connection.commit()

def lost_update(id = 1, rand = False):
    """ Lost-update variation """
    conn = psycopg2.connect(database = "bd", user = "postgres", password = "12345678")
    cur = conn.cursor()
    for i in range(1, 10001):
        if rand:
            id = random.randint(1, 100000)
        cur.execute("SELECT Counter FROM lab1 WHERE USER_ID = %s", (id,))
        counter = cur.fetchone()[0]
        counter +=  1
        cur.execute("UPDATE lab1 SET Counter = %s WHERE USER_ID = %s", (counter, id))
        conn.commit()
    cur.close()
    conn.close()

def inplace_update(id = 1, rand = False):
    """ In-place variation """
    conn = psycopg2.connect(database = "bd", user = "postgres", password = "12345678")
    cur = conn.cursor()
    for i in range(1, 10001):
        if rand:
            id = random.randint(1, 100000)
        cur.execute("UPDATE lab1 SET Counter = Counter + 1 WHERE USER_ID = %s", (id, ))
        conn.commit()
    cur.close()
    conn.close()

def row_level_locking(id = 1, rand = False):
    """ Row-level locking variation """
    conn = psycopg2.connect(database = "bd", user = "postgres", password = "12345678")
    cur = conn.cursor()
    for i in range(1, 10001):
        if rand:
            id = random.randint(1, 100000)
        cur.execute("SELECT Counter FROM lab1 WHERE USER_ID = %s FOR UPDATE", (id,))
        counter = cur.fetchone()[0]
        counter +=  1
        cur.execute("UPDATE lab1 SET Counter = %s WHERE USER_ID = %s", (counter, id))
        conn.commit()
    cur.close()
    conn.close()

def optimistic_concurency_control(id = 1, rand = False):
    """ Optimistic concurrency control variation """
    conn = psycopg2.connect(database = "bd", user = "postgres", password = "12345678")
    cur = conn.cursor()
    for i in range(1, 10001):
        if rand:
            id = random.randint(1, 100000)
        while True:
            cur.execute("SELECT Counter, Version FROM lab1 WHERE USER_ID = %s", (id,))
            counter, version = cur.fetchone()
            counter += 1
            cur.execute("UPDATE lab1 SET Counter = %s, Version = %s WHERE USER_ID = %s AND Version = %s", (counter, version + 1, id, version))
            conn.commit()
            count = cur.rowcount
            if count > 0:
                break
    cur.close()
    conn.close

if __name__ == '__main__':
    rand = False # Set False if there will be only one row. Set True if there will be 100000 and id will be chosen randomly

    # Preparing
    id = 1
    conn = psycopg2.connect(database = "bd", user = "postgres", password = "12345678") # Connecting to database
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS lab1(USER_ID SERIAL PRIMARY KEY, Counter INTEGER, Version INTEGER);") # Creating table if it doesn't exist
    cur.execute("SELECT * FROM lab1;")
    if len(cur.fetchall()) == 0:
        cur.execute("INSERT INTO lab1 VALUES (1, 0, 1);") # Adding row if table is empty
    else:
        cur.execute("UPDATE lab1 SET Counter = 0, Version = 1 WHERE USER_ID = %s;", (id,)) # Resetting Counter and Version 
    if rand:
        for i in range(2, 100001):
            cur.execute("INSERT INTO lab1 VALUES (%s, 0, 1);", (i,))
    conn.commit()

    # Варіант Lost-update
    start = time.time()

    processes = []
    for i in range(10):
        p = Process(target=lost_update, args=(id, rand)) # Creating processes and setting their target
        processes.append(p)
        p.start() # Starting processes
    
    while len(processes) > 0: # Waiting for all processes to finish
        processes = [p for p in processes if p.is_alive()]
        time.sleep(0.25)

    end = time.time()
    timer = round(end - start, 5)

    print(f"Lost-update variant took {timer} seconds")
    if rand:
        cur.execute("SELECT SUM(Counter) FROM lab1;")
        print(f"Total Counter: {cur.fetchone()[0]}\n")
    else:
        cur.execute("SELECT Counter FROM lab1 WHERE USER_ID = 1;")
        print(f"Counter: {cur.fetchone()[0]}\n")

    reset_counter(conn, cur, id = id, rand = rand)

    # Варіант In-place update
    start = time.time()

    processes = []
    for i in range(10):
        p = Process(target=inplace_update, args=(id, rand)) # Creating processes and setting their target
        processes.append(p)
        p.start() # Starting processes
    
    while len(processes) > 0: # Waiting for all processes to finish
        processes = [p for p in processes if p.is_alive()]
        time.sleep(0.25)

    end = time.time()
    timer = round(end - start, 5)

    print(f"In-place update variant took {timer} seconds")
    if rand:
        cur.execute("SELECT SUM(Counter) FROM lab1;")
        print(f"Total Counter: {cur.fetchone()[0]}\n")
    else:
        cur.execute("SELECT Counter FROM lab1 WHERE USER_ID = 1;")
        print(f"Counter: {cur.fetchone()[0]}\n")

    reset_counter(conn, cur, id = id, rand = rand)

    # Варіант Row-level locking
    start = time.time()

    processes = []
    for i in range(10):
        p = Process(target=row_level_locking, args=(id, rand)) # Creating processes and setting their target
        processes.append(p)
        p.start() # Starting processes
    
    while len(processes) > 0: # Waiting for all processes to finish
        processes = [p for p in processes if p.is_alive()]
        time.sleep(0.25)

    end = time.time()
    timer = round(end - start, 5)

    print(f"Row-level locking variant took {timer} seconds")
    if rand:
        cur.execute("SELECT SUM(Counter) FROM lab1;")
        print(f"Total Counter: {cur.fetchone()[0]}\n")
    else:
        cur.execute("SELECT Counter FROM lab1 WHERE USER_ID = 1;")
        print(f"Counter: {cur.fetchone()[0]}\n")

    reset_counter(conn, cur, id = id, rand = rand)

    # Варіант Optimistic concurrency control
    start = time.time()

    processes = []
    for i in range(10):
        p = Process(target=optimistic_concurency_control, args=(id, rand)) # Creating processes and setting their target
        processes.append(p)
        p.start() # Starting processes
    
    while len(processes) > 0: # Waiting for all processes to finish
        processes = [p for p in processes if p.is_alive()]
        time.sleep(0.25)

    end = time.time()
    timer = round(end - start, 5)

    print(f"Optimistic concurrency control variant took {timer} seconds")
    if rand:
        cur.execute("SELECT SUM(Counter) FROM lab1;")
        print(f"Total Counter: {cur.fetchone()[0]}\n")
    else:      
        cur.execute("SELECT Counter FROM lab1 WHERE USER_ID = 1;")
        print(f"Counter: {cur.fetchone()[0]}\n")

    reset_counter(conn, cur, version = True, id = id, rand = rand)

    if rand:
        cur.execute("DELETE FROM lab1 WHERE USER_ID > 1;")
        conn.commit()

    cur.close()
    conn.close()