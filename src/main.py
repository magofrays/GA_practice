import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "include"))

from geneticAlgorithm import geneticAlgorithm

if __name__ == '__main__':
    a = geneticAlgorithm()
    a.read_tasks()
    a.create_individuals()
    a.do_selection()
    

