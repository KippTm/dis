psql -d recipe_site -c "\copy food FROM '$(pwd)/new_db.csv' DELIMITER ';' CSV HEADER"
