SELECT 
    s.Sensor_id,
    s.Temperature_sensor,
    s.Smoke_sensor,
    t.Time_id,
    t.Date,
    t.Time,
    st.Status_id,
    st.Temperature_value,
    st.Smoke_value,
    st.Temperature_Warning,
    st.Smoke_Warning,
    st.Decision
FROM 
    Fire_Fighting.sensors AS s
JOIN 
    Fire_Fighting.timestamps AS t ON s.Sensor_id = t.Sensor_id
JOIN 
    Fire_Fighting.status AS st ON s.Sensor_id = st.Sensor_id;
