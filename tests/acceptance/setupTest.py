from sys import path
from pathlib import Path
wrkdir = Path().absolute()
if not list(filter(lambda x: "innovation_intelligence" in x, path)):
    # innovation_intelligence dir (path/../..)
    path.append(wrkdir.parents[1])
