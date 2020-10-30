# Linee guida test su Data Provider

## Note

I test sono fondamentali per uno sviluppo consistente del prodotto e 
delle funzionalità di questo progetto.

I test sono stati suddivisi in sottocartelle per tipologie comuni, quali:

1. Acceptance test dei Data Providers: i test per certificare se un file fonte può essere importato in Innovation Intelligence

2. Certificate test per la certificazione degli aggiornamenti (**da definire**): i test che permettono di automatizzare parte dei controlli qualità alla piattaforma

3. Test per le classi dei Data Provider: test funzionali interni alla libreria per verificare il funzionamento della classe di Data Provider utilizzata

4. Test per le classi File Parser: test funzionali interni alla libreria per verificare il funzionamento della classe di File Parser utilizzata

5. Test per le classi di Logging: test funzionali interni alla libreria per verificare il funzionamento della classe di Logging utilizzata

Per poter eseguire i test di ogni punto qui sopra, si può utilizzare il seguente
comando da terminale:

``` 
>>> python -W ignore -m unittest discover tests\CARTELLA[\FILE_OPZIONALE]
```

Per controllare le classi di Data Provider eseguire:

``` 
>>> python -W ignore -m unittest discover tests\test_data_provider
```

## Classe Test_* (usata per ogni Data Provider)

La classe di test ha la funzione di aprire il file fonte e di effettuare i controlli per verificare la correttezza delle informazioni da aggiungere al database.

Il controllo era stato inizialmente impostato manualmente per ogni Data Provider secondo le informazioni passate da Riccardo Portolan (guardando le tabelle del DB).

Successivamente, ho aggiunto l'interfaccia con il DB per recuperare le informazioni automaticamente dalle tabelle temporanee (utilizzate per inserire i dati che poi verranno elaborati dalle ETL). (**ancora da implementare**)

### Attributi

Attributi della classe Test_DataProvider:

* ` `  ` file_name `  ` ` : Nome del file fonte da testare

* ` `  ` db_table_name `  ` ` : Nome della tabella del DB su cui i dati vengono caricati

* ` `  ` columns_constraints `  ` ` : colonne che identificano univocamente ogni riga del file fonte

* ` `  ` date_format `  ` ` : Formattazione della colonna data (se presente)

### Metodi

Da scrivere una volta effettuato refactoring.

## Inserimento di un nuovo Data Provider

Per inserire un nuovo Data Provider nei controlli del file fonte...

## Aggiornamento dei file fonte prima di eseguire i test

Per aggiornare i dati di un Data Provider, fornendo il nuovo file fonte da controllare, è necessario:

* rinominare il file come Dio comanda

* copiarlo nella cartella giusta

* aggiustare i parametri di test in caso di modifiche non registrate nel tempo sul DB (evitabile se si interroga direttamente il DB in fase di acceptance test)
