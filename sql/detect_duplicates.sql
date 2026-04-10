-- Detect duplicate event IDs
 
SELECT
    event_id,
    COUNT(*) as count
FROM corporate_actions
GROUP BY event_id
HAVING COUNT(*) > 1;