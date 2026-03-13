from flask import Flask, request, jsonify, render_template, send_file
from database import *
import io
import tempfile

# ReportLab imports for PDF generation
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors

app = Flask(__name__)

# -------------------------
# INITIALIZE DATABASE
# -------------------------

init_db()


# -------------------------
# HOME PAGE
# -------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -------------------------
# ADD FLOOR
# -------------------------

@app.route("/add_floor", methods=["POST"])
def add_floor_api():

    data = request.json
    floor = data.get("floor")

    success = add_floor(floor)

    return jsonify({"success": success})


# -------------------------
# DELETE FLOOR
# -------------------------

@app.route("/delete_floor", methods=["POST"])
def delete_floor_api():

    data = request.json
    floor = data.get("floor")

    success = delete_floor(floor)

    return jsonify({"success": success})


# -------------------------
# ADD ROOM
# -------------------------

@app.route("/add_room", methods=["POST"])
def add_pg_room():

    data = request.json

    floor = data.get("floor")
    room = data.get("room")

    success = create_room(floor, room)

    return jsonify({"success": success})


# -------------------------
# DELETE ROOM
# -------------------------

@app.route("/delete_room", methods=["POST"])
def delete_room_api():

    data = request.json

    floor = data.get("floor")
    room = data.get("room")

    success = delete_room(floor, room)

    return jsonify({"success": success})


# -------------------------
# ADD BEDS
# -------------------------

@app.route("/add_beds", methods=["POST"])
def add_beds_api():

    data = request.json

    floor = data.get("floor")
    room = data.get("room")
    beds = int(data.get("beds"))

    success = add_beds(floor, room, beds)

    return jsonify({"success": success})


# -------------------------
# DELETE BED
# -------------------------

@app.route("/delete_bed", methods=["POST"])
def delete_bed_api():

    data = request.json

    floor = data.get("floor")
    room = data.get("room")
    bed = data.get("bed")

    success = delete_bed(floor, room, bed)

    return jsonify({"success": success})


# -------------------------
# GET ALL BEDS
# -------------------------

@app.route("/beds", methods=["GET"])
def get_all_beds():

    beds = get_beds()

    result = []

    for row in beds:

        result.append({
            "id": row["id"],
            "floor": row["floor"],
            "room": row["room"],
            "bed": row["bed"],
            "tenant": row["tenant_name"],
            "phone": row["phone"],
            "join_date": row["checkin_date"]
        })

    return jsonify(result)


# -------------------------
# ADD TENANT
# -------------------------

@app.route("/add_tenant", methods=["POST"])
def add_pg_tenant():

    data = {

        "name": request.form.get("name"),
        "father": request.form.get("father"),
        "mother": request.form.get("mother"),

        "address": request.form.get("address"),
        "street": request.form.get("street"),
        "area": request.form.get("area"),
        "pincode": request.form.get("pincode"),

        "aadhar_number": request.form.get("aadhar_number"),
        "dob": request.form.get("dob"),
        "email": request.form.get("email"),
        "phone": request.form.get("phone"),

        "office_name": request.form.get("office_name"),
        "office_address": request.form.get("office_address"),

        "deposit": request.form.get("deposit"),
        "rent": request.form.get("rent"),

        "room_type": request.form.get("room_type"),
        "checkin": request.form.get("checkin"),

        "emergency_name": request.form.get("emergency_name"),
        "emergency_phone": request.form.get("emergency_phone"),
        "emergency_relation": request.form.get("emergency_relation"),

        "floor": request.form.get("floor").strip(),
        "room": request.form.get("room").strip(),
        "bed": request.form.get("bed").strip()
    }

    photo_data = None
    aadhar_data = None

    if "photo" in request.files:
        photo_data = request.files["photo"].read()

    if "aadhar" in request.files:
        aadhar_data = request.files["aadhar"].read()

    success = add_tenant(data, photo_data, aadhar_data)

    return jsonify({"success": success})


# -------------------------
# REMOVE TENANT
# -------------------------

@app.route("/remove_tenant", methods=["POST"])
def remove_pg_tenant():

    data = request.json

    floor = data.get("floor")
    room = data.get("room")
    bed = data.get("bed")

    success = remove_tenant(floor, room, bed)

    return jsonify({"success": success})


# -------------------------
# UPDATE TENANT
# -------------------------

@app.route("/update_tenant", methods=["POST"])
def update_pg_tenant():

    data = request.json

    old_name = data.get("old_name")
    name = data.get("name")
    phone = data.get("phone")

    success = update_tenant(old_name, name, phone)

    return jsonify({"success": success})


# -------------------------
# GET TENANT PHOTO
# -------------------------

