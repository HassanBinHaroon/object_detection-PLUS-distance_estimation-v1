# import all the packages
import numpy as np
import seaborn as sns
from pylab import rcParams
import utils

display = utils.notebook_init()

# set defualts
sns.set(style='whitegrid', palette='muted', font_scale=1.2)
rcParams['figure.figsize'] = 16, 10
np.random.seed(42)