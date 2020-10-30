05-05-2020 12:06:06 INFO     (setUpClass) 

## Test Data Provider : Bilanci Infocamere 2020
-------------------

05-05-2020 12:06:06 INFO     (setUpClass) 

Apertura del file excel...

05-05-2020 12:06:47 INFO     (setUpClass) 

Apertura connessione con il DB...

05-05-2020 12:06:48 INFO     (setUpClass) 

Scarico le informazioni sulla tabella 'TMP_IC_DatiStoricizzati'...

05-05-2020 12:06:50 DEBUG    (logDataFrameInfo) 

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 95652 entries, 0 to 95651
Data columns (total 18 columns):
 #   Column                                          Non-Null Count  Dtype 
---  ------                                          --------------  ----- 
 0   c fiscale                                       95652 non-null  object
 1   cia                                             95652 non-null  object
 2   rea                                             95652 non-null  object
 3   anno                                            95652 non-null  object
 4   Totale attivo                                   95652 non-null  object
 5   Totale Immobilizzazioni immateriali             95652 non-null  object
 6   Crediti esigibili entro l'esercizio successivo  95528 non-null  object
 7   Totale patrimonio netto                         95652 non-null  object
 8   Debiti esigibili entro l'esercizio successivo   95528 non-null  object
 9   Totale valore della produzione                  95652 non-null  object
 10  Ricavi delle vendite                            95652 non-null  object
 11  Totale Costi del Personale                      95652 non-null  object
 12  Differenza tra valore e costi della produzione  95652 non-null  object
 13  Ammortamento Immobilizzazione Immateriali       95652 non-null  object
 14  Utile/perdita esercizio ultimi                  95652 non-null  object
 15  valore aggiunto                                 95652 non-null  object
 16  tot.aam.acc.svalutazioni                        95652 non-null  object
 17  (ron) reddito operativo netto                   95652 non-null  object
dtypes: object(18)
memory usage: 13.1+ MB

```

05-05-2020 12:06:50 INFO     (setUpClass) 

-------------------
05-05-2020 12:06:50 DEBUG    (setUp) 


05-05-2020 12:06:50 DEBUG    (test_acceptance_columnsMaxLength) 

### Test Acceptance Columns Max Lenght

05-05-2020 12:06:53 DEBUG    (logDifferences) 

|    |   Database |   DataProvider |
|---:|-----------:|---------------:|
|  0 |         11 |             11 |
|  1 |          2 |              6 |
|  2 |         10 |              7 |

05-05-2020 12:06:53 DEBUG    (tearDown) 

-------------------
05-05-2020 12:06:53 DEBUG    (setUp) 


05-05-2020 12:06:53 DEBUG    (test_acceptance_columnsNullable) 

### Test Acceptance Columns Nullables

05-05-2020 12:06:53 DEBUG    (logDifferences) 

|    | Database   | DataProvider   |
|---:|:-----------|:---------------|
|  0 | False      | False          |
|  1 | False      | False          |
|  2 | True       | False          |
|  3 | False      | False          |
|  4 | True       | False          |
|  5 | True       | False          |
|  6 | True       | True           |
|  7 | True       | False          |
|  8 | True       | True           |
|  9 | True       | False          |
| 10 | True       | False          |
| 11 | True       | False          |
| 12 | True       | False          |
| 13 | True       | False          |
| 14 | True       | False          |
| 15 | True       | False          |

05-05-2020 12:06:53 DEBUG    (tearDown) 

-------------------
05-05-2020 12:06:53 DEBUG    (setUp) 


05-05-2020 12:06:53 DEBUG    (test_acceptance_columnsNumber) 

### Test Acceptance Columns Number

05-05-2020 12:06:53 DEBUG    (logDifferences) 

|    | Database                | DataProvider                                   |
|---:|:------------------------|:-----------------------------------------------|
|  0 | codice_fiscale          | c fiscale                                      |
|  1 | cia                     | cia                                            |
|  2 | rea                     | rea                                            |
|  3 | anno                    | anno                                           |
|  4 | totale_attivo           | Totale attivo                                  |
|  5 | totale_immobilizzazioni | Totale Immobilizzazioni immateriali            |
|  6 | crediti                 | Crediti esigibili entro l'esercizio successivo |
|  7 | totale_patrimonio       | Totale patrimonio netto                        |
|  8 | debiti                  | Debiti esigibili entro l'esercizio successivo  |
|  9 | totale_produzione       | Totale valore della produzione                 |
| 10 | ricavi                  | Ricavi delle vendite                           |
| 11 | costi_personale         | Totale Costi del Personale                     |
| 12 | differenza_costi        | Differenza tra valore e costi della produzione |
| 13 | ammortamento            | Ammortamento Immobilizzazione Immateriali      |
| 14 | utile                   | Utile/perdita esercizio ultimi                 |
| 15 | valore_aggiunto         | valore aggiunto                                |

05-05-2020 12:06:53 DEBUG    (tearDown) 

-------------------
05-05-2020 12:06:53 DEBUG    (setUp) 


05-05-2020 12:06:53 DEBUG    (test_acceptance_columnsTypes_float) 

### Test Acceptance Columns Float Type

05-05-2020 12:06:53 DEBUG    (logDifferences_types) 

**OK**


05-05-2020 12:06:53 DEBUG    (tearDown) 

-------------------
05-05-2020 12:06:53 DEBUG    (setUp) 


05-05-2020 12:06:53 DEBUG    (test_acceptance_columnsTypes_int) 

### Test Acceptance Columns Int Type

05-05-2020 12:06:53 DEBUG    (logDifferences_types) 

**OK**


05-05-2020 12:06:53 DEBUG    (tearDown) 

-------------------
05-05-2020 12:06:53 DEBUG    (setUp) 


05-05-2020 12:06:53 DEBUG    (test_acceptance_columnsTypes_obj) 

### Test Acceptance Columns Object Type

05-05-2020 12:06:53 DEBUG    (logDifferences_types) 

**OK**


05-05-2020 12:06:53 DEBUG    (tearDown) 

-------------------
05-05-2020 12:06:53 DEBUG    (setUp) 


05-05-2020 12:06:53 DEBUG    (test_acceptance_fileExtension_xls) 

### Test Acceptance Estensione

05-05-2020 12:06:53 DEBUG    (logDifferences) 

|    | Database   | DataProvider   |
|---:|:-----------|:---------------|
|  0 | xlsx       | xlsx           |

05-05-2020 12:06:53 DEBUG    (tearDown) 

-------------------
05-05-2020 12:06:53 DEBUG    (setUp) 


05-05-2020 12:06:53 DEBUG    (test_validity_keys) 

### Test Validity Primary Keys

05-05-2020 12:06:53 DEBUG    (logDifferences) 

|    | Database             | DataProvider   |
|---:|:---------------------|:---------------|
|  0 | c fiscale, cia, anno | False          |

05-05-2020 12:06:53 DEBUG    (tearDown) 

-------------------
