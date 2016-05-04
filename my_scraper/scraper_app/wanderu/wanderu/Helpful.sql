
-- Merge QA to PROD

INSERT INTO trips_prod (tripid, carrier, origintime, origincity, 
	originlocation, destinationtime, destinationcity, destinationlocation, 
	price, duration, features, dateoftrip, datescraped)

SELECT tripid, carrier, origintime, origincity, originlocation, 
destinationtime, destinationcity, destinationlocation, price, duration, 
features, dateoftrip, datescraped 
FROM trips_load; 

-- Empty QA

TRUNCATE trips_load ;