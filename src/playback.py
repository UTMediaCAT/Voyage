import psycopg2
import time
import sys
import collections

def assertEqual(a,b):
    if(a != b):
        print("expected: " + str(a))
        print("got: " + str(b))
        assert False

def replay_memory(stream):
    tovisit = collections.deque(["dummy"])
    visited = set()
    visited.add("dummy")
    for line in stream:
        if(line[0] == '1'):#pop from tovisit queue
            assertEqual(tovisit.pop(), line[1:])
        elif(line[0] == '2'):#check if url exists
            expected_value = line[1] == 'y'
            assertEqual((line[2:] in visited), expected_value)
        elif(line[0] == '3'):#insert into visited and tovisit
            tovisit.appendleft(line[1:])
            visited.add(line[1:])


def replay_postgres(stream):
    db = psycopg2.connect(host='localhost', database="crawler", user="postgres", password="password")
    cursor = db.cursor()

    visited_table = "visited"
    tovisit_table = "tovisit"
    cursor.execute("DROP TABLE IF EXISTS " + visited_table)
    cursor.execute("CREATE TABLE " + visited_table + " (url VARCHAR(1024) PRIMARY KEY)")
    cursor.execute("DROP TABLE IF EXISTS " + tovisit_table)
    cursor.execute(u"CREATE TABLE " + tovisit_table + " (id SERIAL PRIMARY KEY, url VARCHAR(1024))")

    cursor.execute(u"INSERT INTO " + visited_table + " VALUES (%s)", ("dummy",))
    cursor.execute(u"INSERT INTO " + tovisit_table + " VALUES (DEFAULT, %s)", ("dummy",))

    for line in stream:
        if(line[0] == '1'):#pop from tovisit queue
            cursor.execute("SELECT * FROM " + tovisit_table + " ORDER BY id LIMIT 1")
            row = cursor.fetchone()
            row_id = row[0]
            current_url = row[1]
            cursor.execute("DELETE FROM " + tovisit_table + " WHERE id=%s", (row_id,))

            assertEqual(current_url, line[1:])
        elif(line[0] == '2'):#check if url exists
            expected_value = line[1] == 'y'

            cursor.execute(u"SELECT EXISTS(SELECT * FROM " + visited_table + " WHERE url=%s)",(line[2:],))
            exists = bool(cursor.fetchone()[0])
            assertEqual(exists, expected_value)
        elif(line[0] == '3'):#insert into visited and tovisit
            cursor.execute(u"INSERT INTO " + tovisit_table + u" VALUES (DEFAULT , %s)", (line[1:],))
            cursor.execute(u"INSERT INTO " + visited_table + u" VALUES (%s)", (line[1:],))

if __name__ == "__main__":
    start = time.time()
    replay_memory(sys.stdin)
    print "memory: " + (time.time() - start)

    #start = time.time()
    #replay_postgres(sys.stdin)
    #print "memory: " + (time.time() - start)