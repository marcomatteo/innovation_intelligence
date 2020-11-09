SELECT TOP (1000) [ID_DATA_FinanziamentiUE_Impresa]
      ,A.[IDProgetto]
      ,[Acronimo]
      ,A.[TipoProgramma]
      ,[IDImpresa]
      ,[CF]
      ,[Denominazione]
      ,[DenominazioneBreve]
      ,[TipoAttivita]
      ,[PartecipazioneConclusa]
      ,[Finanziamento]
      ,[UrlImpresa]
      ,B.[Topic]
  FROM (
      [I2FVGData_staging].[dbo].[DATA_FinanziamentiUE_Impresa] AS A
      INNER JOIN
      [I2FVGData_staging].[dbo].[DATA_FinanziamentiUE_Progetto_Tema] AS B
      ON A.IDProgetto = B.IDProgetto )
  WHERE [CF] = '00823410303'