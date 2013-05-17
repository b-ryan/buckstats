CREATE TABLE events (
  id SERIAL PRIMARY KEY,
  event VARCHAR(50),
  start_time TIMESTAMP,
  end_time TIMESTAMP
);
