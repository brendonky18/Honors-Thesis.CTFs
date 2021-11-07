MODULE NAME
    speed_module - per user configuration of maximum allowed transfer speed

OPTIONS
    none

DESCRIPTION
    if user matches the pattern, his maximum allowed trasfer speed is
    set to the value of second field for downloading files, and to the third
    field for uploading.
    You can use * to match all users, or as mask, e.g. ab* matches all users
    beginning with ab. Order is important, first use most general patterns, 
    then specific ones (in other words, put default limits for * (all not 
    explicitly mentioned users) at the first line).
    If you set 0. as speed limit, it turns limiting off.
    