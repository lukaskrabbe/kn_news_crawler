{{
  config(
        materialized='table',
  )
}}

WITH raw_data AS (
    SELECT
        kn_id as article_id,
        title as article_title,
        subtitle as article_subtitle,
        releasedate as article_releasedate,
        city as article_city,
        resort as article_resort,
        body as article_body,
        insert_timestamp
    FROM raw.article_data
), extract_city AS (
        SELECT
            article_id,
            article_title,
            article_subtitle,
            article_releasedate,
            substring((REGEXP_MATCHES(article_body, '^[A-zßöäüÖÄÜ/-]{1,}[.]|^[A-zßöäüÖÄÜ/-]{1,} [A-zßöäüÖÄÜ/-]{1,}[.]'))[1], 1, length((REGEXP_MATCHES(article_body, '^[A-zßöäüÖÄÜ/-]{1,}[.]|^[A-zßöäüÖÄÜ/-]{1,} [A-zßöäüÖÄÜ/-]{1,}[.]'))[1])-1) AS article_city_ii,
            article_resort,
            substring(article_body, length((REGEXP_MATCHES(article_body, '^[A-zßöäüÖÄÜ/-]{1,}[.]|^[A-zßöäüÖÄÜ/-]{1,} [A-zßöäüÖÄÜ/-]{1,}[.]'))[1])+2) as article_body,
            insert_timestamp
        FROM raw_data
    UNION
        SELECT
            article_id,
            article_title,
            article_subtitle,
            article_releasedate,
            substring((REGEXP_MATCHES(article_body, '^ [A-zßöäüÖÄÜ/-]{1,}[.]|^ [A-zßöäüÖÄÜ/-]{1,} [A-zßöäüÖÄÜ/-]{1,}[.]'))[1], 2, length((REGEXP_MATCHES(article_body, '^ [A-zßöäüÖÄÜ/-]{1,}[.]|^ [A-zßöäüÖÄÜ/-]{1,} [A-zßöäüÖÄÜ/-]{1,}[.]'))[1])-2) AS article_city_ii,
            article_resort,
            substring(article_body, length((REGEXP_MATCHES(article_body, '^ [A-zßöäüÖÄÜ/-]{1,}[.]|^ [A-zßöäüÖÄÜ/-]{1,} [A-zßöäüÖÄÜ/-]{1,}[.]'))[1])+2) as article_body,
            insert_timestamp
        FROM raw_data
), union_cities AS (
    SELECT *
    FROM raw_data
    WHERE article_id NOT IN (SELECT article_id FROM extract_city)
        UNION
    SELECT *
    FROM extract_city
), clean_body_start AS (
    SELECT
        article_id,
        article_title,
        article_subtitle,
        article_releasedate,
        article_city,
        article_resort,
        CASE WHEN article_body LIKE '. %' OR article_body LIKE ' %' OR article_body LIKE ';%' OR article_body LIKE '*%' THEN substring(article_body, 2) ELSE article_body END as article_body,
        insert_timestamp
    FROM union_cities
), add_und_dann_article AS (
    SELECT
        article_id,
        article_title,
        article_subtitle,
        article_releasedate,
        article_city,
        article_resort,
        CASE WHEN (article_body LIKE '...%') AND article_resort = 'Panorama' THEN 'Und dann' || substring(article_body, 4) ELSE article_body END AS article_body,
        insert_timestamp
    FROM clean_body_start
), remove_trash AS (
    SELECT
        article_id,
        article_title,
        CASE WHEN article_subtitle LIKE 'Weiter auf %' THEN NULL ELSE article_subtitle END AS article_subtitle,
        article_releasedate,
        article_city,
        article_resort,
        replace(replace(replace(article_body, '■ ;', ' '), ';', ' '), '  ', ' ') AS article_body,
        insert_timestamp
    FROM add_und_dann_article
), add_lotto_and_fotos AS(
    SELECT
        article_id,
        article_title,
        article_subtitle,
        article_releasedate,
        article_city,
        article_resort,
        article_body,
        CASE WHEN article_body LIKE '%6 aus 49%' OR article_body LIKE '%Alle Angaben ohne Gewähr%' THEN TRUE ELSE FALSE END AS is_lotto,
        CASE WHEN article_body LIKE 'Fotos: %' THEN TRUE ELSE FALSE END AS is_foto,
        CASE WHEN article_body LIKE 'Redaktion 04%' THEN TRUE ELSE FALSE END AS is_redaktion,
        CASE WHEN (article_body LIKE '%Eurosport%' AND (article_resort = 'Sport Aufschlag' OR article_resort = 'Sport')) THEN TRUE ELSE FALSE END AS is_sport_programm,
        CASE WHEN (article_body LIKE '% Nächste Spiele' AND (article_resort = 'Sport Aufschlag' OR article_resort = 'Sport')) THEN TRUE ELSE FALSE END AS is_naechste_spiele,
        insert_timestamp
    FROM remove_trash
)
SELECT *
FROM add_lotto_and_fotos
