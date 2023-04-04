from flask import Flask, render_template, jsonify, request, redirect
import cx_Oracle
from datetime import datetime

app = Flask(__name__)

# conexiunea la baza de date
cx_Oracle.init_oracle_client(lib_dir=r"C:\Users\Gabriela\Desktop\Airport_reservation\instantclient_21_7")
con_tns = cx_Oracle.makedsn('bd-dc.cs.tuiasi.ro', '1539', service_name='orcl')
try:
    con = cx_Oracle.connect('bd158', 'bd158', dsn=con_tns)

except Exception:
    print('Unexpected error')
else:
    print('Conexiune stabilita')


# passenger begin code
@app.route("/")
@app.route('/Passenger')
def passenger():
    passengers = []
    cur = con.cursor()
    cur.execute('select * from passenger')
    for result in cur:
        passenger = {}
        passenger['P_id'] = result[0]
        passenger['First_name'] = result[1]
        passenger['Middle_name'] = result[2]
        passenger['Last_name'] = result[3]
        passenger['Email'] = result[4]
        passenger['Phone_number'] = result[5]
        passengers.append(passenger)
    cur.close()
    return render_template('Passenger.html', passengers=passengers)


# check
@app.route('/addPassenger', methods=['GET', 'POST'])
def addPassenger():
    if request.method == 'POST':
        cur = con.cursor()
        values = []
        id = 'NULL'
        values.append(str(id))
        first = "'" + request.form['first_name'] + "'"
        middle = "'" + request.form['middle_name'] + "'"
        last = "'" + request.form['last_name'] + "'"
        email = "'" + request.form['email'] + "'"
        phone = "'" + request.form['phone_number'] + "'"
        fields = ['P_id', 'First_name', 'Middle_name', 'Last_name', 'Email', 'Phone_number']

        pass_nr = "'" + request.form['pass_nr'] + "'"

        query = 'INSERT INTO %s (%s) VALUES (%s,initcap(%s),initcap(%s),initcap(%s),%s,%s)' % (
            'Passenger', ', '.join(fields), id, first, middle, last, email, phone)
        cur.execute(query)
        cur.execute('commit')
        cur.close()

        cur = con.cursor()
        cur.execute('select max(p_id) from passenger')
        p_id = 0
        for result in cur:
            p_id = result[0]
        cur.close()
        cur = con.cursor()
        query1 = 'INSERT INTO PASSPORT values (NULL,UPPER(%s),%s)' % (pass_nr, p_id)
        cur.execute(query1)
        cur.execute('commit')

        return redirect('/Passenger')
    else:

        cur = con.cursor()
        pas = []
        cur.execute('select pass_nr from passport')
        for result in cur:
            pas.append(result[0])
        cur.close()

        cur = con.cursor()
        phone = []
        cur.execute('select phone_number from passenger')
        for result in cur:
            phone.append(result[0])
        cur.close()

        cur = con.cursor()
        email = []
        cur.execute('select email from passenger')
        for result in cur:
            email.append(result[0])
        cur.close()

        return render_template('addPassenger.html', Passport=pas, Phone=phone, Email=email)


# check
@app.route('/delPassenger', methods=['POST'])
def deletePassenger():
    cur = con.cursor()
    pas = request.form['p_id']
    cur.execute('delete from booking where p_id=' + str(pas))
    cur.execute('delete from passport where p_id=' + str(pas))
    cur.execute('delete from passenger where p_id=' + str(pas))
    cur.execute('commit')
    return redirect('/Passenger')


# check
@app.route('/editPassenger', methods=['POST'])
def editPassenger():
    p_id = "'" + request.form['p_id'] + "'"
    first = "'" + request.form['first_name'] + "'"
    middle = "'" + request.form['middle_name'] + "'"
    last = "'" + request.form['last_name'] + "'"
    email = "'" + request.form['email'] + "'"
    phone = "'" + request.form['phone_number'] + "'"
    cur = con.cursor()
    query = "UPDATE passenger SET First_name=%s,Middle_name=%s, Last_name=%s, Email=%s, Phone_number=%s where P_id=%s" % (
        first, middle, last, email, phone, p_id)

    cur.execute(query)

    cur.execute('commit')

    return redirect('/Passenger')


