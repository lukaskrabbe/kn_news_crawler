{{
  config(
        materialized='table',
  )
}}


WITH authors_list AS (
    SELECT
        authors AS author_list,
        CASE WHEN authors LIKE '%, %' THEN TRUE ELSE FALSE END AS multiple_authors,
        -- COUNT autors:
        CASE WHEN authors LIKE '%, %' THEN
            (LENGTH(authors) - LENGTH(REPLACE(authors, ',', ''))) / LENGTH(',') + 1
        ELSE 1 END AS author_count,
        -- SPLIT authors and remove tailing whitspace:
        CASE WHEN authors LIKE '%, %' THEN
            SPLIT_PART(authors, ',', 1)
        ELSE authors END AS author_1,
        CASE WHEN authors LIKE '%, %' THEN
            RIGHT(SPLIT_PART(authors, ',', 2), LENGTH(SPLIT_PART(authors, ',', 2))-1)
        ELSE NULL END AS author_2,
        CASE WHEN authors LIKE '%, %, %' THEN
            RIGHT(SPLIT_PART(authors, ',', 3), LENGTH(SPLIT_PART(authors, ',', 3))-1)
        ELSE NULL END AS author_3,
        kn_id as article_id,
        insert_timestamp
    FROM raw.article_data
    WHERE authors IS NOT NULL
), authors AS (
    -- get unique authors:
    SELECT DISTINCT author_1 AS author, article_id, insert_timestamp FROM authors_list WHERE author_1 IS NOT NULL
    UNION ALL
    SELECT DISTINCT author_2 AS author, article_id, insert_timestamp FROM authors_list WHERE author_2 IS NOT NULL
    UNION ALL
    SELECT DISTINCT author_3 AS author, article_id, insert_timestamp FROM authors_list WHERE author_3 IS NOT NULL
), author_fotos AS (
    -- extract (Fotos) from author to field
    SELECT
        CASE WHEN author LIKE '%(Fotos)' THEN
            LEFT(author, LENGTH(author)-7)
        ELSE author END AS author,
        CASE WHEN author LIKE '%(Fotos)' THEN TRUE ELSE FALSE END AS photo,
        article_id,
        insert_timestamp
    FROM authors
), author_text AS (
    -- extract (Fotos) from author to field
    SELECT
        CASE WHEN author LIKE '%(Text)' THEN
            LEFT(author, LENGTH(author)-6)
        ELSE author END AS author,
        photo,
        article_id,
        insert_timestamp
    FROM author_fotos
), author_names AS (
    -- split author into first and second name:
    SELECT
        author,
        CASE WHEN author LIKE '% %' THEN
            SPLIT_PART(author, ' ', 1)
        ELSE author END AS first_name,
        CASE WHEN author LIKE '% %' THEN
            RIGHT(author, LENGTH(author) - LENGTH(SPLIT_PART(author, ' ', 1)) - 1)
        ELSE NULL END AS last_name,
        photo,
        article_id,
        insert_timestamp
    FROM author_text
)
SELECT *
FROM author_names