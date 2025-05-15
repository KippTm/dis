e
-- preamble
DROP TABLE IF EXISTS Users CASCADE;
DROP TABLE IF EXISTS Recipe CASCADE;
DROP TABLE IF EXISTS Food CASCADE;
DROP TABLE IF EXISTS Recipe_Content CASCADE;

-- entities 

CREATE TABLE Users 
(	u_name VARCHAR(50),
	PASSWORD VARCHAR(100),
	PRIMARY KEY (u_name));

CREATE TABLE Recipe 
(	
	author VARCHAR(50),
	recipe_name VARCHAR(50),
	PRIMARY KEY (author, recipe_name),
	FOREIGN KEY (author) REFERENCES Users(u_name));

CREATE TABLE Food
(
	food_id VARCHAR(20),
	name	VARCHAR(100),
	category	VARCHAR(100),
	emission	NUMERIC,
	PRIMARY KEY (food_id)
);

-- relationships

CREATE TABLE Recipe_Content
(
	recipe_name VARCHAR(50),
	recipe_author	VARCHAR(50),
	food_id		VARCHAR(20),
	PRIMARY KEY (recipe_name, recipe_author, food_id),
	FOREIGN KEY (recipe_author, recipe_name) REFERENCES Recipe(author, recipe_name),
	FOREIGN KEY (food_id) REFERENCES Food(food_id));
