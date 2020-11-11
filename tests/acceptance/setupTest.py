from sys import path
from pathlib import Path
path = Path().absolute()
if not list(filter(lambda x: "innovation_intelligence" in x, path)):
    # innovation_intelligence dir (path/../..)
    path.append(path.parents[1])
