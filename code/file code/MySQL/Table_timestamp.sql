CREATE TABLE Fire_Fighting.timestamps (
    Time_id INT AUTO_INCREMENT PRIMARY KEY,
    Date DATE NOT NULL,
    Time TIME NOT NULL,
    Sensor_id INT,
    FOREIGN KEY (Sensor_id) REFERENCES Fire_Fighting.sensors(Sensor_id)
);