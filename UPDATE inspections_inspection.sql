UPDATE inspections_inspection
SET scheduledDate = substr(scheduledDate,1,10)
-- convert datetime to date