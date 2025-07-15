WITH positions_raw AS (
    SELECT 
        TRIM(position.value::STRING) AS position
    FROM 
        {{ source('Bronze_data', 'stg_standard_stats') }},
        LATERAL FLATTEN(input => SPLIT(position, ',')) AS position
),

positions AS (
    SELECT DISTINCT position FROM positions_raw
)

SELECT 
    ROW_NUMBER() OVER (ORDER BY position) AS position_id
    ,position
    ,CURRENT_TIMESTAMP AS loaded_at
FROM 
    positions