-- 
create database FeuerwehrNotifications CHARACTER SET utf8 COLLATE utf8_general_ci;
use FeuerwehrNotifications;
create table Alarmdepesche ( id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT
                           , dbIN TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                           , messageID BIGINT UNSIGNED
                           , Einsatzstichwort VARCHAR(512)
                           , AlarmiertesEinsatzmittel VARCHAR(512)
                           , Sondersignal VARCHAR(512)
                           , Einsatzbeginn VARCHAR(512)
                           , Einsatznummer VARCHAR(512)
                           , Auftragsnummer VARCHAR(512)
                           , Name VARCHAR(512)
                           , Zusatz VARCHAR(512)
 			               , Sachverhalt VARCHAR(512)
                           , Patientenname VARCHAR(512)
                           , Target_Objekt VARCHAR(512)
                           , Target_Objekttyp VARCHAR(512)
                           , Target_StrasseHausnummer VARCHAR(512)
                           , Target_Segment VARCHAR(512)
                           , Target_PLZOrt VARCHAR(512)
                           , Target_Region VARCHAR(512)
                           , Target_Info VARCHAR(512)
                           , Target_GeoLat VARCHAR(256)
                           , Target_GeoLong VARCHAR(256)
                           , TransTarget_Transportziel VARCHAR(512)
                           , TransTarget_Objekt VARCHAR(512)
                           , TransTarget_Objekttyp VARCHAR(512)
                           , TransTarget_StrasseHausnummer VARCHAR(512)
                           , TransTarget_PLZOrt VARCHAR(512)
                           , TransTarget_Segment VARCHAR(512)
                           , TransTarget_Region VARCHAR(512)
                           , TransTarget_Info VARCHAR(512)
                           , TransTarget_GeoLat VARCHAR(256)
                           , TransTarget_GeoLong VARCHAR(256)
                           , PRIMARY KEY (id));

-- 
