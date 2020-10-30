05-05-2020 12:03:45 INFO     (setUpClass) 

## Test Data Provider : Ateco Infocamere 2020
-------------------

05-05-2020 12:03:45 INFO     (setUpClass) 

Apertura del file excel...

05-05-2020 12:05:08 INFO     (setUpClass) 

Apertura connessione con il DB...

05-05-2020 12:05:09 INFO     (setUpClass) 

Scarico le informazioni sulla tabella 'TMP_IC_CodiciAttivita'...

05-05-2020 12:05:10 DEBUG    (logDataFrameInfo) 

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 96201 entries, 0 to 96200
Data columns (total 7 columns):
 #   Column                  Non-Null Count  Dtype 
---  ------                  --------------  ----- 
 0   c fiscale               96201 non-null  object
 1   pv                      96201 non-null  object
 2   rea                     96201 non-null  object
 3   loc                     96201 non-null  object
 4   imp att                 91144 non-null  object
 5   ateco 2007              91144 non-null  object
 6   descrizione ateco 2007  91144 non-null  object
dtypes: object(7)
memory usage: 5.1+ MB

```

05-05-2020 12:05:10 INFO     (setUpClass) 

-------------------
05-05-2020 12:05:10 DEBUG    (setUp) 


05-05-2020 12:05:10 DEBUG    (test_acceptance_columnsMaxLength) 

### Test Acceptance Columns Max Lenght

05-05-2020 12:05:12 DEBUG    (logDifferences) 

|    |   Database |   DataProvider |
|---:|-----------:|---------------:|
|  0 |         11 |             11 |
|  1 |          2 |              6 |
|  2 |         10 |              7 |
|  4 |          1 |              1 |
|  5 |         10 |              8 |
|  6 |        200 |            200 |

05-05-2020 12:05:12 DEBUG    (tearDown) 

-------------------
05-05-2020 12:05:12 DEBUG    (setUp) 


05-05-2020 12:05:12 DEBUG    (test_acceptance_columnsNullable) 

### Test Acceptance Columns Nullables

05-05-2020 12:05:12 DEBUG    (logDifferences) 

|    |   Database |   DataProvider |
|---:|-----------:|---------------:|
|  0 |          0 |              0 |
|  1 |          1 |              0 |
|  2 |          1 |              0 |
|  3 |          1 |              0 |
|  4 |          1 |              1 |
|  5 |          1 |              1 |
|  6 |          1 |              1 |

05-05-2020 12:05:12 DEBUG    (tearDown) 

-------------------
05-05-2020 12:05:12 DEBUG    (setUp) 


05-05-2020 12:05:12 DEBUG    (test_acceptance_columnsNumber) 

### Test Acceptance Columns Number

05-05-2020 12:05:12 DEBUG    (logDifferences) 

|    | Database       | DataProvider           |
|---:|:---------------|:-----------------------|
|  0 | codice_fiscale | c fiscale              |
|  1 | provincia      | pv                     |
|  2 | rea            | rea                    |
|  3 | loc            | loc                    |
|  4 | imp_attivita   | imp att                |
|  5 | codiceateco    | ateco 2007             |
|  6 | descrizione    | descrizione ateco 2007 |

05-05-2020 12:05:12 DEBUG    (tearDown) 

-------------------
05-05-2020 12:05:12 DEBUG    (setUp) 


05-05-2020 12:05:12 DEBUG    (test_acceptance_columnsTypes_float) 

### Test Acceptance Columns Float Type

05-05-2020 12:05:12 DEBUG    (logDifferences_types) 

**OK**


05-05-2020 12:05:12 DEBUG    (tearDown) 

-------------------
05-05-2020 12:05:12 DEBUG    (setUp) 


05-05-2020 12:05:12 DEBUG    (test_acceptance_columnsTypes_int) 

### Test Acceptance Columns Int Type

05-05-2020 12:05:12 DEBUG    (logDifferences_types) 

**OK**


05-05-2020 12:05:12 DEBUG    (tearDown) 

-------------------
05-05-2020 12:05:12 DEBUG    (setUp) 


05-05-2020 12:05:12 DEBUG    (test_acceptance_columnsTypes_obj) 

### Test Acceptance Columns Object Type

05-05-2020 12:05:12 DEBUG    (logDifferences_types) 

**OK**


05-05-2020 12:05:12 DEBUG    (tearDown) 

-------------------
05-05-2020 12:05:12 DEBUG    (setUp) 


05-05-2020 12:05:12 DEBUG    (test_acceptance_fileExtension_xls) 

### Test Acceptance Estensione

05-05-2020 12:05:12 DEBUG    (logDifferences) 

|    | Database   | DataProvider   |
|---:|:-----------|:---------------|
|  0 | xlsx       | xlsx           |

05-05-2020 12:05:12 DEBUG    (tearDown) 

-------------------
