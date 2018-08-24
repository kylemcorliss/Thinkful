WITH 
	rain 
AS (
	SELECT 
		Date
	FROM weather
	WHERE Events = 'Rain'
	GROUP BY 1
)

SELECT trip_id
	,duration
	,DATE(start_date) as trip_date
FROM trips t
JOIN rain
ON rain.date = trip_date

ORDER BY duration desc
LIMIT 3