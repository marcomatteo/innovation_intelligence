SELECT distinct 
-- [ID_FinanziamentiUE_Schema]
      [SchemaFinanziamento]
      ,[Schema]
      ,[Descrizione]
    --   ,[RF_FinanziamentiUE_TipoProgramma]
  FROM [I2FVGData_staging].[dbo].[SVC_FinanziamentiUE_Schema]
  where [SchemaFinanziamento] IN (
    'CSA',
    'RIA',
    'IA',
    'MSCA-RISE',
    'SGA-RIA',
    'MSCA-ITN-ETN',
    'Shift2Rail-RIA',
    'ECSEL-RIA',
    'BBI-RIA',
    'MSCA-ITN-EID',
    'Shift2Rail-IA',
    'ECSEL-IA',
    'BBI-IA-DEMO',
    'H2020-EEN-SGA',
    'Shift2Rail-CSA',
    'MSCA-COFUND-DP',
    'MSCA-ITN-EJD',
    'FCH2-RIA'
  )