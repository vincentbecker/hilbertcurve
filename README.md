# hilbertcurve
A simple python script to create a turtle graphic drawing a hilbert curve

The python script `hilbert_curve.py` creates a turtle graphic a space-filling Hilbert curve. The user can adjust the recursion depth by carying the parameter `n`. In contrast to a normal Hilbert curve, the created curves contain areas of different density, which are generated randomly. This behaviour can be controlled by the function `_finish` (either adjusting the randomness or returning `false` in order to create a usual Hilbert curve corresponding to the parameter `n`). The gif below shows an example of a generated Hilbert curve. 

![Hilbert curve with random density](random_hilbert_with_turtle.gif "Hilbert curve with random density")
