SELECT SUBSTR(r.date,6,2) AS 'month' 
	,COUNT(r.listing_id) AS '#_of_trans'
	,AVG(l.Price) AS 'AVG_Price'
FROM reviews r
LEFT JOIN listings l
ON l.id = r.listing_id

GROUP BY SUBSTR(r.date,6,2)

ORDER BY COUNT(l.number_of_reviews) desc

-- July (07) is the most expensive month on average
-- July (07) is also the most popular time for reviews and therefore transactions
-- I am using the reviews dated on a certain day as a transaction count