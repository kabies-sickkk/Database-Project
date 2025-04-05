CREATE TABLE Fire_Fighting.status (
    Status_id INT AUTO_INCREMENT PRIMARY KEY,
    Sensor_id INT,
    Temperature_value FLOAT,
    Smoke_value FLOAT,
    Temperature_Warning VARCHAR(50) AS (CASE WHEN Temperature_value > 60 THEN 'Warning' ELSE 'Normal' END) STORED,
    Smoke_Warning VARCHAR(50) AS (CASE WHEN Smoke_value > 150 THEN 'Warning' ELSE 'Normal' END) STORED,
    Decision VARCHAR(50) AS (
        CASE 
            WHEN Temperature_Warning = 'Warning' AND Smoke_Warning = 'Warning' THEN 'Fire Fighting Required' 
            ELSE 'No Action Needed' 
        END
    ) STORED,
    FOREIGN KEY (Sensor_id) REFERENCES Fire_Fighting.sensors(Sensor_id)
);
