-- seed_random_assets.sql
--
-- Inserts demo AssetTypes, Locations, Employees and multiple random Asset rows.
-- Leaves resource_id NULL so an AFTER INSERT trigger (if present) can populate it.
-- If you don't have TRIGGER privileges / trigger not present, use the optional backfill UPDATE near the end.
--
-- Run in phpMyAdmin (SQL tab) or via mysql CLI:
-- mysql -u user -p your_database < seed_random_assets.sql

START TRANSACTION();

-- Create the asset types if they don't already exist
INSERT IGNORE INTO AssetTypes (asset_type_name)
VALUES ('laptops'), ('desktops'), ('servers'), ('printers');

-- Small set of locations (IDs are explicit because Locations.id is not AUTO_INCREMENT)
INSERT IGNORE INTO Locations (id, phone, street, country, city)
VALUES
  (1, '555-0101', '100 Main St', 'USA', 'Springfield'),
  (2, '555-0202', '200 Market St', 'USA', 'Shelbyville');

-- Small set of employees (IDs explicit)
INSERT IGNORE INTO Employee (id, first_name, last_name, title, email, country, city, location)
VALUES
  (1, 'Alice', 'Anderson', 'Engineer', 'alice@example.com', 'USA', 'Springfield', 1),
  (2, 'Bob', 'Brown', 'Technician', 'bob@example.com', 'USA', 'Shelbyville', 2);

-- Insert multiple random assets. We alternate location_id / employee_id so constraint is satisfied.
-- NOTE: resource_id is set to NULL so your trigger (if installed) can populate it. If you don't have a trigger,
-- run the backfill UPDATE near the bottom of this file after these INSERTs.

-- Laptops (3)
INSERT INTO Asset (resource_id, type_id, date_added, location_id, employee_id, notes, is_decommissioned)
VALUES
  (NULL, (SELECT id FROM AssetTypes WHERE asset_type_name='laptops'), DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*720) DAY), NULL, 1, 'Laptop - developer', 0),
  (NULL, (SELECT id FROM AssetTypes WHERE asset_type_name='laptops'), DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*720) DAY), 1, NULL, 'Laptop - shared pool', 0),
  (NULL, (SELECT id FROM AssetTypes WHERE asset_type_name='laptops'), DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*720) DAY), NULL, 2, 'Laptop - field tech', 0);

-- Desktops (3)
INSERT INTO Asset (resource_id, type_id, date_added, location_id, employee_id, notes, is_decommissioned)
VALUES
  (NULL, (SELECT id FROM AssetTypes WHERE asset_type_name='desktops'), DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*720) DAY), 1, NULL, 'Desktop - reception', 0),
  (NULL, (SELECT id FROM AssetTypes WHERE asset_type_name='desktops'), DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*720) DAY), NULL, 1, 'Desktop - engineer', 0),
  (NULL, (SELECT id FROM AssetTypes WHERE asset_type_name='desktops'), DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*720) DAY), 2, NULL, 'Desktop - lab', 0);

-- Servers (3)
INSERT INTO Asset (resource_id, type_id, date_added, location_id, employee_id, notes, is_decommissioned)
VALUES
  (NULL, (SELECT id FROM AssetTypes WHERE asset_type_name='servers'), DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*720) DAY), 1, NULL, 'Rack server A', 0),
  (NULL, (SELECT id FROM AssetTypes WHERE asset_type_name='servers'), DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*720) DAY), 1, NULL, 'Rack server B', 0),
  (NULL, (SELECT id FROM AssetTypes WHERE asset_type_name='servers'), DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*720) DAY), 2, NULL, 'Backup server', 0);

-- Printers (3)
INSERT INTO Asset (resource_id, type_id, date_added, location_id, employee_id, notes, is_decommissioned)
VALUES
  (NULL, (SELECT id FROM AssetTypes WHERE asset_type_name='printers'), DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*720) DAY), 1, NULL, 'Network Printer', 0),
  (NULL, (SELECT id FROM AssetTypes WHERE asset_type_name='printers'), DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*720) DAY), 2, NULL, 'Floor Printer', 0),
  (NULL, (SELECT id FROM AssetTypes WHERE asset_type_name='printers'), DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND()*720) DAY), NULL, 2, 'Personal printer (tech)', 0);

COMMIT();

-- BACKFILL: populate resource_id for rows inserted above (or any rows missing resource_id).
-- This avoids needing a TRIGGER and prevents the "Can't update table 'Asset' in stored function/trigger"
-- error (MySQL disallows updating the same table from a trigger in this way).

UPDATE Asset a
JOIN AssetTypes t ON a.type_id = t.id
SET a.resource_id = CONCAT(t.asset_type_name, '-', YEAR(a.date_added), '-', LPAD(a.id, 3, '0'))
WHERE a.resource_id IS NULL OR a.resource_id = '';

-- End of file
