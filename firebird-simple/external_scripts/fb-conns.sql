CONNECT /var/lib/firebird/2.5/data/database.fdb USER 'SYSDBA' PASSWORD 'XXX';
select count(*)   from MON$ATTACHMENTS
where MON$ATTACHMENT_ID <> CURRENT_CONNECTION;
quit;
