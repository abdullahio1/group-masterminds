-- Ai generated dummy data
BEGIN;

-- Insert 20 Consultants
INSERT INTO consultants (name, email) VALUES
('Elena Rostova', 'elena.rostova@consulting.com'),
('Marcus Vance', 'marcus.vance@consulting.com'),
('Aisha Patel', 'aisha.patel@consulting.com'),
('Liam O''Connor', 'liam.oconnor@consulting.com'),
('Sofia Silva', 'sofia.silva@consulting.com'),
('Kai Tanaka', 'kai.tanaka@consulting.com'),
('Chloe Dubois', 'chloe.dubois@consulting.com'),
('Devon Miller', 'devon.miller@consulting.com'),
('Amara Okafor', 'amara.okafor@consulting.com'),
('Lucas Schmidt', 'lucas.schmidt@consulting.com'),
('Hannah Abbott', 'hannah.abbott@consulting.com'),
('Noah Kim', 'noah.kim@consulting.com'),
('Isabella Santos', 'isabella.santos@consulting.com'),
('Tariq Al-Mansoor', 'tariq.almansoor@consulting.com'),
('Freja Lindqvist', 'freja.lindqvist@consulting.com'),
('Mateo Hernandez', 'mateo.hernandez@consulting.com'),
('Yuki Sato', 'yuki.sato@consulting.com'),
('Zoe Chen', 'zoe.chen@consulting.com'),
('Oliver Smith', 'oliver.smith@consulting.com'),
('Nadia Becker', 'nadia.becker@consulting.com');

-- Insert 10 Customers
INSERT INTO customers (name) VALUES
('Acme Corporation'),
('Apex Global Solutions'),
('Nexus Dynamics'),
('Starlight Media'),
('Vanguard Tech'),
('Horizon Financial'),
('Quantum Labs'),
('Echo Enterprises'),
('Summit Healthcare'),
('Pulse Retail Group');

-- Insert 100 Non-Overlapping Time Entries
-- Generates 5 realistic sequential entries per consultant across 5 different workdays
INSERT INTO time_entries (consultant_id, customer_id, start_time, end_time, lunch_break)
SELECT 
    c.id AS consultant_id,
    ((c.id + d.day_offset) % 10) + 1 AS customer_id,
    -- Workday starts at 08:00 AM UTC
    (CURRENT_DATE - (d.day_offset || ' days')::INTERVAL + INTERVAL '8 hours') AS start_time,
    -- Workday ends at 05:00 PM UTC (9-hour shift)
    (CURRENT_DATE - (d.day_offset || ' days')::INTERVAL + INTERVAL '17 hours') AS end_time,
    -- 0-60-minute lunch break
    FLOOR(RANDOM() * 61)::INT AS lunch_break
FROM consultants c
CROSS JOIN (
    SELECT generate_series(1, 5) AS day_offset
) d;

COMMIT;
