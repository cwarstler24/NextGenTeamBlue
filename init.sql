create table Locations (
	id INT Primary Key,
	phone VARCHAR(50),
	street VARCHAR(250),
	country VARCHAR(50),
	city VARCHAR(50)
);

create table Employee (
	id INT Primary Key,
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	title VARCHAR(11),
	email VARCHAR(50),
	country VARCHAR(50),
	city VARCHAR(50),
	location INT,
    FOREIGN KEY (location) REFERENCES Locations(id)
);

CREATE TABLE AssetTypes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    asset_type_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE Asset (
    id INT AUTO_INCREMENT PRIMARY KEY,
    resource_id VARCHAR(100),
    type_id INT NOT NULL,
    date_added DATE NOT NULL DEFAULT (CURDATE()),
    location_id INT,
    employee_id INT,
    notes VARCHAR(1000),
    is_decommissioned binary DEFAULT 0,
    UNIQUE INDEX uq_resource_id (resource_id),
    FOREIGN KEY (type_id) REFERENCES AssetTypes(id),
    FOREIGN KEY (location_id) REFERENCES Locations(id),
    FOREIGN KEY (employee_id) REFERENCES Employee(id),
    CONSTRAINT chk_location_or_employee CHECK (
        (location_id IS NOT NULL AND employee_id IS NULL) OR
        (location_id IS NULL AND employee_id IS NOT NULL)
    )
);

CREATE TRIGGER after_insert_assets
AFTER INSERT ON Asset
FOR EACH ROW
BEGIN
    DECLARE v_type_name VARCHAR(50);
    SELECT asset_type_name into v_type_name
    FROM AssetTypes
    WHERE id = NEW.type_id;

    UPDATE Asset
    SET resource_id = CONCAT(
                      v_type_name, '-', YEAR(NEW.date_added), '-', LPAD(NEW.id, 3, '0')
                      )
    WHERE id = NEW.id;
end;
