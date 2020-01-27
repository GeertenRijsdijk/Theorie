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

### Usage
To run the code
    python main.py <path with filename> <amount of houses> <algorithm>
runs the wijk_3.csv file with 20 houses with the greedy algorithm.
The different algorithms that can be run are:
    - r: random
    - g: greedy
    - h: hillclimber
    - s: Simulated Annealing
So for example:
    python main.py ./wijken/wijk_3.csv 20 g

To run the visualization:
    python visualize_csv.py <path with filename>
so for example:
    python visualize_csv.py results/wijk_1_20.csv

### Structure

The following list describes the file structure of the project:

- **/main.py**: the file used to run the algorithms.
- **/visualize_csv.py** the file used to visualize the result csv files
- **/code**: contains all code of the project.
  - **/code/algorithms**: contains code for the different algorithms.
    - **/code/algorithms/random.py**: contains code for the random algorithm.
    - **/code/algorithms/greedy.py**: contains code for the greedy algorithm.
    - **/code/algorithms/hillclimb.py**: contains code for the hillclimber algorithm.
    - **/code/algorithms/simann.py**: contains code for the simulated annealing algorithm.
  - **/code/classes**: contains code for the classes of the project.
    - **/code/classes/grid_class.py**: contains code for the Grid class.
  - **/code/visualize.py**: contains code for the visualization of the project.
  - **/code/output.py**: contains code for the writing of results to csv.
- **/data**: contains the data of the layouts of the projects.

## Authors
* Geerten Rijsdijk
* Wisse Bemelman
* Michael de Jong
