WITH 
	rain 
AS (
	SELECT Date
	FROM weather
	WHERE Events = 'Rain'
	GROUP BY Date
),

rain_trips AS (
SELECT trip_id
	,duration
	,DATE(start_date) as trip_date
FROM trips
JOIN rain
ON rain.date = trip_date

ORDER BY duration desc
)

SELECT trip_date
	,MAX(duration)
FROM rain_trips
GROUP BY trip_date