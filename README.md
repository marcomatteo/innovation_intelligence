# Innovation Intelligence
Project innovation intelligence

## Refactoring 04/2020

Dev'essere tutto ristrutturato come segue:

1. Per leggere i file fonte è necessario costruire una classe di interfaccia (**IParser**) che viene estesa nelle sue funzionalità da una classe specifica per i file csv (**IParserCsv**) e una per i file excel (**IParserXls**)

2. Per leggere il Database è necessario costruire una classe di interfaccia (**II2FVG**) che viene estesa nelle sue funzionalità da ogni tipologia di informazione inserita nel DB. Ad esempio **ICertificazioni** per poter leggere le informazioni sulle certificazioni, **ICreditRating** per i rating di Modefinance e così via...

3. Una classe astratta **DataProvider** che viene implementata nei vari Data Provider (come **Accredia**) che:
    
    - apre il file fonte (grazie al Parser dedicato)

    - salva le informazioni delle tabelle e dei record sul Database (grazie all'interfaccia dedicata)

    - implementa metodi dedicati per ogni Data Provider

    - effettua le operazioni di certificazione

4. Due classi di Logger:

    1. La classe di logger si chiama **TestLogger** e viene utilizzata per tenere traccia dei test delle classi realizzate con un'output in console e su file txt

    2. La classe **TestMarkdownOutput** che viene utilizzata per leggere i risultati dei test secondo una formattazione specifica

5. Ogni classe creata avrà una sua classe di test:

    1. Test sui *parser*: **Test_IParserCsv** e **Test_IParserXls**. Utilizzando i file in ```/data/data_tests/IParsers/``` come verifica dei metodi e del funzionamento della classe

    2. Test sulle interfaccie lato db, ad esempio **Test_ICertificazioni**, in cui sono salvate le specifiche per ogni tipologia di informazioni sul database. Il test verifica che le informazioni siano sempre le stesse e che funzionino i metodi dedicati. **TODO:** costruire un file di config con le specifiche per ogni tabella

    3. Test sulle classi di Data Provider, ad esempio **Test_Accredia**, utilizzando un file fonte costruito per poter verificare che i metodi funzionino

    4. Test di certificazione in cui si verifica che i metodi delle classi Data Provider siano superati dato il vero file fonte come input

    