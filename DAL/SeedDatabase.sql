-- Script Date: 4/9/2016 11:12 AM  - ErikEJ.SqlCeScripting version 3.5.2.58
CREATE TABLE [Locations] (
  [Id] uniqueidentifier NOT NULL
, [Lat] float NULL
, [Lon] float NULL
, [Date] datetime DEFAULT time('now') NOT NULL
, [DeviceId] uniqueidentifier NULL
, CONSTRAINT [PK_Locations] PRIMARY KEY ([Id])
);
