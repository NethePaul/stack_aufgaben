
Diese Anleitung ist zur Übersetzung von allen Fragen im gesamten Kurs von Deutsch zu Mutlilang mit Deutsch und Englisch.

Vorraussetzungen
Der Moodle Kurs muss zu Beginn vollständig in Deutsch sein, bzw. noch keine Multilang Tags enthalten.

Limitationen
Text in CAS Feldern (Felder für Maxima code) (zb. bei Multiple-Choice-Fragen) erscheint nicht in der .csv Datei und muss manuell übersetzt werden, wie zb. "[[lang code='de']]Beispiel[[/lang]][[lang code='en']]Example[[\lang]]"
Quizzes müssen zuletzt manuell aktualisiert oder neu-erstellt werden, sodass sie die übersetzten Fragen verwenden anstelle von den alten nicht-übersetzten.

1. Notwendige Software
Installiere ein Programm zum Bearbeiten von .csv Datein
 zb. Libreoffice oder Excel

Installiere Python und pip
 In Windows:
  Der Installer kann von der Webseite heruntergeladen werden:  https://www.python.org/downloads/windows/
  Alternativ kann Python auch mit den Microsoft Store installiert werden.
  Beide Varianten sollten auch pip mit beinhalten.
  Für mehr Info siehe:  https://learn.microsoft.com/de-de/windows/python/beginner
  Es kann sein, dass die Pfäde, unter dem Python und pip installiert sind, manuell zu der "PATH" Enviournment Variable hinzugefühgt werden müssen.
   Python ist standardmäßig unter "%ProgramFiles%\Python X.Y" oder "%ProgramFiles(x86)%\Python X.Y" oder "%LocalAppData%\Programs\Python\PythonXY" oder "%LocalAppData%\Programs\Python\PythonXY-32" oder "%LocalAppData%\Programs\Python\PythonXY-64" installiert.  (ersetze X.Y durch die installierte Python version)
   Um PATH zu ändern:
    Öffne regedit.exe
    Navigiere zu: "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
    Wenn der Wert von PATH bereits den Pfad zur Python Installation (zb. "C:\Program Files\Python312\") enthält muss es nicht mehr hinzugefügt werden.
    Ansonsten füge hinten an den Wert der Variable PATH ein ";" an und danach den Pfad zu der Python Installation.
     Danach füge hinten an den Wert der Variable PATH ein ";" an und danach den Pfad zu den "Script" Ordner in der Python Installation.
     Der Wert der PATH variable sollte danach ungefähr wie folgt aussehen: "%SystemRoot%\system32;%SystemRoot%;%SystemRoot%\system32\wbem;%SystemRoot%\system32\WindowsPowershell\v1.0;C:\Program Files\dotnet\;C:\Program Files\Python312\;C:\Program Files\Python312\Scripts\"
    
    
 In Linux und Mac kann Python und pip einfach mit den Package Manager bzw. App Store installiert werden.

 Validiere, dass das beides richtig installiert ist, indem Sie CMD, oder eine Shell im Terminal öffnen und den Befehl "python --version" und "pip --version" eingeben.
 Die Befehle sollten dann die installierten Versionen von Python und pip ausgeben.

Installiere lxml, und beautifulsoup4 mit pip
In Linux und Mac können manche von diesen auch mit den Package Manager bzw. App Store installiert werden.
In Linux und Mac kann es sein, dass man pipx anstelle von pip verwenden muss.
 Befehle:
 "pip install lxml"
 "pip install beautifulsoup4"
Installiere libretranslate:(nur für automatische Übersetzung notwendig) (Die Installation kann lange dauern)
 In Linux und Mac: "pipx install libretranslate"
 In Windows: Folge die Anleitung von  https://github.com/nuttolum/LibreOnWindows
  Alternativ in Windows:
   Installiere "WSL" wie nach  https://learn.microsoft.com/de-de/windows/wsl/install.
   Dann starte WSL mit den Befehl "wsl ~".
   Dann in WSL installiere pipx mit den Befehl "sudo apt install python-pipx".
   Dann installiere libretranslate in WSL mit den Befehl "pipx install libretranslate".
 

2. Export der Fragen aus Moodle
Navigiere zu den Moodle Kurs.
In der Top-bar, klicke auf das Zahnrad, dann im Menu klicke auf "Mehr".
Dann neben "Fragensammlung" klicke auf Export und wähle "Moodle-XML-Format" als Dateiformat und klicke "Fragen in Datei exportieren"
Es startet dann ein Download für die .xml Datei.
In Windows: aktiviere Dateinamenerweiterungen, wie nach:  https://support.microsoft.com/de-de/windows/allgemeine-dateierweiterungen-in-windows-da4a4430-8e76-89c5-59f7-1cdbbc75cb01

3. Vorbereitung für die Übersetzung
Erstelle ein Ordner für die Übersetzung. 
Kopiere die .xml Datei in den Ordner.
Kopiere die Python-scripte(.py Datein) von  https://github.com/NethePaul/stack_aufgaben/tree/main/python in den Ordner.
Navigiere zu den Ordner in CMD oder in einer Shell mithilfe von den "cd" Befehl, oder den File Explorer. (Alle Befehle müssen in diesen Ordner ausgeführt werden.)
 Im File Explorer: Öffne den Ordner, und dann mit ein rechts-Klick im Ordner öffnet sich ein Menu, in den Menu klicke "Im Terminal öffnen" oder etwas ähnliches.
 In CMD:
  Mit den "dir" Befehl können alle Datein und Ordner(als <DIR> markiert) gelistet werden.
 In einer POSIX-compliant Shell (zb. Windows Powershell, oder Bash)
  Mit den "ls" Befehl können alle Datein und Ordner gelistet werden.
  Mit den "ls -d" Befehl können alle Ordner gelistet werden.
 Generell:
  Mit "cd [Name des Ordner]" kann zu den Ordner navigiert werden.
  Mit "cd .." kann man zu den Obergeordneten obergeordneten Ordner zurück navigieren.
Erstelle die .csv und .xml.template datein mit den Befehl "python xml2csv.py"
Achtung: In allen weiteren Schritten wird eine wiederholte Ausführung eines der xml2csv Skripten die bisherigen Übersetzungen in der .csv Datei löschen!

4. Übersetzung

4.1 (nur für die automatische Überestzung)
Öffne ein 2. Terminal/CMD und gebe dort den Befehl "libretranslate --load-only de,en"
In Windows: Wenn libretranslate unter WSL installiert ist, muss der Befehl in WSL ausgeführt werden.
Warte bis der Befehl die Ausgabe "Running on http://127.0.0.1:5000" in den Terminal schreibt.
Beende den Befehl nicht. Lass das Terminal/CMD im Hintergrund offen.

Gebe den Befehl "python autotranslate.py" ein. (Der Befehl kann mehrere Stunden brauchen bei vollständiger CPU-Auslastung)
Wenn der Befehl unterbrochen wird, kann die Übersetzung weitergeführt werden duch einer wiederholten Eingabe des Befehls, während der libretranslate Befehl im Hintergrund läuft.
Sobald der Befehl endet kann das 2. Terminal/CMD mit den libretranslate Befehl geschlossen werden.
Automatische Übersetzung kann häufig Fehler machen, selbst wenn der vorherige Befehl ohne Fehlermeldungen endete, und besonders mit Fachsprache und wenn Text mit LaTeX oder Maxima Code unterbrochen ist.
Daher ist es wichtig die .csv Datei vollständig manuell nach Fehlern zu durchsuchen.
Achtung: Wenn text innerhalb von Mathematischen Ausdrücken in LaTeX (zb. "\(\text{Beispiel}\)") oder in Maxima Code (zb. "{@'Beispiel'@}") steht, wird es nicht automatisch übersetzt.

4.2
Öffnen sie die .csv Datei
Wenn Sie bei den Öffnen gefragt werden, setzen Sie den Delimiter bzw. Trennzeichen auf ein Komma(",") und nichts anderes.
Sie sollten dann eine Tabelle mit drei Spalten sehen.
Im Header der Tabelle steht links "Nummer", mittig "de", und rechts "en".
Verändern Sie an der "Nummer" Spalte und dem Header nichts.
Dann muss man die "en" Spalte bearbeiten bis in jeder Zeile die "en" Spalte die Übersetzung der "de" Spalte ist.

Wenn Sie Excel verwenden, geben Sie den Befehl "python csv4excel.py" ein.
Öffnen Sie die .csv Datei
Wenn Sie bei den Öffnen gefragt werden, setzen Sie den Delimiter bzw. Trennzeichen auf ein Komma(",") und nichts anderes.
Sie sollten dann eine Tabelle mit drei Spalten sehen.
Im Header der Tabelle steht links "Nummer", mittig "de", und rechts "en".
Verändern Sie an der "Nummer" Spalte und dem Header nichts.
Dann muss man die "en" Spalte bearbeiten bis in jeder Zeile die "en" Spalte die Übersetzung der "de" Spalte ist.

5. Import in Moodle
Geben Sie den Befehl "python fix_template.py" ein.
Geben Sie den Befehl "python csv2xml.py" ein.
Es wird dann eine neue _new.xml Datei im Ordner erstellt.
Dann in Moodle, im selben Menu wo "Export" stand neben "Fragensammlung", klicke auf "Import".
Wähle "Moodle-XML-Format" als Dateiformat und die _new.xml Datei als Datei.
Dann klicke Import.

Die Frage werden in einer Neuen Unterkategorie namens "übersetzt" importiert.
Davon abgesehen bleibt die Kategorienstruktur erhalten.
Die alten Fragen bleiben unverändert.

6. Aktualisiere Quizzes und CAS-Felder
Alle Quizze werden danach noch die alten Fragen referenzieren.
Daher müssen entweder alle Quizzes neu erstellt werden mit den neuen Fragen.
Oder von allen Quizzen müssen alle Fragen entfernt werden und mit den übersetzten Fragen ersetzt werden.
Text unter "Questionvariables" oder "Aufgabenvariablen" wird nicht in der .csv Datei zum Übersetzen auftauchen. Daher muss der Text noch manuell übersetzt werden.
Hierfür kann die Maxima-Funktion " tr(de,en):=castext("[[lang code='de']]{@de@}[[/lang]][[lang code='en']]{@en@}[[/lang]]"); "  hilfreich sein. Sie wird wie folt aufgerufen:  " tr("Beispiel","Example") ".

7. (optional) Hochladen der Fragen in Git
zum Teilen mit anderen Universitäten
Geben Sie den Befehl "python prettyfy_cli [Name der _new.csv Datei]" und danach "python split_exported_xml [Name der _new.csv Datei]" ein.
Es sollte dann ein neuer Ordner namens "separate_questions" erscheinen mit allen Fragen als separate .xml Datein.
Diese .xml Datein können dann in ein Git Repository hochgeladen werden.





