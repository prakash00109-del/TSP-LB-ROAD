import sqlite3

DB_NAME = "pg.db"


# -------------------------
# DATABASE CONNECTION
# -------------------------

def connect():

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# -------------------------
# INITIALIZE DATABASE
# -------------------------

def init_db():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS rooms(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        floor TEXT,
        room TEXT,
        bed TEXT,

        tenant_name TEXT,
        father_name TEXT,
        mother_name TEXT,

        address TEXT,
        street TEXT,
        area TEXT,
        pincode TEXT,

        aadhar_number TEXT,
        dob TEXT,
        email TEXT,
        phone TEXT,

        office_name TEXT,
        office_address TEXT,

        deposit TEXT,
        rent TEXT,

        room_type TEXT,
        checkin_date TEXT,

        emergency_name TEXT,
        emergency_phone TEXT,
        emergency_relation TEXT,

        photo BLOB,
        aadhar BLOB

    )
    """)

    conn.commit()
    conn.close()


# -------------------------
# ADD FLOOR
# -------------------------

def add_floor(floor):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO rooms (floor, room, bed) VALUES (?, '', '')",
        (floor,)
    )

    conn.commit()
    conn.close()

    return True


# -------------------------
# CREATE ROOM
# -------------------------

def create_room(floor, room):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM rooms
    WHERE floor=? AND room=? AND bed=''
    """, (floor, room))

    exists = cur.fetchone()

    if not exists:

        cur.execute(
            "INSERT INTO rooms (floor, room, bed) VALUES (?, ?, '')",
            (floor, room)
        )

    conn.commit()
    conn.close()

    return True


# -------------------------
# ADD BEDS
# -------------------------

def add_beds(floor, room, beds):

    conn = connect()
    cur = conn.cursor()

    for i in range(1, beds + 1):

        bed = f"Bed{i}"

        cur.execute("""
        SELECT * FROM rooms
        WHERE floor=? AND room=? AND bed=?
        """, (floor, room, bed))

        exists = cur.fetchone()

        if not exists:

            cur.execute(
                "INSERT INTO rooms (floor, room, bed) VALUES (?, ?, ?)",
                (floor, room, bed)
            )

    conn.commit()
    conn.close()

    return True


# -------------------------
# GET ALL BEDS
# -------------------------

def get_beds():

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM rooms")

    rows = cur.fetchall()

    conn.close()

    return rows


# -------------------------
# GET SINGLE TENANT BY ID
# -------------------------

def get_tenant(bed_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM rooms WHERE id=?",
        (bed_id,)
    )

    row = cur.fetchone()

    conn.close()

    return row


# -------------------------
# ADD TENANT (FULL PROFILE)
# -------------------------

def add_tenant(data, photo, aadhar):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    UPDATE rooms SET

        tenant_name=?,
        father_name=?,
        mother_name=?,
        address=?,
        street=?,
        area=?,
        pincode=?,
        aadhar_number=?,
        dob=?,
        email=?,
        phone=?,
        office_name=?,
        office_address=?,
        deposit=?,
        rent=?,
        room_type=?,
        checkin_date=?,
        emergency_name=?,
        emergency_phone=?,
        emergency_relation=?,
        photo=?,
        aadhar=?

    WHERE floor=? AND room=? AND bed=?
    """, (

        data.get("name"),
        data.get("father"),
        data.get("mother"),
        data.get("address"),
        data.get("street"),
        data.get("area"),
        data.get("pincode"),
        data.get("aadhar_number"),
        data.get("dob"),
        data.get("email"),
        data.get("phone"),
        data.get("office_name"),
        data.get("office_address"),
        data.get("deposit"),
        data.get("rent"),
        data.get("room_type"),
        data.get("checkin"),
        data.get("emergency_name"),
        data.get("emergency_phone"),
        data.get("emergency_relation"),
        photo,
        aadhar,

        data.get("floor"),
        data.get("room"),
        data.get("bed")

    ))

    conn.commit()
    conn.close()

    return True


# -------------------------
# REMOVE TENANT
# -------------------------

def remove_tenant(floor, room, bed):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    UPDATE rooms SET

        tenant_name=NULL,
        father_name=NULL,
        mother_name=NULL,
        address=NULL,
        street=NULL,
        area=NULL,
        pincode=NULL,
        aadhar_number=NULL,
        dob=NULL,
        email=NULL,
        phone=NULL,
        office_name=NULL,
        office_address=NULL,
        deposit=NULL,
        rent=NULL,
        room_type=NULL,
        checkin_date=NULL,
        emergency_name=NULL,
        emergency_phone=NULL,
        emergency_relation=NULL,
        photo=NULL,
        aadhar=NULL

    WHERE floor=? AND room=? AND bed=?
    """, (floor, room, bed))

    conn.commit()
    conn.close()

    return True


# -------------------------
# UPDATE TENANT BASIC INFO
# -------------------------

def update_tenant(old_name, name, phone):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    UPDATE rooms
    SET tenant_name=?, phone=?
    WHERE tenant_name=?
    """, (name, phone, old_name))

    conn.commit()
    conn.close()

    return True


# -------------------------
# DELETE FLOOR
# -------------------------

def delete_floor(floor):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM rooms WHERE floor=?",
        (floor,)
    )

    conn.commit()
    conn.close()

    return True


# -------------------------
# DELETE ROOM
# -------------------------

def delete_room(floor, room):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    DELETE FROM rooms
    WHERE floor=? AND room=?
    """, (floor, room))

    conn.commit()
    conn.close()

    return True


# -------------------------
# DELETE BED
# -------------------------

def delete_bed(floor, room, bed):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    DELETE FROM rooms
    WHERE floor=? AND room=? AND bed=?
    """, (floor, room, bed))

    conn.commit()
    conn.close()

    return True