@app.route("/photo/<int:bed_id>")
def get_photo(bed_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT photo FROM rooms WHERE id=?", (bed_id,))
    row = cur.fetchone()

    conn.close()

    if row and row[0]:

        return send_file(
            io.BytesIO(row[0]),
            mimetype="image/jpeg"
        )

    return "", 404


# -------------------------
# GET AADHAAR PHOTO
# -------------------------

@app.route("/aadhar/<int:bed_id>")
def get_aadhar(bed_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT aadhar FROM rooms WHERE id=?", (bed_id,))
    row = cur.fetchone()

    conn.close()

    if row and row[0]:

        return send_file(
            io.BytesIO(row[0]),
            mimetype="image/jpeg"
        )

    return "", 404


# -------------------------
# DOWNLOAD TENANT FORM PDF
# -------------------------

@app.route("/download_tenant/<int:bed_id>")
def download_tenant(bed_id):

    tenant = get_tenant(bed_id)

    if not tenant:
        return "Tenant not found", 404

    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("<b>PG TENANT REGISTRATION FORM</b>", styles["Title"]))
    elements.append(Spacer(1,20))

    # PERSONAL DETAILS
    elements.append(Paragraph("<b>Personal Details</b>", styles["Heading3"]))

    personal = [
        ["Name", tenant["tenant_name"]],
        ["Father Name", tenant["father_name"]],
        ["Mother Name", tenant["mother_name"]],
        ["DOB", tenant["dob"]],
        ["Phone", tenant["phone"]],
        ["Email", tenant["email"]],
        ["Aadhaar Number", tenant["aadhar_number"]],
    ]

    table = Table(personal, colWidths=[180,350])
    table.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),1,colors.grey),
        ("BACKGROUND",(0,0),(0,-1),colors.lightgrey)
    ]))

    elements.append(table)
    elements.append(Spacer(1,20))


    # ADDRESS
    elements.append(Paragraph("<b>Address</b>", styles["Heading3"]))

    address = [
        ["Address", tenant["address"]],
        ["Street", tenant["street"]],
        ["Area", tenant["area"]],
        ["Pincode", tenant["pincode"]],
    ]

    table = Table(address, colWidths=[180,350])
    table.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),1,colors.grey),
        ("BACKGROUND",(0,0),(0,-1),colors.lightgrey)
    ]))

    elements.append(table)
    elements.append(Spacer(1,20))


    # OFFICE DETAILS
    elements.append(Paragraph("<b>Office Details</b>", styles["Heading3"]))

    office = [
        ["Office Name", tenant["office_name"]],
        ["Office Address", tenant["office_address"]],
    ]

    table = Table(office, colWidths=[180,350])
    table.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),1,colors.grey),
        ("BACKGROUND",(0,0),(0,-1),colors.lightgrey)
    ]))

    elements.append(table)
    elements.append(Spacer(1,20))


    # EMERGENCY CONTACT
    elements.append(Paragraph("<b>Emergency Contact</b>", styles["Heading3"]))

    emergency = [
        ["Name", tenant["emergency_name"]],
        ["Phone", tenant["emergency_phone"]],
        ["Relation", tenant["emergency_relation"]],
    ]

    table = Table(emergency, colWidths=[180,350])
    table.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),1,colors.grey),
        ("BACKGROUND",(0,0),(0,-1),colors.lightgrey)
    ]))

    elements.append(table)
    elements.append(Spacer(1,20))


    # RENT DETAILS
    elements.append(Paragraph("<b>Rental Details</b>", styles["Heading3"]))

    rent = [
        ["Room Type", tenant["room_type"]],
        ["Deposit", tenant["deposit"]],
        ["Rent", tenant["rent"]],
        ["Check-in Date", tenant["checkin_date"]],
    ]

    table = Table(rent, colWidths=[180,350])
    table.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),1,colors.grey),
        ("BACKGROUND",(0,0),(0,-1),colors.lightgrey)
    ]))

    elements.append(table)
    elements.append(Spacer(1,30))


    # PHOTO
    if tenant["photo"]:
        photo_path = tempfile.NamedTemporaryFile(delete=False,suffix=".jpg").name
        with open(photo_path,"wb") as f:
            f.write(tenant["photo"])

        elements.append(Paragraph("<b>Tenant Photo</b>", styles["Heading3"]))
        elements.append(Image(photo_path,2*inch,2*inch))
        elements.append(Spacer(1,20))


    # AADHAAR
    if tenant["aadhar"]:
        aadhar_path = tempfile.NamedTemporaryFile(delete=False,suffix=".jpg").name
        with open(aadhar_path,"wb") as f:
            f.write(tenant["aadhar"])

        img = Image(aadhar_path)
        img.drawHeight = 3*inch
        img.drawWidth = img.drawHeight * (img.imageWidth / img.imageHeight)

        elements.append(Paragraph("<b>Aadhaar Card</b>", styles["Heading3"]))
        elements.append(img)

    elements.append(Spacer(1,40))

    elements.append(Paragraph("Tenant Signature: ____________________", styles["Normal"]))
    elements.append(Spacer(1,20))
    elements.append(Paragraph("PG Owner Signature: ____________________", styles["Normal"]))

    pdf_path = tempfile.NamedTemporaryFile(delete=False,suffix=".pdf").name

    doc = SimpleDocTemplate(pdf_path,pagesize=A4)
    doc.build(elements)

    return send_file(
        pdf_path,
        as_attachment=True,
        download_name=f"{tenant['tenant_name']}_tenant_form.pdf",
        mimetype="application/pdf"
    )
# -------------------------
# RUN SERVER
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)