@app.route('/getPassenger', methods=['POST'])
def getPassenger():
    id = request.form['p_id']
    cur = con.cursor()
    cur.execute('select * from passenger where p_id=' + id)

    p = cur.fetchone()
    p_id = p[0]
    first_name = p[1]
    middle_name = p[2]
    last_name = p[3]
    email = p[4]
    phone = p[5]
    cur.close()

    cur = con.cursor()
    phone_nr = []
    cur.execute('select phone_number from passenger where phone_number!=' + phone)
    for result in cur:
        phone_nr.append(result[0])
    cur.close()

    cur = con.cursor()
    mail = []
    cur.execute('select email from passenger where p_id!=' + str(p_id))
    for result in cur:
        mail.append(result[0])
    cur.close()

    return render_template('editPassenger.html', P_id=p_id, First_name=first_name, Middle_name=middle_name,
                           Last_name=last_name,
                           Email=email, Phone_number=phone, Phone=phone_nr, Pass_email=mail)


# -------passport
# check
@app.route('/Passport')
def passport():
    passports = []
    cur = con.cursor()
    cur.execute('select * from Passport')
    for result in cur:
        pas = {}
        pas['Pass_id'] = result[0]
        pas['Pass_nr'] = result[1]
        cur1=con.cursor()
        cur1.execute('select first_name,last_name from passenger where p_id='+str(result[2]))
        for result1 in cur1:
            pas['P_id']=result1[0]+" "+result1[1]
        cur1.close()
        passports.append(pas)
    cur.close()
    return render_template('Passport.html', passports=passports)


# check
@app.route('/editPassport', methods=['POST'])
def editPassport():
    pass_id = "'" + request.form['pass_id'] + "'"
    pass_nr = "'" + request.form['pass_nr'] + "'"

    cur = con.cursor()
    query = "UPDATE passport SET Pass_nr=%s where Pass_id=%s" % (
        pass_nr, pass_id)

    cur.execute(query)

    cur.execute('commit')

    return redirect('/Passport')


# check
@app.route('/getPassport', methods=['POST'])
def getPassport():
    id = request.form['pass_id']
    cur = con.cursor()
    cur.execute('select * from passport where pass_id=' + id)

    p = cur.fetchone()
    pass_id = p[0]
    pass_nr = p[1]
    cur.close()

    cur = con.cursor()
    pas = []
    cur.execute('select pass_nr from passport where pass_id!=' + str(pass_id))
    for result in cur:
        pas.append(result[0])
    cur.close()

    return render_template('editPassport.html', Pass_nr=pass_nr, Pass_id=pass_id, Passport=pas)


# -------Airport
# check
@app.route('/Airport')
def airport():
    airports = []
    cur = con.cursor()
    cur.execute('select * from airport')
    for result in cur:
        air = {}
        air['Airport_id'] = result[0]
        air['Name'] = result[1]
        air['Country'] = result[2]
        air['City'] = result[3]
        airports.append(air)
    cur.close()
    return render_template('Airport.html', airports=airports)


# check
@app.route('/addAirport', methods=['GET', 'POST'])
def addAirport():
    if request.method == 'POST':
        cur = con.cursor()
        airport_id = 'NULL'
        name = "'" + request.form['name'] + "'"
        country = "'" + request.form['country'] + "'"
        city = "'" + request.form['city'] + "'"
        fields = ['Airport_id', 'Name', 'Country', 'City']

        query = 'INSERT INTO %s (%s) VALUES (%s,initcap(%s),initcap(%s),initcap(%s))' % (
            'Airport', ', '.join(fields), airport_id, name, country, city)
        cur.execute(query)
        cur.execute('commit')
        return redirect('/Airport')
    else:

        cur = con.cursor()
        cur.execute('select name from airport')
        name = []
        for result in cur:
            name.append(result[0])
        cur.close()

        return render_template('addAirport.html', Name=name)


