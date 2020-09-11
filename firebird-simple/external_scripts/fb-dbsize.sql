CONNECT /var/lib/firebird/2.5/data/database.fdb USER 'SYSDBA' PASSWORD 'XXX';
select mon$pages * mon$page_size from MON$DATABASE;
quit;
