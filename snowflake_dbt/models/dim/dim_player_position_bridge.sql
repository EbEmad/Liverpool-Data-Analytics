WITH flattened_pos AS (
    SELECT 
        dp.player_id,
        TRIM(position.value::STRING) AS position
    FROM 
        {{ ref('dim_players') }} AS dp
    JOIN 
        {{ source('Bronze_data', 'stg_standard_stats') }} AS raw
        ON dp.player_name = raw.player
    , 
        LATERAL FLATTEN(input => SPLIT(raw.position, ',')) AS position
)

SELECT 
    fp.player_id,
    dp.position_id,
    CURRENT_TIMESTAMP AS loaded_at
FROM 
    flattened_pos AS fp
JOIN 
    {{ ref('dim_positions') }} AS dp
ON 
    fp.position = dp.position