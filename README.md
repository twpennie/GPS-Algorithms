# GPS-Algorithms
representation of path finding algorithms (Djikstra / Prim)


 The weight I will be using is the distance between cities along roads, the data for which I got from
 google maps.


                                           ascii art of my graph:

                                                  Boston
                                                /       \ 
                                      103.3 mi /         \ 106.9 mi
                                              /   51.4 mi \
                                         Hartford ------ New London
                                        /      \               / 
                               116.3 mi/        \ 38.9 mi     / 47.8 mi
                                      / 80.7 mi  \           /
                                 N.Y.C ----------- New Haven
                                /     \
                       20.1 mi /       \ 25.8 mi
                              / 53.6 mi \
                        Maplewood ------ Garden City


These nodes are added manually in GraphTest.py

TODO:
- create GUI for adding/removing nodes
- create animation to show path finding
- allow user to create roadblocks and block off certain edges
