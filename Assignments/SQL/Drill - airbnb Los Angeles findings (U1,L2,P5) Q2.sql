SELECT COUNT(`id`) AS '#_of_listings' 
	--,`name`
	--,`host_name` 
	,`neighbourhood` 
	--,`room_type` 
	,avg(`price`) AS 'AVG_Price' 
	--,`minimum_nights` 
	,COUNT(`number_of_reviews`)  AS 'Total_reviews'
	,AVG(`reviews_per_month`) AS 'AVG_reviews_per_month' 
	--,`availability_365`
FROM listings

GROUP BY `neighbourhood` 

ORDER BY COUNT(`number_of_reviews`) desc