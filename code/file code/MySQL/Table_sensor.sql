CREATE SCHEMA `Fire_Fighting`;

CREATE TABLE Fire_Fighting.sensors (
    Sensor_id INT AUTO_INCREMENT PRIMARY KEY,
    Temperature_sensor VARCHAR(50) NOT NULL,
    Smoke_sensor VARCHAR(50) NOT NULL
);
