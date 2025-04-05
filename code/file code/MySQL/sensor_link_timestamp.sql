DELIMITER //

CREATE TRIGGER Fire_Fighting.after_insert_sensors
AFTER INSERT ON Fire_Fighting.sensors
FOR EACH ROW
BEGIN
    INSERT INTO Fire_Fighting.timestamps (Date, Time, Sensor_id)
    VALUES (CURRENT_DATE, CURRENT_TIME, NEW.Sensor_id);
END //

DELIMITER ;
