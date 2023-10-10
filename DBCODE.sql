/* 
This worksheet creates all tables for the pyproject.
*/

CREATE OR REPLACE DATABASE stocks_db;
USE DATABASE stocks_db;

-----------
-- GAMES -- 
-----------

CREATE OR REPLACE TABLE games 
(
    g_id INT AUTOINCREMENT
    , g_name TEXT
    , g_total_turns INT
    , g_sec_per_turn INT
    , g_starting_money NUMBER(20,2)
    , g_turns_between_events INT
    , g_player_count INT
    , g_stocks_count INT
    , g_is_open BOOLEAN
    
    , PRIMARY KEY(g_id)
);

------------
-- STOCKS --
------------

CREATE OR REPLACE TABLE stocks 
(
    s_id INT AUTOINCREMENT
    , s_name TEXT

    , PRIMARY KEY(s_id)
);

CREATE OR REPLACE TABLE forex_to_stocks 
(
    fs_stock_id INT 
    , fs_currency_id INT
    , fs_currency_weight NUMBER(8,2)

    , PRIMARY KEY (fs_stock_id, fs_currency_id)
);

CREATE OR REPLACE TABLE stock_market 
(
    sm_stock_id INT
    , sm_game_id INT
    , sm_turn_id INT
    , sm_stock_value NUMBER(8,2)

    , PRIMARY KEY (sm_stock_id, sm_game_id, sm_turn_id)
);

------------
-- TRADES -- 
------------

CREATE OR REPLACE TABLE transactions 
(
    t_id INT AUTOINCREMENT
    , t_game_id INT
    , t_turn_id INT
    , t_player_id INT
    , t_stock_id INT
    , t_type TEXT
    , t_stock_amount INT
    , t_money_amount NUMBER(20,2)
    , t_with_market BOOLEAN

    , PRIMARY KEY(t_id)
);

CREATE OR REPLACE TABLE portfolio 
(
    po_player_id INT 
    , po_game_id INT
    , po_stock_id INT
    , po_turn_id INT
    , po_amount INT
    
    , PRIMARY KEY(po_player_id, po_game_id, po_stock_id, po_turn_id)
);

-------------
-- PLAYERS --
-------------

CREATE OR REPLACE TABLE players
(
    pl_id INT AUTOINCREMENT
    , pl_name TEXT

    , PRIMARY KEY (pl_id)
);

CREATE OR REPLACE TABLE players_to_game 
( 
    ptg_player_id INT
    , ptg_game_id INT
    , ptg_turn_id INT
    , ptg_money_amount NUMBER(20, 2)

    , PRIMARY KEY (ptg_player_id, ptg_game_id, ptg_turn_id)
);

------------
-- EVENTS --
------------

-- CREATE OR REPLACE TABLE events 
-- (
--     e_id INT AUTOINCREMENT
--     , e_type TEXT
--     , e_content TEXT
--     , e_pct_or_total TEXT
--     , e_pct_change NUMBER(8,2)
--     , e_total_change NUMBER(8,2)

--     , PRIMARY KEY (e_id)
-- );   

-- CREATE OR REPLACE TABLE events_to_stocks 
-- (
--     es_event_id INT
--     , es_stock_id INT
--     , es_game_id INT

--     , PRIMARY KEY (es_event_id, es_stock_id)
-- );

------------
-- FOREX --
------------
SELECT * FROM CURRENCIES;
CREATE OR REPLACE TABLE currencies 
(
    c_id INT AUTOINCREMENT
    , c_code TEXT UNIQUE
    , c_name TEXT 
    , c_country TEXT
    , c_continent TEXT

    , PRIMARY KEY (c_id)
);

CREATE OR REPLACE TABLE forex_history 
(
    fh_timestamp_id INT
    , fh_currency_id INT
    , fh_date DATE
    , fh_value_to_dollar NUMBER(8,2)

    , PRIMARY KEY (fh_timestamp_id, fh_currency_id)
);





