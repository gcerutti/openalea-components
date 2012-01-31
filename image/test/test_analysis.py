from openalea.image.all import *
from numpy import mean
from time import time


def show_result(txt,function):
    ctime = time()
    res = function()
    ctime = time() - ctime
    print txt,':',res,'(%f sec.)'%ctime
    return res

def time_result(txt,function):
    ctime = time()
    res = function()
    ctime = time() - ctime
    print txt,'(%f sec.)'%ctime
    return res

def test_on_segmentation():
    im = time_result('Read image',lambda : read_inrimage("segmentation.inr.gz"))
    analysis = SpatialImageAnalysis(im)
    show_result('Nb labels',analysis.nb_labels)
    time_result('Bounding Box',analysis.boundingbox)
    show_result('Mean volume',lambda : mean(analysis.volume()))
    time_result('Center of mass',analysis.center_of_mass)
    show_result('Neigbbors',lambda: len(analysis.neighbors(range(10,20))))
    show_result('All Neigbbors',lambda: len(analysis.neighbors()))
    show_result('All Wall Surface',lambda: len(analysis.all_wall_surfaces()))

    
def test_on_simple_array():
    import numpy as np
    a = np.array([[1, 2, 7, 7, 1, 1],
                  [1, 6, 5, 7, 3, 3],
                  [2, 2, 1, 7, 3, 3],
                  [1, 1, 1, 4, 1, 1]])
    print a.shape
    
    from openalea.image.algo.analysis import SpatialImageAnalysis
    analysis = SpatialImageAnalysis(a)

    res = analysis.neighbors(7)
    assert res == { 7:[1, 2, 3, 4, 5]}

    res = analysis.neighbors([7,2])
    assert res == { 7: [1, 2, 3, 4, 5], 2: [1, 6, 7] }

    neighbors = analysis.neighbors()
    assert neighbors == { 1: [2, 3, 4, 5, 6, 7], 2: [1, 6, 7], 3: [1, 7], 4: [1, 7], 5: [1, 6, 7], 6: [1, 2, 5], 7: [1, 2, 3, 4, 5] }

    assert analysis.volume(7) == 4.0
    
    assert analysis.volume([7,2]) == [4.0, 3.0]
    
    assert analysis.volume() == [10.0, 3.0, 4.0, 1.0, 1.0, 1.0, 4.0]
    
    print analysis.center_of_mass(7)
    assert analysis.center_of_mass(7) == [0.75, 2.75, 0.0]
    
    assert analysis.center_of_mass([7,2]) == [[0.75, 2.75, 0.0], [1.3333333333333333, 0.66666666666666663, 0.0]]
    
    assert analysis.center_of_mass() == [[1.8, 2.2999999999999998, 0.0],[1.3333333333333333, 0.66666666666666663, 0.0], [1.5, 4.5, 0.0], [3.0, 3.0, 0.0], [1.0, 2.0, 0.0], [1.0, 1.0, 0.0], [0.75, 2.75, 0.0]]
     
    assert analysis.wall_surface(7,2) ==  1
    
    walls = analysis.all_wall_surfaces() 
    a = list(walls.items())
    a.sort()
    print a
    assert  walls == {(1, 2): 5.0, (1, 3): 4.0, (1, 4): 2.0, (1, 5): 1.0, (1, 6): 1.0, (1, 7): 2.0, (2, 6): 2.0, (2, 7): 1.0, (3, 7): 2, (4, 7): 1, (5, 6): 1.0, (5, 7): 2.0 }
    # (1, 2): 4.0 - 5.0,  (1, 4): 1.0 - 2.0, (2, 6): 1.0 - 2.0, 
    print 'ok'
    
    
if __name__ == '__main__':
    #test_on_segmentation()
    test_on_simple_array()
    
