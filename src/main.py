import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "include"))
sys.path.append(str(Path(__file__).parent / "include/GUI"))

from geneticAlgorithm import geneticAlgorithm
from app import App

if __name__ == '__main__':
    a = App()
    a.run()

