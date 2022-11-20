#Create SQLite database
import sqlite3

#Create database with name of ctf
def create_tchallenge(db_name):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("CREATE TABLE challenges (id integer primary key, nameid text, name text, points integer, description text, flag text, d_history integer)")
    conn.commit()
    conn.close()

def create_thistory(db_name):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("CREATE TABLE history (id integer primary key, description text)")
    conn.commit()
    conn.close()

#Create database for players
def create_tuser(db_name):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("CREATE TABLE users (id integer primary key, points integer, challengesdone text)")
    conn.commit()
    conn.close()

#Create table for ctf
def create_ctf():
    conn = sqlite3.connect("/root/oka/core.db")
    c = conn.cursor()
    c.execute("CREATE TABLE ctf (id integer primary key, name text, active int)")
    conn.commit()
    conn.close()

#Add ctf to database
def add_ctf(name):
    conn = sqlite3.connect("/root/oka/core.db")
    c = conn.cursor()
    c.execute("INSERT INTO ctf (name, active) VALUES (?, ?)", (name, 0))
    conn.commit()
    conn.close()

#Add challenge to database
def add_challenge(db_name, name, points, flag):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("INSERT INTO challenges (nameid, points, flag) VALUES (?, ?, ?)", (name, points, flag))
    conn.commit()
    conn.close()

#Ajoute un history
def add_history(db_name, description):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("INSERT INTO history (description) VALUES (?)", (description,))
    conn.commit()
    conn.close()

#Ajoute un joueur
def add_user(db_name, id):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("INSERT INTO users (id, points, challengesdone) VALUES (?, ?, ?)", (id, 0, ""))
    conn.commit()
    conn.close()

#Set active ctf
def set_active_ctf(name):
    conn = sqlite3.connect("/root/oka/core.db")
    c = conn.cursor()
    c.execute("UPDATE ctf SET active = 0")
    c.execute("UPDATE ctf SET active = 1 WHERE name = ?", (name,))
    conn.commit()
    conn.close()

#Update name of challenge
def update_name(db_name, nameid, name):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("UPDATE challenges SET name = ? WHERE nameid = ?", (name, nameid))
    conn.commit()
    conn.close()

#Update points of challenge
def update_points(db_name, id, points):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("UPDATE challenges SET points = ? WHERE nameid = ?", (points, id))
    conn.commit()
    conn.close()

#Update description of challenge
def update_description(db_name, id, description):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("UPDATE challenges SET description = ? WHERE nameid = ?", (description, id))
    conn.commit()
    conn.close()

#Update flag of challenge
def update_flag(db_name, id, flag):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("UPDATE challenges SET flag = ? WHERE nameid = ?", (flag, id))
    conn.commit()
    conn.close()

#Update history of challenge
def update_history(db_name, id, d_history):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("UPDATE challenges SET d_history = ? WHERE nameid = ?", (d_history, id))
    conn.commit()
    conn.close()

#Update score of player
def update_score(db_name, id, points):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("UPDATE users SET points = ? WHERE id = ?", (points, id))
    conn.commit()
    conn.close()

#Update challenges done of player
def update_challengesdone(db_name, id, challengesdone):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("UPDATE users SET challengesdone = ? WHERE id = ?", (challengesdone, id))
    conn.commit()
    conn.close()

def get_challengesdone(db_name, id):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("SELECT challengesdone FROM users WHERE id = ?", (id,))
    challengesdone = c.fetchone()
    conn.close()
    return challengesdone

#Get classement of players
def get_classement(db_name):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM users ORDER BY points DESC")
    classement = c.fetchall()
    conn.close()
    return classement

#Get challenge nameid by flag
def get_nameid(db_name, flag):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("SELECT nameid FROM challenges WHERE flag = ?", (flag,))
    nameid = c.fetchone()
    conn.close()
    return nameid

#Get score of player
def get_score(db_name, id):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("SELECT points FROM users WHERE id = ?", (id,))
    score = c.fetchone()
    conn.close()
    return score

#Get score of challenge with flag
def get_points(db_name, flag):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("SELECT points FROM challenges WHERE flag = ?", (flag,))
    points = c.fetchone()
    conn.close()
    return points

#Get challenge from database
def get_challenge(db_name, id):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM challenges WHERE id = ?", (id,))
    challenge = c.fetchone()
    conn.close()
    return challenge

#Get active ctf
def get_active_ctf():
    conn = sqlite3.connect("/root/oka/core.db")
    c = conn.cursor()
    c.execute("SELECT name FROM ctf WHERE active = 1")
    ctf = c.fetchone()
    conn.close()
    return ctf

#Get all players
def get_all_players(db_name):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("SELECT id FROM users")
    players = c.fetchall()
    conn.close()
    return players

#Get id of history from challenge
def get_history_id(db_name, flag):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("SELECT d_history FROM challenges WHERE flag = ?", (flag,))
    history_id = c.fetchone()
    conn.close()
    return history_id

#Get all challenge from database
def get_all_challenges(db_name):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM challenges")
    challenges = c.fetchall()
    conn.close()
    return challenges

#Get all history from database
def get_all_history(db_name):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM history")
    history = c.fetchall()
    conn.close()
    return history

#Get history
def get_history(db_name, id):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("SELECT description FROM history WHERE id = ?", (id,))
    history = c.fetchone()
    conn.close()
    return history

#Check if challenge with flag
def check_flag(db_name, flag):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("SELECT flag FROM challenges WHERE flag = ?", (flag,))
    challenge = c.fetchone()
    conn.close()

    if challenge is None:
        return False
    else:
        return True

#Check if player exists
def check_player(db_name, id):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE id = ?", (id,))
    player = c.fetchone()
    conn.close()

    if player is None:
        return False
    else:
        return True

#Remove challenge from database
def remove_challenge(db_name, id):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("DELETE FROM challenges WHERE nameid = ?", (id,))
    conn.commit()
    conn.close()

#Remove player from database
def remove_player(db_name, id):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()
    conn.close()

#Remove ctf from database
def remove_ctf(db_name, name):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("DELETE FROM ctf WHERE name = ?", (name,))
    conn.commit()
    conn.close()

#remove history from database
def remove_history(db_name, id):
    conn = sqlite3.connect("/root/oka/" + db_name)
    c = conn.cursor()
    c.execute("DELETE FROM history WHERE id = ?", (id,))
    conn.commit()
    conn.close()

#Drop CTF
def drop_ctf():
    conn = sqlite3.connect("/root/oka/core.db")
    c = conn.cursor()
    c.execute("DROP TABLE ctf")
    conn.commit()
    conn.close()