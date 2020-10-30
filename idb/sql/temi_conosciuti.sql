SELECT distinct 
        -- [ID_FinanziamentiUETema]
      [Topic]
      ,[Tema]
      ,[Descrizione]
    --   ,[RF_FinanziamentiUE_TipoProgramma]
  FROM [I2FVGData_staging].[dbo].[SVC_FinanziamentiUETema]
  WHERE [Topic] IN (
    'REV-INEQUAL-12-2017',
    'CULT-COOP-11-2016-2017',
    'DT-SPIRE-06-2019',
    'ICT-19-2019',
    'EIC-SMEInst-2018-2020',
    'ICT-17-2018',
    'ICT-19-2017',
    'MSCA-RISE-2017',
    'MG-8-4-2017',
    'ICT-08-2017',
    'IoT-01-2016',
    'ICT-26-2016',
    'INFRAIA-1-2014-2015',
    'SC1-BHC-28-2019',
    'FETOPEN-01-2018-2019-2020',
    'MG-7-3-2017',
    'SGA-FET-GRAPHENE-2017',
    'MSCA-ITN-2017',
    'S2R-OC-IP2-01-2017',
    'MG-2.3-2016',
    'ECSEL-2016-1',
    'WASTE-6a-2015',
    'DT-ICT-07-2018-2019',
    'BBI.2017.R4',
    'CE-SPIRE-10-2018',
    'COMPET-7-2017',
    'LC-MG-1-3-2018',
    'MG-2-2-2018',
    'INFRADEV-01-2017',
    'IoT-03-2017',
    'ICT-05-2019',
    'ICT-09-2019-2020',
    'LCE-06-2015',
    'ICT-07-2017',
    'MG-6.3-2015',
    'MG-4.3-2015',
    'BBI.2017.R7',
    'ICT-01-2016',
    'EE-10-2016',
    'FETOPEN-RIA-2014-2015',
    'S2R-OC-IP2-01-2019',
    'S2R-OC-IP2-02-2019',
    'MG-5-2-2017',
    'ECSEL-2018-1-IA',
    'SU-ICT-03-2018',
    'SFS-30-2018-2019-2020',
    'S2R-OC-IP2-02-2018',
    'S2R-OC-IP4-01-2018',
    'BBI.2017.D5',
    'LCE-06-2017',
    'GALILEO-1-2017',
    'S2R-OC-IP2-02-2017',
    'S2R-OC-IP5-01-2017',
    'SEC-19-BES-2016',
    'BG-01-2016',
    'PHC-11-2015',
    'ICT-35-2018',
    'NMP-10-2014',
    'FoF-11-2015',
    'MG-4.1-2014',
    'SGA-FET-GRAPHENE-2019',
    'INFRAIA-01-2016-2017',
    'ICT-13-2018-2019',
    'MSCA-RISE-2016',
    'ICT-07-2014',
    'ICT-18-2018',
    'SEC-12-FCT-2016-2017',
    'FOF-03-2016',
    'SFS-07b-2015',
    'SCC-01-2015',
    'MG-2.3-2014',
    'EIC-FTI-2018-2020',
    'MSCA-RISE-2019',
    'CE-SC5-01-2018',
    'NMBP-23-2016',
    'WASTE-1-2014',
    'MSCA-ITN-2016',
    'SwafS-05-2017',
    'NMBP-35-2017',
    'ICT-30-2017',
    'S2R-OC-IP2-02-2015',
    'NMBP-10-2016',
    'ICT-09-2017',
    'SC5-21-2016-2017',
    'DT-TRANSFORMATIONS-11-2019',
    'MSCA-ITN-2018',
    'MG-4.2-2014',
    'MG-8.2a-2014',
    'MG-5.3-2014',
    'MG-7.2a-2014',
    'MG-6.2-2014',
    'FOF-11-2016',
    'CE-SPIRE-05-2019',
    'LC-SC3-SCC-1-2018-2019-2020',
    'DT-BG-04-2018-2019',
    'ICT-23-2019',
    'SwafS-01-2018-2019-2020',
    'MG-2-1-2018',
    'MSCA-ITN-2019',
    'BBI.2018.SO2.D3',
    'BIOTEC-03-2018',
    'SU-DRS03-2018-2019-2020',
    'LC-SC3-EE-9-2018-2019',
    'SU-DS05-2018-2019',
    'INNOSUP-09-2018',
    'LC-SFS-03-2018',
    'H2020EENSGA3',
    'MG-4-3-2018',
    'ICT-11-2018-2019',
    'ICT-04-2018',
    'MG-7-1-2017',
    'NMBP-22-2017',
    'ICT-25-2016-2017',
    'FETOPEN-01-2016-2017',
    'EE-16-2016-2017',
    'SMEInst-06-2016-2017',
    'SMEInst-10-2016-2017',
    'SMEInst-11-2016-2017',
    'LCE-04-2017',
    'SMEInst-04-2016-2017',
    'MG-2.2-2016',
    'BBI-2016-D05',
    'SFS-03-2016',
    'SFS-06-2016',
    'SMEInst-09-2016-2017',
    'BBI-2016-D03',
    'EE-22-2016-2017',
    'H2020-SGA2-EEN',
    'SMEInst-12-2016-2017',
    'ICT-10-2016',
    'EUJ-01-2016',
    'S2R-OC-IP2-03-2015',
    'S2R-OC-IP4-02-2016',
    'MG-3.6b-2015',
    'S2R-OC-IP4-01-2016',
    'ICT-14-2016-2017',
    'FTIPilot-1-2015',
    'NMP-19-2015',
    'ICT-19-2015',
    'MG-5.5a-2015',
    'ECSEL-07-2015',
    'CIP-01-2016-2017',
    'EE-07-2015',
    'LCE-14-2015',
    'PHC-02-2015',
    'SCC-03-2015',
    'ICT-30-2015',
    'FETFLAGSHIP',
    'MSCA-ITN-2015-ETN',
    'ICT-10-2015',
    'ICT-37-2015-1',
    'PHC-12-2015-1',
    'ICT-27-2015',
    'FETHPC-1-2014',
    'ICT-12-2015',
    'FoF-14-2015',
    'ICT-14-2014',
    'INNOVATION',
    'ICT-28-2015',
    'NMP-25-2014-1',
    'BBI.VC2.R4',
    'WASTE-3-2014',
    'PHC-12-2014',
    'MSCA-COFUND-2014-DP',
    'PHC-19-2014',
    'ICT-06-2014',
    'MSCA-RISE-2014',
    'ICT-26-2014',
    'LCE-07-2014',
    'NMP-01-2014',
    'DS-02-2014',
    'ICT-23-2014',
    'GALILEO-1-2014',
    'MSCA-ITN-2014-EJD',
    'MSCA-ITN-2014-ETN',
    'MSCA-ITN-2014-EID',
    'GALILEO-2-2014',
    'LCE-02-2014',
    'SC1-DTH-03-2018',
    'EeB-01-2014',
    'MG-2.2-2014',
    'FCH-04-3-2019',
    'SwafS-19-2018-2019-2020'
)