# check
@app.route('/delAirport', methods=['POST'])
def deleteAirport():
    cur = con.cursor()
    id = request.form['airport_id']

    flight_id = []
    cur.execute('select flight_id from flight where airport_id=' + str(id) + 'or airport_id1=' + str(id))
    for result in cur:
        flight_id.append(result[0])
    for i in flight_id:
        cur.execute('delete from booking where flight_id=' + str(i))
    cur.execute('delete from flight where airport_id=' + str(id) + 'or airport_id1=' + str(id))
    cur.execute('delete from airport where airport_id=' + str(id))
    cur.execute('commit')
    return redirect('/Airport')


# check
@app.route('/editAirport', methods=['POST'])
def editAirport():
    airport_id = "'" + request.form['airport_id'] + "'"
    name = "'" + request.form['name'] + "'"
    country = "'" + request.form['country'] + "'"
    city = "'" + request.form['city'] + "'"

    cur = con.cursor()
    query = "UPDATE airport SET Name=%s,Country=%s, City=%s where Airport_id=%s" % (
        name, country, city, airport_id)

    cur.execute(query)

    cur.execute('commit')

    return redirect('/Airport')


# check
@app.route('/getAirport', methods=['POST'])
def getAirport():
    id = request.form['airport_id']
    cur = con.cursor()
    cur.execute('select * from airport where airport_id=' + str(id))

    p = cur.fetchone()
    airport_id = p[0]
    name = p[1]
    country = p[2]
    city = p[3]

    cur.close()

    cur = con.cursor()
    cur.execute('select name from airport where airport_id!=' + str(airport_id))
    nume = []
    for result in cur:
        nume.append(result[0])
    cur.close()

    return render_template('editAirport.html', Airport_id=airport_id, Name=name, Country=country, City=city, Nume=nume)


# -------Flight
# check
@app.route('/Flight')
def flight():
    flights = []
    cur = con.cursor()
    cur.execute('select * from flight')
    for result in cur:
        fl = {}
        fl['Flight_id'] = result[0]
        fl['Departure_date'] = datetime.strptime(str(result[1]), '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%y')
        fl['Arrival_date'] = datetime.strptime(str(result[2]), '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%y')
        fl['Capacity'] = result[3]
        fl['Available'] = result[4]
        cur1 = con.cursor()
        cur1.execute('select name from airport where airport_id=' + str(result[5]))
        for result1 in cur1:
            fl['Airport_id'] = result1[0]
        cur1.close()
        cur1 = con.cursor()
        cur1.execute('select name from airport where airport_id=' + str(result[6]))
        for result2 in cur1:
            fl['Airport_id1'] = result2[0]
        cur1.close()
        flights.append(fl)
    cur.close()
    return render_template('Flight.html', flights=flights)


# check
@app.route('/addFlight', methods=['GET', 'POST'])
def addFlight():
    if request.method == 'POST':
        cur = con.cursor()
        values = []
        flight_id = 'NULL'
        values.append(str(flight_id))
        values.append(
            "'" + datetime.strptime(str(request.form['departure_date']), '%Y-%m-%d').strftime('%d.%b.%Y') + "'")
        values.append("'" + datetime.strptime(str(request.form['arrival_date']), '%Y-%m-%d').strftime('%d.%b.%Y') + "'")

        values.append("'" + request.form['capacity'] + "'")
        available = 'NULL'
        values.append(str(available))

        dep_name = "'" + request.form['departure_airport'] + "'"
        cur.execute('select airport_id from Airport where name=' + dep_name)
        for result in cur:
            dep_id = result[0]
        values.append(str(dep_id))
        cur.close()

        cur = con.cursor()
        arr_name = "'" + request.form['arrival_airport'] + "'"
        cur.execute('select airport_id from Airport where name=' + arr_name)
        for result in cur:
            arr_id = result[0]
        values.append(str(arr_id))

        cur.close()

        cur = con.cursor()
        fields = ['Flight_id', 'Departure_date', 'Arrival_date', 'Capacity', 'Available', 'Airport_id', 'Airport_id1']

        query = 'INSERT INTO %s (%s) VALUES (%s)' % ('Flight', ', '.join(fields), ', '.join(values))
        cur.execute(query)
        cur.execute('commit')
        return redirect('/Flight')
    else:

        air = []
        cur = con.cursor()
        cur.execute('select name from airport')
        for result in cur:
            air.append(result[0])
        cur.close()

        return render_template('addFlight.html', Airport=air)


