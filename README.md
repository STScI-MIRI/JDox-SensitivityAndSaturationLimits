# JDox-Values

This repository contains code to produce MIRI sensitivity and saturation limit plots for JDox, based on Pandeia calculations. The input for the code are data tables produced using the Pandeia ETC engine by K. Pontoppidan for the following modes/settings:

* point source sensitivities for MIRI imager, LRS (slit and slitless), MRS (continuum and line)
* extended source sensitivities for MIRI imager and MRS (continuum and line)

### Input files

* miri_imaging_sensitivity_extended.npz
* miri_mrs_sensitivity_extended.npz
* miri_mrs_sensitivity_updated.npz
* miri_lrs_sensitivity_updated.npz
* miri_imaging_sensitivity_updated.npz

These files were last updated using **ETC v. 1.2**.

### Input file structure

The data files are in .npz format, which can easily be read in with the numpy.load() function, e.g.:

```python
import numpy as np
f = 'miri_imaging_sensitivity_updated.npz'
sens = np.load(f)
```

Column headers can be inspected using the .keys() method, e.g.

```
sens.keys()
['wavelengths', 'sns', 'lim_fluxes', 'sat_limits', 'configs']
```

### Authors & Maintainers   

Contributors to this code:

* Katie Murray (kmurray@stsci.edu)
* Sarah Kendrew (sarah.kendrew@esa.int)

The code will be maintained by the MIRI branch. 

