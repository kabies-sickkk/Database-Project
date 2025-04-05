DELIMITER //

CREATE TRIGGER Fire_Fighting.after_insert_sensor_values
AFTER INSERT ON Fire_Fighting.sensor_values
FOR EACH ROW
BEGIN
    INSERT INTO Fire_Fighting.status (Sensor_id, Temperature_value, Smoke_value)
    VALUES (NEW.Sensor_id, NEW.Temperature_value, NEW.Smoke_value);
END //

DELIMITER ;
