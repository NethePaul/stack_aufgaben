Warnung:
 Die Python-Skripte sind noch nicht bereit.




Diese Anleitung ist zur Übersetzung von allen Fragen im gesamten Kurs von Deutsch zu Mutlilang mit Deutsch und Englisch.

Vorraussetzungen
Der Moodle Kurs muss zu Beginn vollständig in Deutsch sein, bzw. noch keine Multilang Tags enthalten.

Limitationen
Text in CAS Feldern (Felder für Maxima code) (zb. bei Multiple-Choice-Fragen) erscheint nicht in der .csv Datei und muss manuell übersetzt werden, wie zb. "[[lang code='de']]Beispiel[[/lang]][[lang code='en']]Example[[\lang]]"
Quizzes müssen zuletzt manuell aktualisiert oder neu-erstellt werden, sodass sie die übersetzten Fragen verwenden anstelle von den alten nicht-übersetzten.

1. Notwendige Software
Installiere ein Programm zum Bearbeiten von .csv Datein
 zb. Libreoffice oder Excel
Installiere Python
 In Windows:
  Der Installer kann von der Webseite heruntergeladen werden:  https://www.python.org/downloads/windows/
  Alternativ kann Python auch mit den Microsoft Store installiert werden.
  Für mehr Info siehe:  https://learn.microsoft.com/de-de/windows/python/beginner
  Unter Umständen muss der Pfad, unter dem Python installiert ist, manuell zu der "PATH" Enviournment Variable hinzugefühgt werden.
 In Linux und Mac kann Python einfach mit den Package Manager bzw. App Store installiert werden.

 Validiere, dass Python richtig installiert ist, indem Sie CMD, oder eine Shell im Terminal öffnen und den Befehl "python --version" eingeben.
 Der Befehl sollte dann die installierte Version von Python ausgeben oder ein Fehler verursachen wenn Python nicht installiert ist.

2. Export der Fragen aus Moodle
Navigiere zu den Moodle Kurs.
In der Top-bar, klicke auf das Zahnrad, dann im Menu klicke auf "Mehr".
Dann neben "Fragensammlung" klicke auf Export und wähle "Moodle-XML-Format" als Dateiformat und klicke "Fragen in Datei exportieren"
Es startet dann ein Download für die .xml Datei.

3. Vorbereitung für die Übersetzung
Erstelle ein Ordner für die Übersetzung. 
Kopiere die .xml Datei in den Ordner.
Kopiere die Python-scripte(.py Datein) von  https://github.com/NethePaul/stack_aufgaben/python in den Ordner.
Navigiere zu den Ordner in CMD oder in einer Shell mithilfe von den "cd" Befehl. (Alle Befehle müssen in diesen Ordner ausgeführt werden.)
 In CMD:
  Mit den "dir" Befehl können alle Datein und Ordner(als <DIR> markiert) gelistet werden.
 In einer POSIX-compliant Shell (zb. Windows Powershell, oder Bash)
  Mit den "ls" Befehl können alle Datein und Ordner gelistet werden.
  Mit den "ls -d" Befehl können alle Ordner gelistet werden.
 Generell:
  Mit "cd [Name des Ordner]" kann zu den Ordner navigiert werden.
  Mit "cd .." kann man zu den Obergeordneten obergeordneten Ordner zurück navigieren.
Erstelle die .csv und .xml.template datein mit einen der Beiden folgenden Befehlen:
"python xml2csv.py" (ohne automatischer Übersetzung) oder 
"pyhton xml2csv_with_autotranslate.py" (mit automatischer Übersetzung).
Wenn Sie versehentlich den Falschen der beiden Befehle ausgeführt haben oder Sie sich Ihre Meinung geändert haben und lieber den anderen Befehl ausführen wollen, können Sie in diesen Schritt noch einfach den anderen ausführen ohne Konsequenzen.
Achtung: In allen weiteren Schritten wird eine wiederholte Ausführung eines der xml2csv Skripten die bisherigen Übersetzungen in der .csv Datei löschen!

4. Übersetzung
Öffnen sie die .csv Datei
Wenn Sie bei den Öffnen gefragt werden, setzen Sie den Delimiter bzw. Trennzeichen auf ein Komma(",") und nichts anderes.
Sie sollten dann eine Tabelle mit drei Spalten sehen.
Im Header der Tabelle steht links "Nummer", mittig "de", und rechts "en".
Verändern Sie an der "Nummer" Spalte und dem Header nichts.
Dann muss man die "en" Spalte bearbeiten bis in jeder Zeile die "en" Spalte die Übersetzung der "de" Spalte ist.

4.1 ohne automatischer Übersetzung
Es kann sich empfehlen die "de" Spalte (ausser Header) zu Beginn in die "en" Spalte zu kopieren.
Mit Search&Replace in der "en" Spalte kann man häufig wiederholte Ausdrücke alle auf einmal übersetzen.

4.2 mit automatischer Überestzung
Automatische Übersetzung kann häufig Fehler machen, besonders mit Fachsprache und wenn Text mit LaTeX oder Maxima Code unterbrochen ist.
Daher ist es wichtig die .csv Datei vollständig manuell nach Fehlern zu durchsuchen.
Achtung: Wenn text innerhalb von Mathematischen Ausdrücken in LaTeX (zb. "\(\text{Beispiel}\)") oder in Maxima Code (zb. "{@'Beispiel'@}") steht, wird es nicht automatisch übersetzt.

5. Import in Moodle
Gebe den Befehl "python csv2xml.py" ein.
Es wird dann eine neue _new.xml Datei im Ordner erstellt.
Dann in Moodle, im selben Menu wo "Export" stand neben "Fragensammlung", klicke auf "Import".
Wähle "Moodle-XML-Format" als Dateiformat und die _new.xml Datei als Datei.
Dann klicke Import.

Die Frage werden in einer Neuen Unterkategorie namens "übersetzt" importiert.
Davon abgesehen bleibt die Kategorienstruktur erhalten.
Die alten Fragen bleiben unverändert.

6. Aktualisiere Quizzes
Alle Quizze werden danach noch die alten Fragen referenzieren.
Daher müssen entweder alle Quizzes neu erstellt werden mit den neuen Fragen.
Oder von allen Quizzen müssen alle Fragen entfernt werden und mit den übersetzten Fragen ersetzt werden.

7. (optional) Hochladen der Fragen in Git
zum Teilen mit anderen Universitäten
Gebe den Befehl "python prettyfy_cli [Name der _new.csv Datei]" und danach "python split_exported_xml [Name der _new.csv Datei]" ein.
Es sollte dann ein neuer Ordner namens "separate_questions" erscheinen mit allen Fragen als separate .xml Datein.
Diese .xml Datein können dann in ein Git Repository hochgeladen werden.





