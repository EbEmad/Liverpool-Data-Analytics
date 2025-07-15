SELECT
    md5(COALESCE(CAST(p.player_id AS STRING), '')) AS fact_player_id

    
    -- Dim references
    ,p.player_id

    -- 
    ,AERIAL_DUELS_LOST
    ,AERIAL_DUELS_WON
    ,AERIAL_DUELS_WONX
    ,BLOCKS_BLOCKS
    ,BLOCKS_PASS
    ,BLOCKS_SH
    ,CARRIES_1_3
    ,CARRIES_CARRIES
    ,CARRIES_CPA
    ,CARRIES_DIS
    ,CARRIES_MIS
    ,CHALLENGES_ATT
    ,CHALLENGES_LOST
    ,CHALLENGES_TKL
    ,CHALLENGES_TKLX
    ,CORNER_KICKS_IN
    ,CORNER_KICKS_OUT
    ,CORNER_KICKS_STR
    ,EXPECTED_NPXG_SH
    ,EXPECTED_NP_G_XG
    ,EXPECTED_XA
    ,EXPECTED_XAG
    ,ss.EXPECTED_XG
    ,GCA_GCA
    ,GCA_GCA90
    ,GCA_TYPES_DEF
    ,GCA_TYPES_FLD
    ,GCA_TYPES_PASSDEAD
    ,GCA_TYPES_PASSLIVE
    ,GCA_TYPES_SH
    ,GCA_TYPES_TO
    ,INT
    ,KP
    ,LONG_ATT
    ,LONG_CMP
    ,LONG_CMPX
    ,MEDIUM_ATT
    ,MEDIUM_CMP
    ,MEDIUM_CMPX
    ,OUTCOMES_BLOCKS
    ,OUTCOMES_CMP
    ,OUTCOMES_OFF
    ,PASS_TYPES_CK
    ,PASS_TYPES_CRS
    ,PASS_TYPES_DEAD
    ,PASS_TYPES_FK
    ,PASS_TYPES_LIVE
    ,PASS_TYPES_SW
    ,PASS_TYPES_TB
    ,PASS_TYPES_TI
    ,PERFORMANCE_2CRDY
    ,PERFORMANCE_AST
    ,ss.PERFORMANCE_CRDR
    ,ss.PERFORMANCE_CRDY
    ,PERFORMANCE_CRS
    ,PERFORMANCE_FLD
    ,PERFORMANCE_FLS
    ,PERFORMANCE_GLS
    ,PERFORMANCE_GXA
    ,PERFORMANCE_G_PK
    ,PERFORMANCE_INT
    ,PERFORMANCE_OFF
    ,PERFORMANCE_OG
    ,PERFORMANCE_PK
    ,PERFORMANCE_PKATT
    ,PERFORMANCE_PKCON
    ,PERFORMANCE_PKWON
    ,PERFORMANCE_RECOV
    ,PERFORMANCE_TKLW
    ,PER_90_MINUTES_AST
    ,PER_90_MINUTES_GLS
    ,PER_90_MINUTES_GXA
    ,PER_90_MINUTES_GXA_PK
    ,PER_90_MINUTES_G_PK
    ,PER_90_MINUTES_NPXG
    ,PER_90_MINUTES_NPXGXXAG
    ,PER_90_MINUTES_XAG
    ,PER_90_MINUTES_XG
    ,PER_90_MINUTES_XGXXAG
    ,ss.PLAYING_TIME_90S
    ,ss.PLAYING_TIME_MIN
    ,PLAYING_TIME_MINX
    ,PLAYING_TIME_MN_MP
    ,ss.PLAYING_TIME_MP
    ,PLAYING_TIME_STARTS
    ,PPA
    ,PRGP
    ,PROGRESSION_PRGC
    ,PROGRESSION_PRGP
    ,PROGRESSION_PRGR
    ,RECEIVING_PRGR
    ,RECEIVING_REC
    ,SCA_SCA
    ,SCA_SCA90
    ,SCA_TYPES_DEF
    ,SCA_TYPES_FLD
    ,SCA_TYPES_PASSDEAD
    ,SCA_TYPES_PASSLIVE
    ,SCA_TYPES_SH
    ,SCA_TYPES_TO
    ,SHORT_ATT
    ,SHORT_CMP
    ,SHORT_CMPX
    ,STANDARD_DIST
    ,STANDARD_FK
    ,STANDARD_GLS
    ,STANDARD_G_SH
    ,STANDARD_G_SOT
    ,STANDARD_PK
    ,STANDARD_PKATT
    ,STANDARD_SH
    ,STANDARD_SH_90
    ,STANDARD_SOT
    ,STANDARD_SOTX
    ,STANDARD_SOT_90
    ,STARTS_COMPL
    ,STARTS_MN_START
    ,STARTS_STARTS
    ,SUBS_MN_SUB
    ,SUBS_SUBS
    ,SUBS_UNSUB
    ,TACKLES_ATT_3RD
    ,TACKLES_DEF_3RD
    ,TACKLES_MID_3RD
    ,TACKLES_TKL
    ,TACKLES_TKLW
    ,TAKE_ONS_ATT
    ,TAKE_ONS_SUCC
    ,TAKE_ONS_SUCCX
    ,TAKE_ONS_TKLD
    ,TAKE_ONS_TKLDX
    ,TEAM_SUCCESS_ONG
    ,TEAM_SUCCESS_ONGA
    ,TEAM_SUCCESS_ON_OFF
    ,TEAM_SUCCESS_PPM
    ,TEAM_SUCCESS_XG_ONXG
    ,TEAM_SUCCESS_XG_ONXGA
    ,TEAM_SUCCESS_XG_ON_OFF
    ,TEAM_SUCCESS_XG_XGXXX
    ,TEAM_SUCCESS_XG_XGX_90
    ,TEAM_SUCCESS_XXX
    ,TEAM_SUCCESS_X_90
    ,TKLXINT
    ,TOTAL_ATT
    ,TOTAL_CMP
    ,TOTAL_CMPX
    ,TOTAL_PRGDIST
    ,TOTAL_TOTDIST
    ,TOUCHES_ATT_3RD
    ,TOUCHES_ATT_PEN
    ,TOUCHES_DEF_3RD
    ,TOUCHES_DEF_PEN
    ,TOUCHES_LIVE
    ,TOUCHES_MID_3RD
    ,TOUCHES_TOUCHES
    ,XAG

    ,CURRENT_TIMESTAMP AS loaded_at
FROM 
    {{ source('Bronze_data', 'stg_standard_stats') }} AS ss
-- JOIN remaining bronze tables ON player/squad
LEFT JOIN 
    {{ source('Bronze_data', 'stg_playing_time') }} AS pt
ON 
    pt.player = ss.player 
LEFT JOIN 
    {{ source('Bronze_data', 'stg_passing') }} AS pass
ON 
    pass.player = ss.player 
LEFT JOIN 
    {{ source('Bronze_data', 'stg_pass_types') }} AS pass_type
ON 
    pass_type.player = ss.player 
LEFT JOIN 
    {{ source('Bronze_data', 'stg_possession') }} AS pos
ON 
    pos.player = ss.player 
LEFT JOIN 
    {{ source('Bronze_data', 'stg_defensive_actions') }} AS def
ON 
    def.player = ss.player 
LEFT JOIN 
    {{ source('Bronze_data', 'stg_goal_shot_creation') }} AS gca
ON 
    gca.player = ss.player 
LEFT JOIN 
    {{ source('Bronze_data', 'stg_miscellaneous_stats') }} AS misc
ON 
    misc.player = ss.player
-- Join with dimension models
LEFT JOIN 
    {{ ref('dim_players') }} AS p
ON 
    p.player_name = ss.player