# check
@app.route('/delFlight', methods=['POST'])
def deleteFlight():
    cur = con.cursor()
    id = request.form['flight_id']
    cur.execute('delete from booking where flight_id=' + str(id))
    cur.execute('delete from flight where flight_id=' + str(id))
    cur.execute('commit')
    return redirect('/Flight')


# check
@app.route('/editFlight', methods=['POST'])
def editFlight():
    cur = con.cursor()

    flight_id = "'" + request.form['flight_id'] + "'"
    departure_date = "'" + datetime.strptime(str(request.form['departure_date']), '%Y-%m-%d').strftime('%d.%b.%Y') + "'"
    arrival_date = "'" + datetime.strptime(str(request.form['arrival_date']), '%Y-%m-%d').strftime('%d.%b.%Y') + "'"
    capacity = request.form['capacity']
    old_capacity = request.form['old_capacity']
    available = request.form['available']
    departure_airport = "'" + request.form['departure_airport'] + "'"
    arrival_airport = "'" + request.form['arrival_airport'] + "'"

    new_available = int(available) - (int(old_capacity) - int(capacity))

    cur1 = con.cursor()
    departure_id = 0
    cur1.execute('select airport_id from airport where name=' + departure_airport)
    for result in cur1:
        departure_id = result[0]
    cur1.close()

    cur1 = con.cursor()
    arrival_id = 0
    cur1.execute('select airport_id from airport where name=' + arrival_airport)
    for result in cur1:
        arrival_id = result[0]
    cur1.close()
    try:
        query = "UPDATE flight SET Departure_date=%s,Arrival_date=%s, Capacity=%s,Available=%s,Airport_id=%s,Airport_id1=%s where Flight_id=%s" % (
            departure_date, arrival_date, str(capacity), str(new_available), str(departure_id), str(arrival_id), flight_id)

        cur.execute(query)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str("Nu se poate actualiza")}), 500

    cur.execute('commit')

    return redirect('/Flight')


