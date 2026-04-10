-- Missing values
SELECT * FROM corporate_actions
WHERE value IS NULL;
 
-- Mismatch values
SELECT * FROM corporate_actions
WHERE value != expected_value;
 
-- Invalid values (zero or negative)
SELECT * FROM corporate_actions
WHERE value <= 0;