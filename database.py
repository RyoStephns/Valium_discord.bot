import sqlite3 as sql
def Table():
    conn = sql.connect('data.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE players (
                name text,
                id int,
                lvl int,
                credit int, 
                hp int,
                hplim int, 
                str int, 
                vit int,
                def int,
                exp int,
                expup int, 
                mp int,
                mplim int,
                intel int
            )""")
    c.execute("""CREATE TABLE usable (
                id int,
                pots int,
                potm int,
                potl int,
                dgate int, 
                cgate int,
                bgate int, 
                agate int,
                sgate int
            )""")
    print('Succesfully create table')
    conn.commit()
    conn.close()

def CheckID(ID):
    conn = sql.connect('data.db')
    c= conn.cursor()
    c.execute("SELECT id FROM players")
    Ids=c.fetchall()
    val=(len(Ids))
    for i in range(val):
        check=(Ids[i][0])
        if check == ID:
            return True
    conn.close()

def Create_Account(id,name):
    conn = sql.connect('data.db')
    c= conn.cursor()
    c.execute(f"INSERT INTO players VALUES('{name}','{id}','1','1000','60','60','4','4','0','0','40','20','20','0')")
    c.execute(f"INSERT INTO usable VALUES('{id}','5','0','0','0','0','0','0',0)")
    print('Succesfully add player')
    conn.commit()
    conn.close()

def Read():
    conn = sql.connect('data.db')
    c= conn.cursor()
    c.execute(f"SELECT * FROM players")
    items = c.fetchall()
    number= 1
    data = []
    print('==============')
    for i in items:
        print(f'{number}.{i}')
        number += 1
        data.append(i)
    print('==============')
    conn.close()
    return data

def Check(ID,types):
    conn = sql.connect('data.db')
    c= conn.cursor()
    c.execute(f"SELECT {types} FROM players WHERE id = '{ID}' ")
    items = c.fetchall()[0][0]
    conn.close()
    return(items)

def Usable(ID):
    conn = sql.connect('data.db')
    c= conn.cursor()
    c.execute(f"SELECT * FROM usable WHERE id = '{ID}' ")
    items = c.fetchall()[0][1:8]
    conn.close()
    return(items)

def CheckUsable(ID,TYPE):
    conn = sql.connect('data.db')
    c= conn.cursor()
    c.execute(f"SELECT {TYPE} FROM usable WHERE id = '{ID}' ")
    items = c.fetchall()[0][0]
    conn.close()
    return(items)

def Edit(id=None,typ=None,add=True,val=None):
    conn = sql.connect('data.db')
    c= conn.cursor()
    if add == True:
        c.execute(f"SELECT {typ} FROM players WHERE id = '{id}'")
        data= c.fetchall()[0][0]
        edit= data+val
        c.execute(f"UPDATE players SET {typ} = '{edit}' WHERE id = '{id}' ")
    elif add == False:
        c.execute(f"SELECT {typ} FROM players WHERE id = '{id}'")
        data= c.fetchall()[0][0]
        edit= data-val
        c.execute(f"UPDATE players SET {typ} = '{edit}' WHERE id = '{id}' ")
    conn.commit()
    conn.close()

def Set(id=None,typ=None,val=None):
    conn = sql.connect('data.db')
    c= conn.cursor()
    c.execute(f"SELECT {typ} FROM players WHERE id = '{id}'")
    c.execute(f"UPDATE players SET {typ} = '{val}' WHERE id = '{id}' ")
    conn.commit()
    conn.close()
def SetZero(id,typ):
    conn = sql.connect('data.db')
    c= conn.cursor()
    value = 0
    c.execute(f"SELECT {typ} FROM players WHERE id = '{id}'")
    c.execute(f"UPDATE players SET {typ} = '{value}' WHERE id = '{id}' ")
    conn.commit()
    conn.close()
    return value

def EditUsable(id=None,typ=None,add=True,val=None):
    conn = sql.connect('data.db')
    c= conn.cursor()
    if add == True:
        c.execute(f"SELECT {typ} FROM usable WHERE id = '{id}'")
        data= c.fetchall()[0][0]
        edit= data+val
        c.execute(f"UPDATE usable SET {typ} = '{edit}' WHERE id = '{id}' ")
    elif add == False:
        c.execute(f"SELECT {typ} FROM usable WHERE id = '{id}'")
        data= c.fetchall()[0][0]
        edit= data-val
        c.execute(f"UPDATE usable SET {typ} = '{edit}' WHERE id = '{id}' ")
    conn.commit()
    conn.close()

def intro(user):
    test=CheckID(user)
    pots=['Potion(S)', CheckUsable(user,'pots')]
    potl=['Potion(M)', CheckUsable(user,'potm')]
    potm=['Potion(L)', CheckUsable(user,'potl')]
    dkey=['D-Gate Key',CheckUsable(user,'dgate')]
    ckey=['C-Gate Key',CheckUsable(user,'cgate')]
    bkey=['B-Gate Key',CheckUsable(user,'bgate')]
    akey=['A-Gate Key',CheckUsable(user,'agate')]
    skey=['A-Gate Key',CheckUsable(user,'sgate')]
    if test == False:
        return False
    else:
        name= [pots[0],potm[0],potl[0],dkey[0],ckey[0],bkey[0],akey[0]]
        value=[pots[1],potm[1],potl[1],dkey[1],ckey[1],bkey[1],akey[1]]
        num=[]
        for i in range(0,7):
            if value[i] > 0:
                num.append(i)
            else:
                continue
        leng=(len(num))
        items=[]
        for i in range(leng):
            chk=num[i]
            items.append([name[chk],value[chk]])
        return items

def delete(id):
    conn = sql.connect('data.db')
    c= conn.cursor()
    c.execute(f"DELETE FROM players WHERE id = '{id}'")
    conn.commit()
    conn.close()
# =============================================================