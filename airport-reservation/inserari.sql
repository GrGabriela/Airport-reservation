-------inserare in bazele de date-----------


-------inserari in tabela Airport-----------

insert into Airport values (NULL,'Baneasa','Romania','Bucuresti');
insert into Airport values(NULL,'Frankfurt','Germania','Frankfurt');
insert into Airport values(NULL,'Ataturk','Turcia','Istanbul');
insert into Airport values(NULL,'Barajas','Spania','Madrid');
insert into Airport values(NULL,'Fiumicino','Italia','Roma');
insert into Airport values(NULL,'Otopeni','Romania','Bucuresti');
insert into Airport values(NULL,'Denver','SUA','Colorado');
select * from Airport;

--------inserari in tabela Passenger-------

insert into Passenger values(NULL,'Diana','Maria','Popescu','anamaria2@gmail.com','0745964155');
insert into Passenger values(NULL,'Paula',NULL,'Stanescu','paulaa21@gmail.com','0756925145');
insert into Passenger values(NULL,'Mihai','Andrei','Dobre','dobremi@gmail.com','0786951489');
insert into Passenger values(NULL,'Maria',NULL,'Popovici','pmaria1@gmail.com','0763956478');
insert into Passenger values(NULL,'Leon',NULL,'Alvarez',NULL,'0765937168');
insert into Passenger values(NULL,'Ada',NULL,'Freud','adafreud20@gmail.com','0783164927');
insert into Passenger values(NULL,'Giuliana',NULL,'Ajello',NULL,'0725498762');
insert into Passenger values(NULL,'Lorenzzo','Carlo','Amato','lorenzzo_carlo@gmail.com','0731654877');
insert into Passenger values(NULL,'Luke',NULL,'Smith','luke1@gmail.com','0726498135');
insert into Passenger values(NULL,'Ethan','Maria','Jones',NULL,'0736491226');
select * from Passenger;

------------inserari in tabela Passport------------

insert into Passport values(NULL,'C03005988',28);
insert into Passport values(NULL,'431276122',29);
insert into Passport values(NULL,'340007237',30);
insert into Passport values(NULL,'791234567',31);
insert into Passport values(NULL,'GA3029221',32);
insert into Passport values(NULL,'A11163131',33);
insert into Passport values(NULL,'PA4500513',34);
insert into Passport values(NULL,'PCU000541',35);
insert into Passport values(NULL,'208889457',36);
insert into Passport values(NULL,'100003106',37);
select * from Passport;

----SCHIMBARE FORMAT DATA pentru a putea afisa si ora-----------

select * from nls_session_parameters where parameter='NLS_DATE_FORMAT';
alter session set nls_date_format = 'DD/MON/YYYY HH24:MI';

------------inserari in tabela Flight------


insert into Flight values(NULL,to_date('25-11-2022 11:00','DD-MM-YYYY HH24:MI'),to_date('26-11-2022 10:00','DD-MM-YYYY HH24:MI'),15,NULL,15,20);
insert into Flight values(NULL,to_date('05-12-2022 12:00','DD-MM-YYYY HH24:MI'),to_date('07-12-2022 11:00','DD-MM-YYYY HH24:MI'),10,NULL,16,19);
insert into Flight values(NULL,to_date('07-12-2022 14:00','DD-MM-YYYY HH24:MI'),to_date('08-12-2022 06:00','DD-MM-YYYY HH24:MI'),13,NULL,20,21);
insert into Flight values(NULL,to_date('10-12-2022 15:00','DD-MM-YYYY HH24:MI'),to_date('12-12-2022 12:00','DD-MM-YYYY HH24:MI'),16,NULL,18,15);
insert into Flight values(NULL,to_date('15-12-2022 12:00','DD-MM-YYYY HH24:MI'),to_date('16-12-2022 10:00','DD-MM-YYYY HH24:MI'),17,NULL,17,16);
insert into Flight values(NULL,to_date('17-12-2022 17:00','DD-MM-YYYY HH24:MI'),to_date('19-12-2022 13:00','DD-MM-YYYY HH24:MI'),16,NULL,16,21);
select * from Flight;

---pentru a face update in tabela Flight in campul available
----trebuie sa avem grija si de campul available care trebuie sa se actualizeze
----in acelasi timp pentru a nu crea erori in sistemul de rezervare
---vom pune intr-o variabila vechea valoare a capacitatii pentru a o folosi la 
----actualizarea locurilor disponibile


---actualizam capacitate pentru zborul care are flight_id=25

variable old_capacitate number;
exec select Capacity into :old_capacitate from Flight where flight_id=25;
print old_capacitate;

---marim cu 5 locuri
update Flight set capacity=18 where Flight_id=25;
update Flight set Available=Available-(:old_capacitate-capacity) where flight_id=25;

----scadem aceeasi capacitate cu 8 

variable old_capacitate number;
exec select Capacity into :old_capacitate from Flight where flight_id=25;
print old_capacitate;
update Flight set capacity=16 where Flight_id=25;
update Flight set Available=Available-(:old_capacitate-capacity) where flight_id=25;

select * from Flight;

---------inserari in tabela Booking-----------
-----se poate observa ca atunci cand se insereaza,va scadea nr de locuri disponibile
-----pentru acel zbor,iar cand se sterge o inregistrare/se anuleaza rezervarea
-----se va aduna acel nr de locuri la locurile disponibile

insert into Booking values(NULL,3,5,29);
insert into Booking values(NULL,4,6,30);
INSERT INTO Booking values(NULL,5,7,31);
insert into Booking values(NULL,2,5,33);
insert into Booking values(NULL,5,6,28);
insert into Booking values(NULL,7,7,35);

select * from booking;
select * from flight;

delete from Booking where Ticket_id=16;
delete from Booking where Ticket_id=17;



