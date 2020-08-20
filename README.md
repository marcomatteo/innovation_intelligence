# Innovation Intelligence
Project innovation intelligence

## Refactoring 04/2020

Dev'essere tutto ristrutturato come segue:

1. Per leggere i file fonte è necessario costruire una classe di interfaccia (**IParser**) che viene estesa nelle sue funzionalità da una classe specifica per i file csv (**IParserCsv**) e una per i file excel (**IParserXls**)

2. Una classe astratta **DataProvider** che viene implementata nei vari Data Provider che:
    
    - apre il file fonte (grazie al Parser dedicato)

    - implementa i metodi generici per interrogare il Data Provider dai test

3. Una classe per ogni Data Provider (come **Accredia**) che:

    - salva le informazioni sulla tipologia di dati nelle colonne del file fonte (per convertire correttamente il DataFrame in fase di test_acceptance) 

    - implementa metodi dedicati al Data Provider (preprocessing, filtraggio dei codici fiscali)

4. [Deprecated] Due classi di Logger:

    1. La classe di logger si chiama **TestLogger** e viene utilizzata per tenere traccia dei test delle classi realizzate con un'output in console e su file txt

    2. La classe **TestMarkdownOutput** che viene utilizzata per leggere i risultati dei test secondo una formattazione specifica

5. Ogni classe creata avrà una sua classe **AcceptanceBuilder** che riunisce le informazioni dettagliate sul file fonte con il Data Provider:

    - Dev'essere creato un file Excel contenente una tabella con la configurazione per il Data Provider specifico.
    La tabella dev'essere strutturata come segue:

    - Colonne:
        1. nome_colonna, testo : nome colonna non vincolante, utilizzata anche per definire la tipologia del file fonte nella prima riga
        
        2. tipologia_colonna, testo (*object*, *int*, *float*, *date*) : controllo se i valori sono compatibili

        3. lunghezza_massima_valori, numero intero : controllo che rispetti la lunghezza massima possibile

        4. contiene_valori_mancanti, True / False : controllo se può contenere valori mancanti

        5. chiave_primaria, True / False : controllo duplicati

    - Eccezione: la prima riga contiene la tipologia del file fonte nella colonna "nome colonna", il file Excel di configurazione procederà automaticamente a caricare le impostazioni di configurazione per il file fonte direttamente dalla seconda riga.
    

6. I Test:

    1. Test sui *parser*: **Test_IParserCsv** e **Test_IParserXls**. Utilizzando i file in ```/data/data_tests/IParsers/``` come verifica dei metodi e del funzionamento della classe

    2. Test sulle interfaccie lato db, ad esempio **Test_ICertificazioni**, in cui sono salvate le specifiche per ogni tipologia di informazioni sul database. Il test verifica che le informazioni siano sempre le stesse e che funzionino i metodi dedicati. **TODO:** costruire un file di config con le specifiche per ogni tabella

    3. Test sulle classi di Data Provider, ad esempio **Test_Accredia**, utilizzando un file fonte costruito per poter verificare che i metodi funzionino

    4. Test di certificazione in cui si verifica che i metodi delle classi Data Provider siano superati dato il vero file fonte come input

    