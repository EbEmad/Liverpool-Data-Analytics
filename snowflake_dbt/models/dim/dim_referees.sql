SELECT 
    ROW_NUMBER() OVER (ORDER BY match_referee) AS referee_id,
    match_referee AS referee_name,
    CURRENT_TIMESTAMP AS loaded_at
FROM 
    {{ source('Bronze_data', 'stg_scores_fixtures') }}
WHERE 
    match_referee IS NOT NULL
GROUP BY 
    match_referee