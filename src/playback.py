import psycopg2
import time
import sys
import collections
import MySQLdb

def assertEqual(a,b):
    if(a != b):
        print("expected: " + str(a))
        print("got: " + str(b))
        assert False

def replay_memory(stream):
    tovisit = collections.deque([sys.argv[1] + '\n'])
    visited = set()
    visited.add(sys.argv[1] + '\n')

    i = 0
    z = 0
    for line in stream:
        i += 1
        #print(i)
        if(line[0] == '1'):#pop from tovisit queue
            result = tovisit.pop()
            #assertEqual(result, line[1:])
        elif(line[0] == '2'):#check if url exists
            expected_value = line[1] == 'y'
            z += int(line[2:] in visited)
            #assertEqual((line[2:] in visited), expected_value)
        elif(line[0] == '3'):#insert into visited and tovisit
            tovisit.appendleft(line[1:])
            visited.add(line[1:])
    print z

def replay_memory_and_fix(stream):
    tovisit = collections.deque([sys.argv[1] + '\n'])
    visited = set()
    visited.add(sys.argv[1] + '\n')

    for line in stream:
        if(line[0] == '1'):#pop from tovisit queue
            sys.stdout.write(line)
            result = tovisit.pop()
            #assertEqual(result, line[1:])
        elif(line[0] == '2'):#check if url exists
            sys.stdout.write(line)
            expected_value = line[1] == 'y'
            #assertEqual((line[2:] in visited), expected_value)
        elif(line[0] == '3'):#insert into visited and tovisit
            if(line[1:] not in visited):
                tovisit.appendleft(line[1:])
                visited.add(line[1:])
                sys.stdout.write(line)
            else:
                sys.stderr.write(line[1:])



def replay_postgres(stream):
    db = psycopg2.connect(host='localhost', database="crawler", user="postgres", password="password")
    cursor = db.cursor()

    visited_table = "visited"
    tovisit_table = "tovisit"
    cursor.execute("DROP TABLE IF EXISTS " + visited_table)
    cursor.execute("CREATE TABLE " + visited_table + " (url VARCHAR(1024) PRIMARY KEY)")
    cursor.execute("DROP TABLE IF EXISTS " + tovisit_table)
    cursor.execute(u"CREATE TABLE " + tovisit_table + " (id SERIAL PRIMARY KEY, url VARCHAR(1024))")

    cursor.execute(u"INSERT INTO " + visited_table + " VALUES (%s)", (sys.argv[1],))
    cursor.execute(u"INSERT INTO " + tovisit_table + " VALUES (DEFAULT, %s)", (sys.argv[1],))

    for line in stream:
        if(line[0] == '1'):#pop from tovisit queue
            cursor.execute("SELECT * FROM " + tovisit_table + " ORDER BY id LIMIT 1")
            row = cursor.fetchone()
            row_id = row[0]
            result = row[1]
            cursor.execute("DELETE FROM " + tovisit_table + " WHERE id=%s", (row_id,))

            #assertEqual(result, line[1:])
        elif(line[0] == '2'):#check if url exists
            expected_value = line[1] == 'y'

            cursor.execute(u"SELECT EXISTS(SELECT * FROM " + visited_table + " WHERE url=%s)",(line[2:],))
            exists = bool(cursor.fetchone()[0])
            #assertEqual(exists, expected_value)
        elif(line[0] == '3'):#insert into visited and tovisit
            cursor.execute(u"INSERT INTO " + tovisit_table + u" VALUES (DEFAULT , %s)", (line[1:],))
            cursor.execute(u"INSERT INTO " + visited_table + u" VALUES (%s)", (line[1:],))

def replay_mysql(stream):
    db = MySQLdb.connect(host="localhost", user="root", passwd="password", db="crawler", charset="utf8")
    cursor = db.cursor()

    visited_table = "visited"
    tovisit_table = "tovisit"
    cursor.execute("DROP TABLE IF EXISTS " + visited_table)
    cursor.execute("CREATE TABLE " + visited_table + " (url VARCHAR(1024), PRIMARY KEY(url)) ROW_FORMAT=DYNAMIC")
    cursor.execute("DROP TABLE IF EXISTS " + tovisit_table)
    cursor.execute("CREATE TABLE " + tovisit_table + " (id INT NOT NULL AUTO_INCREMENT, url VARCHAR(1024), PRIMARY KEY(id))")

    cursor.execute(u"INSERT INTO " + tovisit_table + " VALUES (DEFAULT, %s)", (sys.argv[1],))
    cursor.execute(u"INSERT INTO " + visited_table + " VALUES (%s)", (sys.argv[1],))

    for line in stream:
        if(line[0] == '1'):#pop from tovisit queue
            cursor.execute("SELECT * FROM " + tovisit_table + " ORDER BY id LIMIT 1")
            row = cursor.fetchone()
            row_id = row[0]
            result = row[1]
            cursor.execute("DELETE FROM " + tovisit_table + " WHERE id=%s", (row_id,))

            #assertEqual(result, line[1:])
        elif(line[0] == '2'):#check if url exists
            expected_value = line[1] == 'y'

            #mysql implementation does check and insert in one go
            if(cursor.execute(u"INSERT INTO " + visited_table + u" VALUES (%s) ON DUPLICATE KEY UPDATE url=url", (line[1:],))):
                cursor.execute(u"INSERT INTO " + tovisit_table + u" VALUES (DEFAULT , %s)", (line[1:],))

if __name__ == "__main__":
    #start = time.time()
    #replay_memory(sys.stdin)
    #print "memory: " + str(time.time() - start)

    #start = time.time()
    #replay_postgres(sys.stdin)
    #print "postgres: " + str(time.time() - start)

    start = time.time()
    replay_mysql(sys.stdin)
    print "mysql: " + str(time.time() - start)