#!/usr/bin/env python
# coding: utf-8

# # Answering Business Questions Using SQL

# Connect to the source database

# In[1]:


get_ipython().run_cell_magic('capture', '', '%load_ext sql\n%sql sqlite:///chinook.db')


# # Overview of the Data

# In[4]:


get_ipython().run_cell_magic('sql', '', 'SELECT name,\n    type\nFROM sqlite_master\nWHERE type IN ("table","view");')


# # Selecting New Albums to Purchase

# In[5]:


get_ipython().run_cell_magic('sql', '', '\nWITH usa_tracks_sold AS\n   (\n    SELECT il.* FROM invoice_line il\n    INNER JOIN invoice i on il.invoice_id = i.invoice_id\n    INNER JOIN customer c on i.customer_id = c.customer_id\n    WHERE c.country = "USA"\n   )\n\nSELECT\n    g.name genre,\n    count(uts.invoice_line_id) tracks_sold,\n    cast(count(uts.invoice_line_id) AS FLOAT) / (\n        SELECT COUNT(*) from usa_tracks_sold\n    ) percentage_sold\nFROM usa_tracks_sold uts\nINNER JOIN track t on t.track_id = uts.track_id\nINNER JOIN genre g on g.genre_id = t.genre_id\nGROUP BY 1\nORDER BY 2 DESC\nLIMIT 10;')


# Based on the sales of tracks across different genres in the USA, we should purchase the new albums by the following artists:
# 
# Red Tone (Punk)
# Slim Jim Bites (Blues)
# Meteor and the Girls (Pop)

# # Analyzing Employee Sales Performance

# In[6]:


get_ipython().run_cell_magic('sql', '', '\nWITH customer_support_rep_sales AS\n    (\n     SELECT\n         i.customer_id,\n         c.support_rep_id,\n         SUM(i.total) total\n     FROM invoice i\n     INNER JOIN customer c ON i.customer_id = c.customer_id\n     GROUP BY 1,2\n    )\n\nSELECT\n    e.first_name || " " || e.last_name employee,\n    e.hire_date,\n    SUM(csrs.total) total_sales\nFROM customer_support_rep_sales csrs\nINNER JOIN employee e ON e.employee_id = csrs.support_rep_id\nGROUP BY 1;')


# While there is a 20% difference in sales between Jane (the top employee) and Steve (the bottom employee), the difference roughly corresponds to the differences in their hiring dates.

# # Analyzing Sales by Country

# In[7]:


get_ipython().run_cell_magic('sql', '', '\nWITH country_or_other AS\n    (\n     SELECT\n       CASE\n           WHEN (\n                 SELECT count(*)\n                 FROM customer\n                 where country = c.country\n                ) = 1 THEN "Other"\n           ELSE c.country\n       END AS country,\n       c.customer_id,\n       il.*\n     FROM invoice_line il\n     INNER JOIN invoice i ON i.invoice_id = il.invoice_id\n     INNER JOIN customer c ON c.customer_id = i.customer_id\n    )\n\nSELECT\n    country,\n    customers,\n    total_sales,\n    average_order,\n    customer_lifetime_value\nFROM\n    (\n    SELECT\n        country,\n        count(distinct customer_id) customers,\n        SUM(unit_price) total_sales,\n        SUM(unit_price) / count(distinct customer_id) customer_lifetime_value,\n        SUM(unit_price) / count(distinct invoice_id) average_order,\n        CASE\n            WHEN country = "Other" THEN 1\n            ELSE 0\n        END AS sort\n    FROM country_or_other\n    GROUP BY country\n    ORDER BY sort ASC, total_sales DESC\n    );')


# Based on the data, there may be opportunity in the following countries:
# 
# Czech Republic
# United Kingdom
# India
# 

# # Albums vs. Individual Tracks

# In[8]:


get_ipython().run_cell_magic('sql', '', '\nWITH invoice_first_track AS (\n  SELECT\n    il.invoice_id AS invoice_id,\n    MIN(il.track_id) AS first_track_id\n  FROM\n    invoice_line il\n  GROUP BY\n    1\n)\n\n-- Use a subquery to select the results of the invoice_first_track CTE and determine whether customers made album purchases\nSELECT\n  album_purchase,\n  COUNT(invoice_id) AS number_of_invoices,\n  CAST(COUNT(invoice_id) AS FLOAT) / (\n    SELECT COUNT(*) FROM invoice\n  ) AS percent\nFROM\n  (\n    SELECT\n      ifs.*,\n      CASE\n        -- Use the EXCEPT operator to compare the tracks in the first invoice with the tracks in subsequent invoices,\n        -- and determine whether any tracks from the album were purchased in subsequent invoices.\n        -- If the result of the EXCEPT is NULL, it means that all tracks from the album were purchased in subsequent invoices,\n        -- and the customer made an album purchase.\n        -- If the result of the EXCEPT is not NULL, it means that at least one track from the album was not purchased in subsequent invoices,\n        -- and the customer did not make an album purchase.\n        WHEN (\n          SELECT\n            t.track_id\n          FROM\n            track t\n          WHERE\n            t.album_id = (\n              SELECT\n                t2.album_id\n              FROM\n                track t2\n              WHERE\n                t2.track_id = ifs.first_track_id\n            )\n          EXCEPT\n          SELECT\n            il2.track_id\n          FROM\n            invoice_line il2\n          WHERE\n            il2.invoice_id = ifs.invoice_id\n        ) IS NULL\n        AND (\n          SELECT\n            il2.track_id\n          FROM\n            invoice_line il2\n          WHERE\n            il2.invoice_id = ifs.invoice_id\n          EXCEPT\n          SELECT\n            t.track_id\n          FROM\n            track t\n          WHERE\n            t.album_id = (\n              SELECT\n                t2.album_id\n              FROM\n                track t2\n              WHERE\n                t2.track_id = ifs.first_track_id\n            )\n        ) IS NULL\n        THEN "yes"\n        ELSE "no"\n      END AS album_purchase\n    FROM\n      invoice_first_track ifs\n  ) subquery\n-- Group by album_purchase to get the counts and percentages for each type of purchase\nGROUP BY\n  album_purchase;')


# Album purchases account for 18.6% of purchases. Based on this data, I would recommend against purchasing only select tracks from albums from record companies, since there is potential to lose one fifth of revenue
