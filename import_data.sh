#!/bin/bash

# Drop the database if it exists (optional, for a clean start)
# dropdb --if-exists recipe_site

# Create the database
createdb recipe_site

# Apply schema
psql -d recipe_site -f db_schema.sql

# Import food data from CSV
psql -d recipe_site -c "\copy food FROM '$(pwd)/new_db.csv' DELIMITER ';' CSV HEADER"

# Populate example recipes
psql -d recipe_site -f populate_example_recipes.sql

echo "Database setup complete."
