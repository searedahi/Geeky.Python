CREATE TABLE [Locations] (
  [Id] uniqueidentifier PRIMARY KEY NOT NULL
, [Lat] real NULL
, [Lon] real NULL
, [Date] datetime DEFAULT CURRENT_TIMESTAMP NOT NULL
, [DeviceId] uniqueidentifier NULL
);
GO

CREATE TABLE [Hits] (
  [Id] uniqueidentifier PRIMARY KEY NOT NULL
, [SensorId] int NULL
, [Date] datetime DEFAULT CURRENT_TIMESTAMP NOT NULL
, [DeviceId] uniqueidentifier NULL
);
GO

CREATE TABLE [Temperatures] (
  [Id] uniqueidentifier PRIMARY KEY NOT NULL
, [SensorReading] real NULL
, [Date] datetime DEFAULT CURRENT_TIMESTAMP NOT NULL
, [DeviceId] uniqueidentifier NULL
);
GO


CREATE VIEW [TemperaturesView] AS
SELECT [Id]
	, [SensorReading]
	, ([SensorReading] / 1000) AS [Celcius]
	, (([SensorReading] / 1000) * 9.0 / 5.0 + 32.0) AS [Farenheight]
	, [Date]
	, [DeviceId]
FROM
	[Temperatures]
GO