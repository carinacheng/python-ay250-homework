Instructions for re-producing "hw_4_assignment.ipynb":
    - Start up an ipycluster: $ ipycluster start -n 4
    - Then executing the notebook cell by cell should work

Specs of my Laptop: 
    - 2017 Macbook Pro with 2.5 GHz Intel Core i7, 2 "cores"

Explanation of plot:
    - Simple Serial: The execution time scales roughly linearly with the number of darts thrown, as expected. There is some small overhead time for a small number of darts, but then the simulation rate stays constant.
    - Multiprocessing: The execution time is roughly constant until ~10^5 darts, and then increases linearly. The two behaviors describe different regimes - one dominated by overhead costs (relatively slow execution times) and one where the large number of darts allows parallelization to become more effective than the serial version.
    - IPcluster: The behavior is similar to that of multiprocessing, with execution times being slightly faster, possibly due to 4 IPython engines (instead of 2 "cores").
