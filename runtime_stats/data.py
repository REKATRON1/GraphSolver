
from dataclasses import dataclass

from .algorithmus_data import AlgorithmusData
from .visual_data import VisualData
from .input_data import InputData

@dataclass
class Data:
    visual_data: VisualData = None
    algo_data: AlgorithmusData = None
    input_data: InputData = None

data: Data = Data()

def update_data(ndata: Data) -> None:
    data.visual_data = ndata.visual_data

def update_visual_data(vdata: VisualData) -> None:
    data.visual_data = vdata

def update_algo_data(adata: AlgorithmusData) -> None:
    data.algo_data = adata

def update_input_data(idata: InputData) -> None:
    data.input_data = idata