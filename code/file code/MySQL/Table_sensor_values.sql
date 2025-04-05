CREATE TABLE Fire_Fighting.sensor_values (
    Value_id INT AUTO_INCREMENT PRIMARY KEY,
    Sensor_id INT,
    Temperature_value FLOAT NOT NULL,
    Smoke_value FLOAT NOT NULL,
    FOREIGN KEY (Sensor_id) REFERENCES Fire_Fighting.sensors(Sensor_id)
);