# check
@app.route('/getFlight', methods=['POST'])
def getFlight():
    id = request.form['flight_id']
    cur = con.cursor()
    cur.execute('select * from flight where flight_id=' + str(id))

    p = cur.fetchone()
    flight_id = p[0]
    departure_date = datetime.strptime(str(p[1]), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
    arrival_date = datetime.strptime(str(p[2]), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
    capacity = p[3]
    available = p[4]
    cur1 = con.cursor()
    cur1.execute('select name from airport where airport_id=' + str(p[5]))
    for result in cur1:
        departure_airport = result[0]
    cur1.close()

    cur1 = con.cursor()
    cur1.execute('select name from airport where airport_id=' + str(p[6]))
    for result in cur1:
        arrival_airport = result[0]
    cur1.close()

    cur1 = con.cursor()
    air = []
    cur1.execute('select name from airport')
    for result in cur1:
        air.append(result[0])
    cur1.close()

    cur.close()

    return render_template('editFlight.html', Flight_id=flight_id, Available=available, Departure_date=departure_date,
                           Arrival_date=arrival_date, Capacity=capacity, Departure_airport=departure_airport,
                           Arrival_airport=arrival_airport, Airport=air)


# -------Booking
# check
@app.route('/Booking')
def booking():
    bookings = []
    cur = con.cursor()
    cur.execute('select * from booking')
    for result in cur:
        booking = {}
        booking['Ticket_id'] = result[0]
        booking['Seat_nr'] = result[1]

        cur1 = con.cursor()
        cur1.execute('select first_name,last_name from passenger where P_id=' + str(result[2]))
        for result1 in cur1:
            booking['P_id'] = result1[0] + " " + result1[1]
        cur1.close()
        cur1 = con.cursor()
        cur1.execute('select d.name,a.name from flight f,airport d,airport a where flight_id=' + str(
            result[3]) + 'and f.airport_id=d.airport_id and f.airport_id1=a.airport_id')
        for result1 in cur1:
            booking['Flight_id'] = result1[0] + "-" + result1[1]
        bookings.append(booking)
    cur.close()
    return render_template('Booking.html', bookings=bookings)


# modificare rute
@app.route('/addBooking', methods=['GET', 'POST'])
def addBooking():
    if request.method == 'POST':
        values = []
        ticket_id = 'NULL'
        values.append(str(ticket_id))
        seat="'" + request.form['seat_nr'] + "'"
        values.append(str(seat))

        cur = con.cursor()
        p_phone = "'" + request.form['phone'] + "'"
        cur.execute('select p_id from Passenger where phone_number=' + p_phone)
        for result in cur:
            p_id = result[0]
        values.append(str(p_id))
        cur.close()

        cur = con.cursor()
        flight_dep = "'" + request.form['flight_dep'] + "'"
        flight_arr = "'" + request.form['flight_arr'] + "'"
        cur.execute(
            'select flight_id from Flight where airport_id=(select airport_id from Airport where name=' + flight_dep + ') and airport_id1=(select airport_id from Airport where name=' + flight_arr + ')')
        for result in cur:
            flight_id = result[0]
        values.append(str(flight_id))
        cur.close()

        '''cur=con.cursor()
        cur.execute('select departure_date,arrival_date from flight where flight_id='+str(flight_id))
        for result in cur:
            dep_date=result[0]
            arr_date=result[1]

        print(dep_date)
        print(arr_date)
        cur.close()



        cur=con.cursor();
        cur.execute(f"select count(*) from booking b,passenger p,flight f where \
                    b.p_id=p.p_id and f.flight_id=b.flight_id and p.p_id=(select \
                    p_id from passenger where phone_number='{p_phone}') and \
                    b.flight_id in (select g.flight_id from flight g \
                    where ( (to_date('{dep_date}','yyyy-mm-dd') between f.departure_date and f.arrival_date )\
                    or (to_date('{arr_date}','yyyy-mm-dd') between f.departure_date and f.arrival_date)\
                    or (f.departure_date between to_date('{dep_date}','yyyy-mm-dd') and to_date('{arr_date}','yyyy-mm-dd'))\
                    or (f.arrival_date between to_date('{dep_date}','yyyy-mm-dd') and to_date('{arr_date}','yyyy-mm-dd'))))")

        for result in cur:
            valid=result[0]
        cur.close()
        print(valid)
'''
        cur = con.cursor()
        fields = ['Ticket_id', 'Seat_nr', 'P_id', 'Flight_id']
        try:
            query = 'INSERT INTO %s (%s) VALUES (%s)' % ('Booking', ', '.join(fields), ', '.join(values))
            cur.execute(query)
        except Exception as e:
            return jsonify({'status': 'error', 'message': str("Nu mai sunt locuri disponibile")}), 500
        cur.execute('commit')
        return redirect('/Booking')
    else:

        air = []
        air1 = []
        cur = con.cursor()
        cur.execute('select d.name from airport d,flight f where d.airport_id=f.airport_id order by f.flight_id')
        for result in cur:
            air.append(result[0])
        cur.close()

        cur = con.cursor()
        cur.execute('select a.name from airport a,flight f where a.airport_id=f.airport_id1 order by f.flight_id')
        for result in cur:
            air1.append(result[0])
        cur.close()

        return render_template('addBooking.html', Airport_dep=air, Airport_arr=air1)


# check
@app.route('/delBooking', methods=['POST'])
def deleteBooking():
    cur = con.cursor()
    ticket = "'" + request.form['ticket_id'] + "'"

    cur.execute('delete from booking where ticket_id=' + ticket)
    cur.execute('commit')
    return redirect('/Booking')


@app.route('/editBooking', methods=['POST'])
def editBooking():
    cur = con.cursor()
    old_flight_id = request.form['old_flight_id']
    id = "'" + request.form['ticket_id'] + "'"
    old_seat = request.form['old_seat']
    seat = request.form['seat']
    phone = "'" + request.form['p_id'] + "'"
    cur1 = con.cursor()
    cur1.execute('select p_id from passenger where phone_number=' + phone)
    for result in cur1:
        p_id = result[0]
    cur1.close()

    flight_d = "'" + request.form['flight_dep'] + "'"
    flight_a = "'" + request.form['flight_arr'] + "'"

    cur1 = con.cursor()
    cur1.execute(
        'select flight_id from flight where airport_id=(select airport_id from airport where name=' + flight_d + ')and airport_id1=(select airport_id from airport where name=' + flight_a + ')')
    for result in cur1:
        flight_id = result[0]
    cur1.close()

    if int(flight_id) == int(old_flight_id):
        cur1 = con.cursor()
        cur1.execute('select available from flight where flight_id=' + str(flight_id))
        for result in cur1:
            av = result[0]
        cur1.close()

        new_av = (int(av) + int(old_seat)) - int(seat)

        cur1 = con.cursor()
        try:
            cur1.execute('update flight set available=' + str(new_av) + 'where flight_id=' + str(flight_id))
            #cur1.execute('commit')
        except Exception as e:
            return jsonify({'status': 'error', 'message': str("Nu mai sunt locuri disponibile")}), 500
        cur1.close()
    else:
        cur1 = con.cursor()
        cur1.execute('select available from flight where flight_id=' + str(old_flight_id))
        for result in cur1:
            old_av = result[0]
        cur1.close()

        new_available_old_flight = int(old_av) + int(old_seat)

        cur1 = con.cursor()
        cur1.execute('select available from flight where flight_id=' + str(flight_id))
        for result in cur1:
            av = result[0]
        cur1.close()

        new_av = int(av) - int(seat)
        try:
            cur1 = con.cursor()
            cur1.execute('update flight set available=' + str(new_av) + 'where flight_id=' + str(flight_id))
            # cur1.execute('commit')
            cur1.close()

            cur1 = con.cursor()
            cur1.execute(
                'update flight set available=' + str(new_available_old_flight) + 'where flight_id=' + str(old_flight_id))
            #cur1.execute('commit')
            cur1.close()
        except Exception as e:
            return jsonify({'status': 'error', 'message': str("Nu mai sunt locuri disponibile")}), 500


    #cur1 = con.cursor()
    #cur1.execute('update flight set available=' + str(new_av) + 'where flight_id=' + str(flight_id))
    #cur1.execute('commit')
    #cur1.close()

    query = "UPDATE booking SET Seat_nr=%s,P_id=%s,Flight_id=%s where Ticket_id=%s" % (
        str(seat), str(p_id), str(flight_id), id)
    cur.execute(query)
    cur.execute('commit')

    return redirect('/Booking')


# check
@app.route('/getBooking', methods=['POST'])
def getBooking():
    id = request.form['ticket_id']
    cur = con.cursor()
    cur.execute('select * from booking where ticket_id=' + str(id))

    p = cur.fetchone()
    ticket_id = p[0]
    seat = p[1]
    cur1 = con.cursor()
    cur1.execute('select phone_number from passenger where p_id=' + str(p[2]))
    for result in cur1:
        pas = result[0]

    flight_id = p[3]
    cur1.close()
    cur1 = con.cursor()
    cur1.execute('select d.name,a.name from airport d,airport a,flight f where flight_id=' + str(
        p[3]) + 'and d.airport_id=f.airport_id and a.airport_id=f.airport_id1')
    for result in cur1:
        fli_d = result[0]
        fli_a = result[1]
    cur1.close()

    cur1 = con.cursor()
    phone = []
    cur1.execute('select phone_number from passenger')
    for result in cur1:
        phone.append(result[0])
    cur1.close()

    air = []
    air1 = []
    cur1 = con.cursor()
    cur1.execute('select d.name from airport d,flight f where d.airport_id=f.airport_id order by f.flight_id')
    for result in cur1:
        air.append(result[0])
    cur1.close()

    cur1 = con.cursor()
    cur1.execute('select a.name from airport a,flight f where a.airport_id=f.airport_id1 order by f.flight_id')
    for result in cur1:
        air1.append(result[0])
    cur1.close()

    cur1 = con.cursor()
    cur1.execute('select available from flight where flight_id=' + str(flight_id))
    for result in cur1:
        available = result[0]
    cur1.close()

    cur.close()

    return render_template('editBooking.html', Ticket_id=ticket_id, Seat_nr=seat, P_id=pas, Fli_a=fli_a,
                           Fli_d=fli_d, Phone=phone, Airport=air, Airport1=air1, Flight_id=flight_id,
                           Available=available)


if __name__ == "__main__":
    app.run(debug=True)
    con.close()
