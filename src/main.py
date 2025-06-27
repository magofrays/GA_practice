import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "include"))

from geneticAlgorithm import geneticAlgorithm
from gui import App

if __name__ == '__main__':
    a = App()
    a.run()

