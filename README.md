# Amstelhaege Programmeertheorie
(dutch introduction)
Na jarenlang getouwtrek is de knoop eindelijk doorgehakt: er komt een nieuwe woonwijk in de Duivendrechtse polder, net ten noorden van Ouderkerk aan de Amstel. De huisjes zijn bedoeld voor het midden- en bovensegment van de markt, met name expats en hoogopgeleide werknemers actief op de Amsterdamse Zuidas.

Omdat de Duivenderechtse polder ooit beschermd natuurgebied was, is de compromis dat er alleen lage vrijstaande woningen komen, om zo toch het landelijk karakter te behouden. Dit, gecombineerd met een aantal strenge restricties ten aanzien van woningaanbod en het oppervlaktewater, maakt het een planologisch uitdagende klus. De gemeente overweegt drie varianten: de 20-huizenvariant, de 40-huizenvariant en de 60-huizenvariant. Er wordt aangenomen dat een huis meer waard wordt naarmate de vrijstand toeneemt, de rekenpercentages zijn per huistype vastgesteld.

## Aan de slag

### Requirements
This code is written in python 3.7+. The requirements.txt file contains all packages needed to run the code. These can be installed using pip with the following commands:

    pip install -r requirements.txt

Or using conda:

    conda install --file requirements.txt

### Use
To run the code
    python main.py <path with filename> <amount of houses> <algorithm>
So for example:
    python main.py ./wijken/wijk_3.csv 20 g
runs the wijk_3.csv file with 20 houses with the greedy algorithm.
The different algorithms can be found in the main.py file.

### Structure
* **algorithms.py**: contains code for the different algorithms
* **visualize.py**: contains code to visualize the house placement
* **wijken/**: contains different csv file with the placement of water

## Authors
* Geerten Rijsdijk
* Wisse Bemelman
* Michael de Jong
