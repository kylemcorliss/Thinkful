SELECT `id` 
	,`name`
	,`host_name` 
	,`neighbourhood` 
	,`room_type` 
	,MAX(`price`) 
	,`minimum_nights` 
	,`number_of_reviews` 
	,`reviews_per_month` 
	,`availability_365`
FROM listings

GROUP BY `id` 
	, `name`
	, `host_name` 
	, `neighbourhood` 
	, `room_type`  
	, `minimum_nights` 
	, `number_of_reviews` 
	, `reviews_per_month` 
	, `availability_365`

ORDER BY MAX(price) desc
LIMIT 1

-- The most expensive listing is the historic hollywood hills estate for $25k, but there are 0 reviews. 
-- So it doesn't seem like there is a lot of traffic for this site.
	