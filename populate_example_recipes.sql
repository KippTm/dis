-- Insert the example user
INSERT INTO users (username, password)
VALUES ('example', 'hashed_example_password');

INSERT INTO recipe (author, recipe_name) VALUES
('example', 'Vegetarisk Grøntsagsfad'),
('example', 'Oksekød Deluxe Burger'),
('example', 'Tunsalat med Dressing');

INSERT INTO recipe_content (recipe_name, recipe_author, food_id, amount) VALUES
('Vegetarisk Grøntsagsfad', 'example', 'Ra00001', 20),  -- Peberfrugt
('Vegetarisk Grøntsagsfad', 'example', 'Ra00002', 56),  -- Tomat
('Vegetarisk Grøntsagsfad', 'example', 'Ra00003', 200),  -- Squash
('Vegetarisk Grøntsagsfad', 'example', 'Ra00004', 250);  -- Aubergine

INSERT INTO recipe_content (recipe_name, recipe_author, food_id, amount) VALUES
('Oksekød Deluxe Burger', 'example', 'Ra00012', 250),  -- Hakket oksekød 10–15%
('Oksekød Deluxe Burger', 'example', 'Ra00028', 100),  -- Toastbrød
('Oksekød Deluxe Burger', 'example', 'Ra00067', 10), -- Thousand island dressing
('Oksekød Deluxe Burger', 'example', 'Ra00080', 40); -- Mozzarella

INSERT INTO recipe_content (recipe_name, recipe_author, food_id, amount) VALUES
('Tunsalat med Dressing', 'example', 'Ra00094', 650), -- Tun i tomat
('Tunsalat med Dressing', 'example', 'Ra00066', 50), -- Olie-eddike dressing
('Tunsalat med Dressing', 'example', 'Ra00002', 40);  -- Tomat
