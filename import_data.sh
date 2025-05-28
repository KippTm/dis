#!/bin/bash
psql -d recipe_site -c "\copy food FROM '$(pwd)/new_db.csv' DELIMITER ';' CSV HEADER"
psql -d recipe_site -f populate_example_recipes.sql

