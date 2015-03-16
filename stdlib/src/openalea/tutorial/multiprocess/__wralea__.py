
# This file has been generated at Wed Sep 26 17:31:46 2012

from openalea.core import *


__name__ = 'openalea.tutorial.multiprocess'

__editable__ = True
__description__ = ''
__license__ = ''
__url__ = ''
__alias__ = []
__version__ = ''
__authors__ = ''
__institutes__ = ''
__icon__ = ''


__all__ = ['_77042384', '_77042512', '_77042448']



_77042384 = CompositeNodeFactory(name='tutorial parallel_map',
                             description='',
                             category='Unclassified',
                             doc='',
                             inputs=[],
                             outputs=[],
                             elt_factory={  2: ('openalea.multiprocessing', 'parallel map'),
   3: ('openalea.function operator', 'function'),
   4: ('openalea.python method', 'range'),
   5: ('openalea.multiprocessing', 'parallel map'),
   6: ('openalea.flow control', 'X'),
   7: ('openalea.python method', 'range'),
   8: ('openalea.math', '*'),
   9: ('openalea.data structure', 'int'),
   10: ('openalea.flow control', 'annotation'),
   11: ('openalea.flow control', 'annotation')},
                             elt_connections={  33261544: (6, 0, 8, 0),
   33261568: (3, 0, 2, 0),
   33261592: (7, 0, 5, 1),
   33261616: (4, 0, 2, 1),
   33261640: (8, 0, 5, 0),
   33261664: (9, 0, 8, 1)},
                             elt_data={  2: {  'block': False,
         'caption': 'parallel map',
         'delay': 0,
         'factory': '<openalea.core.node.NodeFactory object at 0x4e6c490> : "parallel map"',
         'hide': True,
         'id': 2,
         'is_in_error_state': False,
         'is_user_application': False,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': -195.0,
         'posy': 65.0,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   3: {  'block': False,
         'caption': 'f',
         'delay': 0,
         'factory': '<openalea.core.node.NodeFactory object at 0x5b3c610> : "function"',
         'hide': True,
         'id': 3,
         'is_in_error_state': False,
         'is_user_application': False,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': -237.95866700480522,
         'posy': -52.79412636388825,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   4: {  'block': False,
         'caption': 'range',
         'delay': 0,
         'factory': '<openalea.core.node.NodeFactory object at 0x75ba450> : "range"',
         'hide': True,
         'id': 4,
         'is_in_error_state': False,
         'is_user_application': False,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': -79.0,
         'posy': -54.0,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   5: {  'block': False,
         'caption': 'parallel map',
         'delay': 0,
         'factory': '<openalea.core.node.NodeFactory object at 0x4e6c490> : "parallel map"',
         'hide': True,
         'id': 5,
         'is_in_error_state': False,
         'is_user_application': False,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': 108.42564121115043,
         'posy': 75.9446333678437,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   6: {  'block': False,
         'caption': 'X0',
         'delay': 0,
         'factory': '<openalea.core.node.NodeFactory object at 0x8c7f1d0> : "X"',
         'hide': True,
         'id': 6,
         'is_in_error_state': False,
         'is_user_application': False,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': 65.91727369449718,
         'posy': -51.447628249363646,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   7: {  'block': False,
         'caption': 'range',
         'delay': 0,
         'factory': '<openalea.core.node.NodeFactory object at 0x75ba450> : "range"',
         'hide': True,
         'id': 7,
         'is_in_error_state': False,
         'is_user_application': False,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': 221.2101644455652,
         'posy': -43.859235823552595,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   8: {  'block': False,
         'caption': '*',
         'delay': 0,
         'factory': '<openalea.core.node.NodeFactory object at 0x5f17e10> : "*"',
         'hide': True,
         'id': 8,
         'is_in_error_state': False,
         'is_user_application': False,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': 84.40626509661223,
         'posy': 8.038691913963063,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   9: {  'block': False,
         'caption': '2',
         'delay': 0,
         'factory': '<openalea.core.node.NodeFactory object at 0x487a450> : "int"',
         'hide': True,
         'id': 9,
         'is_in_error_state': False,
         'is_user_application': False,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': 124.59972466642756,
         'posy': -49.839889866571035,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   10: {  'factory': '<openalea.core.node.NodeFactory object at 0x8c713d0> : "annotation"',
          'id': 10,
          'posx': -212.26618858133065,
          'posy': 133.05465967171213,
          'txt': u'launch  in a shell:\nipcluster start --n=2 '},
   11: {  'factory': '<openalea.core.node.NodeFactory object at 0x8c713d0> : "annotation"',
          'id': 11,
          'posx': 100.95587017892555,
          'posy': 143.40910789519168,
          'txt': u'Error raised:\nFunctionType'},
   '__in__': {  'block': False,
                'caption': 'In',
                'delay': 0,
                'hide': True,
                'id': 0,
                'is_in_error_state': False,
                'is_user_application': False,
                'lazy': True,
                'port_hide_changed': set(),
                'posx': 0,
                'posy': 0,
                'priority': 0,
                'use_user_color': True,
                'user_application': None,
                'user_color': None},
   '__out__': {  'block': False,
                 'caption': 'Out',
                 'delay': 0,
                 'hide': True,
                 'id': 1,
                 'is_in_error_state': False,
                 'is_user_application': False,
                 'lazy': True,
                 'port_hide_changed': set(),
                 'posx': 0,
                 'posy': 0,
                 'priority': 0,
                 'use_user_color': True,
                 'user_application': None,
                 'user_color': None}},
                             elt_value={  2: [],
   3: [(0, "'def f(x):\\n  return x**2'")],
   4: [(0, '0'), (1, '100'), (2, '1')],
   5: [],
   6: [(0, "'x'")],
   7: [(0, '0'), (1, '100'), (2, '1')],
   8: [],
   9: [(0, '2')],
   10: [],
   11: [],
   '__in__': [],
   '__out__': []},
                             elt_ad_hoc={  2: {'position': [-195.0, 65.0], 'userColor': None, 'useUserColor': False},
   3: {'position': [-237.95866700480522, -52.79412636388825], 'userColor': None, 'useUserColor': False},
   4: {'position': [-79.0, -54.0], 'userColor': None, 'useUserColor': False},
   5: {'position': [108.42564121115043, 75.9446333678437], 'userColor': None, 'useUserColor': False},
   6: {'position': [65.91727369449718, -51.447628249363646], 'userColor': None, 'useUserColor': False},
   7: {'position': [221.2101644455652, -43.859235823552595], 'userColor': None, 'useUserColor': False},
   8: {'position': [84.40626509661223, 8.038691913963063], 'userColor': None, 'useUserColor': False},
   9: {'position': [124.59972466642756, -49.839889866571035], 'userColor': None, 'useUserColor': False},
   10: {'visualStyle': 0, 'position': [-212.26618858133065, 133.05465967171213], 'color': None, 'text': u'launch  in a shell:\nipcluster start --n=2 ', 'textColor': None, 'rectP2': (-1, -1)},
   11: {'visualStyle': 0, 'position': [100.95587017892555, 143.40910789519168], 'color': None, 'text': u'Error raised:\nFunctionType', 'textColor': None, 'rectP2': (-1, -1)},
   '__in__': {'position': [0, 0], 'userColor': None, 'useUserColor': True},
   '__out__': {'position': [0, 0], 'userColor': None, 'useUserColor': True}},
                             lazy=True,
                             eval_algo='LambdaEvaluation',
                             )




_77042512 = CompositeNodeFactory(name='tutorial pmap',
                             description='',
                             category='Unclassified',
                             doc='',
                             inputs=[],
                             outputs=[],
                             elt_factory={  2: ('openalea.data structure', 'int'),
   3: ('openalea.data structure.string', 'string'),
   4: ('openalea.data structure.string', 'string'),
   5: ('openalea.multiprocessing', 'pmap'),
   6: ('openalea.flow control', 'X'),
   7: ('openalea.python method', 'range'),
   8: ('openalea.math', '*'),
   9: ('openalea.data structure', 'int'),
   10: ('openalea.data structure', 'int'),
   11: ('openalea.data structure', 'int'),
   12: ('openalea.flow control', 'X'),
   13: ('openalea.python method', 'range'),
   14: ('openalea.math', '*'),
   15: ('openalea.data structure', 'int'),
   16: ('openalea.function operator', 'map'),
   17: ('openalea.flow control', 'annotation'),
   18: ('openalea.flow control', 'annotation')},
                             elt_connections={  151772524: (2, 0, 7, 1),
   151772536: (16, 0, 3, 0),
   151772548: (14, 0, 16, 0),
   151772560: (12, 0, 14, 0),
   151772572: (10, 0, 5, 2),
   151772584: (9, 0, 8, 1),
   151772596: (7, 0, 5, 1),
   151772608: (6, 0, 8, 0),
   151772620: (8, 0, 5, 0),
   151772632: (11, 0, 13, 1),
   151772644: (15, 0, 14, 1),
   151772656: (5, 0, 4, 0),
   151772668: (13, 0, 16, 1)},
                             elt_data={  2: {  'block': False,
         'caption': '100',
         'delay': 0,
         'factory': '<openalea.core.node.NodeFactory object at 0xadf948c> : "int"',
         'hide': True,
         'id': 2,
         'is_in_error_state': False,
         'is_user_application': False,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': 172.9981227710845,
         'posy': -48.88660504735711,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   3: {  'block': False,
         'caption': "'[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130, 132, 134, 136, 138, 140, 142, 144, 146, 148, 150, 152, 154, 156, 158, 160, 162, 164, 166, 168, 170, 172, 174, 176, 178, 180, 182, 184, 186, 188, 190, 192, 194, 196, 198]'",
         'delay': 0,
         'factory': '<openalea.core.node.NodeFactory object at 0xae7ccac> : "string"',
         'hide': True,
         'id': 3,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': -160.17156572881132,
         'posy': 129.13296343982876,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   4: {  'block': False,
         'caption': "'[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130, 132, 134, 136, 138, 140, 142, 144, 146, 148, 150, 152, 154, 156, 158, 160, 162, 164, 166, 168, 170, 172, 174, 176, 178, 180, 182, 184, 186, 188, 190, 192, 194, 196, 198]'",
         'delay': 0,
         'factory': '<openalea.core.node.NodeFactory object at 0xae7ccac> : "string"',
         'hide': True,
         'id': 4,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': 108.45840363918109,
         'posy': 129.60405628020763,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   5: {  'block': False,
         'caption': 'pmap',
         'delay': 0,
         'factory': '<openalea.core.node.NodeFactory object at 0xae7c48c> : "pmap"',
         'hide': True,
         'id': 5,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': 149.32760800722573,
         'posy': 81.49698742220951,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   6: {  'block': False,
         'caption': 'X',
         'delay': 0,
         'factory': '<openalea.core.node.NodeFactory object at 0xac6788c> : "X"',
         'hide': True,
         'id': 6,
         'is_in_error_state': False,
         'is_user_application': False,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': 66.8594593752549,
         'posy': -46.265607005196216,
         'priority': 0,
         'use_user_color': True,
         'user_application': None,
         'user_color': 255},
   7: {  'block': False,
         'caption': 'range',
         'delay': 0,
         'factory': '<openalea.core.node.NodeFactory object at 0xae5c92c> : "range"',
         'hide': True,
         'id': 7,
         'is_in_error_state': False,
         'is_user_application': False,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': 167.03448780199665,
         'posy': 7.018790937363946,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   8: {  'block': False,
         'caption': '*',
         'delay': 0,
         'factory': '<openalea.core.node.NodeFactory object at 0xad69a2c> : "*"',
         'hide': True,
         'id': 8,
         'is_in_error_state': False,
         'is_user_application': False,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': 84.40626509661223,
         'posy': 8.038691913963063,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   9: {  'block': False,
         'caption': '2',
         'delay': 0,
         'factory': '<openalea.core.node.NodeFactory object at 0xadf948c> : "int"',
         'hide': True,
         'id': 9,
         'is_in_error_state': False,
         'is_user_application': False,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': 124.59972466642756,
         'posy': -49.839889866571035,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   10: {  'block': False,
          'caption': '4',
          'delay': 0,
          'factory': '<openalea.core.node.NodeFactory object at 0xadf948c> : "int"',
          'hide': True,
          'id': 10,
          'lazy': True,
          'port_hide_changed': set(),
          'posx': 265.92759819267144,
          'posy': 22.73777626362295,
          'priority': 0,
          'use_user_color': False,
          'user_application': None,
          'user_color': None},
   11: {  'block': False,
          'caption': '100',
          'delay': 0,
          'factory': '<openalea.core.node.NodeFactory object at 0xadf948c> : "int"',
          'hide': True,
          'id': 11,
          'is_in_error_state': False,
          'is_user_application': False,
          'lazy': True,
          'port_hide_changed': set(),
          'posx': -99.29353896789479,
          'posy': -44.64676948394739,
          'priority': 0,
          'use_user_color': False,
          'user_application': None,
          'user_color': None},
   12: {  'block': False,
          'caption': 'X',
          'delay': 0,
          'factory': '<openalea.core.node.NodeFactory object at 0xac6788c> : "X"',
          'hide': True,
          'id': 12,
          'is_in_error_state': False,
          'is_user_application': False,
          'lazy': True,
          'port_hide_changed': set(),
          'posx': -201.36337445169835,
          'posy': -39.49660757146181,
          'priority': 0,
          'use_user_color': True,
          'user_application': None,
          'user_color': 255},
   13: {  'block': False,
          'caption': 'range',
          'delay': 0,
          'factory': '<openalea.core.node.NodeFactory object at 0xae5c92c> : "range"',
          'hide': True,
          'id': 13,
          'is_in_error_state': False,
          'is_user_application': False,
          'lazy': True,
          'port_hide_changed': set(),
          'posx': -108.3656017826379,
          'posy': 11.95885058558213,
          'priority': 0,
          'use_user_color': False,
          'user_application': None,
          'user_color': None},
   14: {  'block': False,
          'caption': '*',
          'delay': 0,
          'factory': '<openalea.core.node.NodeFactory object at 0xad69a2c> : "*"',
          'hide': True,
          'id': 14,
          'is_in_error_state': False,
          'is_user_application': False,
          'lazy': True,
          'port_hide_changed': set(),
          'posx': -182.8743830495833,
          'posy': 14.336598507318584,
          'priority': 0,
          'use_user_color': False,
          'user_application': None,
          'user_color': None},
   15: {  'block': False,
          'caption': '2',
          'delay': 0,
          'factory': '<openalea.core.node.NodeFactory object at 0xadf948c> : "int"',
          'hide': True,
          'id': 15,
          'is_in_error_state': False,
          'is_user_application': False,
          'lazy': True,
          'port_hide_changed': set(),
          'posx': -142.68092347976796,
          'posy': -43.54198327321548,
          'priority': 0,
          'use_user_color': False,
          'user_application': None,
          'user_color': None},
   16: {  'block': False,
          'caption': 'map',
          'delay': 0,
          'factory': '<openalea.core.node.NodeFactory object at 0xae7c58c> : "map"',
          'hide': True,
          'id': 16,
          'lazy': True,
          'port_hide_changed': set(),
          'posx': -115.89305783249556,
          'posy': 82.43917310296723,
          'priority': 0,
          'use_user_color': False,
          'user_application': None,
          'user_color': None},
   17: {  'factory': '<openalea.core.node.NodeFactory object at 0xabd9a4c> : "annotation"',
          'id': 17,
          'posx': 29.678848943867948,
          'posy': -93.74747523539251,
          'txt': u'Parallel Map on 4 processors'},
   18: {  'factory': '<openalea.core.node.NodeFactory object at 0xac6728c> : "annotation"',
          'id': 18,
          'posx': -220.364398945261,
          'posy': -93.6404248833485,
          'txt': u'Map on a single processor'},
   '__in__': {  'block': False,
                'caption': 'In',
                'delay': 0,
                'hide': True,
                'id': 0,
                'is_in_error_state': False,
                'is_user_application': False,
                'lazy': True,
                'port_hide_changed': set(),
                'posx': 0,
                'posy': 0,
                'priority': 0,
                'use_user_color': True,
                'user_application': None,
                'user_color': None},
   '__out__': {  'block': False,
                 'caption': 'Out',
                 'delay': 0,
                 'hide': True,
                 'id': 1,
                 'is_in_error_state': False,
                 'is_user_application': False,
                 'lazy': True,
                 'port_hide_changed': set(),
                 'posx': 0,
                 'posy': 0,
                 'priority': 0,
                 'use_user_color': True,
                 'user_application': None,
                 'user_color': None}},
                             elt_value={  2: [(0, '100')],
   3: [],
   4: [],
   5: [],
   6: [(0, "'x'")],
   7: [(0, '0'), (2, '1')],
   8: [],
   9: [(0, '2')],
   10: [(0, '4')],
   11: [(0, '100')],
   12: [(0, "'x'")],
   13: [(0, '0'), (2, '1')],
   14: [],
   15: [(0, '2')],
   16: [],
   17: [],
   18: [],
   '__in__': [],
   '__out__': []},
                             elt_ad_hoc={  2: {  'position': [172.9981227710845, -48.88660504735711],
         'useUserColor': False,
         'userColor': None},
   3: {  'position': [-160.17156572881132, 129.13296343982876],
         'useUserColor': False,
         'userColor': None},
   4: {  'position': [108.45840363918109, 129.60405628020763],
         'useUserColor': False,
         'userColor': None},
   5: {  'position': [149.32760800722573, 81.49698742220951],
         'useUserColor': False,
         'userColor': None},
   6: {  'position': [66.8594593752549, -46.265607005196216],
         'useUserColor': True,
         'userColor': [255, 255, 0]},
   7: {  'position': [167.03448780199665, 7.018790937363946],
         'useUserColor': False,
         'userColor': None},
   8: {  'position': [84.40626509661223, 8.038691913963063],
         'useUserColor': False,
         'userColor': None},
   9: {  'position': [124.59972466642756, -49.839889866571035],
         'useUserColor': False,
         'userColor': None},
   10: {  'position': [265.92759819267144, 22.73777626362295],
          'useUserColor': False,
          'userColor': None},
   11: {  'position': [-99.29353896789479, -44.64676948394739],
          'useUserColor': False,
          'userColor': None},
   12: {  'position': [-201.36337445169835, -39.49660757146181],
          'useUserColor': True,
          'userColor': [255, 255, 0]},
   13: {  'position': [-108.3656017826379, 11.95885058558213],
          'useUserColor': False,
          'userColor': None},
   14: {  'position': [-182.8743830495833, 14.336598507318584],
          'useUserColor': False,
          'userColor': None},
   15: {  'position': [-142.68092347976796, -43.54198327321548],
          'useUserColor': False,
          'userColor': None},
   16: {  'position': [-115.89305783249556, 82.43917310296723],
          'useUserColor': False,
          'userColor': None},
   17: {  'color': [241, 234, 255],
          'position': [29.678848943867948, -93.74747523539251],
          'rectP2': (289.91457359252047, 272.28625575283814),
          'text': u'Parallel Map on 4 processors',
          'textColor': None,
          'visualStyle': 1},
   18: {  'color': [241, 234, 255],
          'position': [-220.364398945261, -93.6404248833485],
          'rectP2': (231.49906138554226, 270.4018843913227),
          'text': u'Map on a single processor',
          'textColor': None,
          'visualStyle': 1},
   '__in__': {  'position': [0, 0], 'useUserColor': True, 'userColor': None},
   '__out__': {  'position': [0, 0], 'useUserColor': True, 'userColor': None}},
                             lazy=True,
                             eval_algo='LambdaEvaluation',
                             )




_77042448 = CompositeNodeFactory(name='x+1',
                             description='',
                             category='Unclassified',
                             doc='',
                             inputs=[],
                             outputs=[{  'desc': '', 'interface': IFunction, 'name': 'f'}],
                             elt_factory={  2: ('openalea.flow control', 'X'),
   3: ('openalea.math', '+'),
   4: ('openalea.data structure', 'int')},
                             elt_connections={  167296484: (3, 0, '__out__', 0),
   167296496: (2, 0, 3, 0),
   167296508: (4, 0, 3, 1)},
                             elt_data={  2: {  'block': False,
         'caption': 'X0',
         'delay': 0,
         'factory': '<openalea.core.node.NodeFactory object at 0xd02068c> : "X"',
         'hide': True,
         'id': 2,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': -749.0,
         'posy': -508.0,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   3: {  'block': False,
         'caption': '+',
         'delay': 0,
         'factory': '<openalea.core.node.NodeFactory object at 0xd0ceeac> : "+"',
         'hide': True,
         'id': 3,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': -700.0,
         'posy': -430.0,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   4: {  'block': False,
         'caption': '0',
         'delay': 0,
         'factory': '<openalea.core.node.NodeFactory object at 0xd153fac> : "int"',
         'hide': True,
         'id': 4,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': -642.0,
         'posy': -506.0,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   '__in__': {  'block': False,
                'caption': 'In',
                'delay': 0,
                'hide': True,
                'id': 0,
                'lazy': True,
                'port_hide_changed': set(),
                'posx': 0,
                'posy': 0,
                'priority': 0,
                'use_user_color': True,
                'user_application': None,
                'user_color': None},
   '__out__': {  'block': False,
                 'caption': 'Out',
                 'delay': 0,
                 'hide': True,
                 'id': 1,
                 'lazy': True,
                 'port_hide_changed': set(),
                 'posx': -695.5,
                 'posy': -370.0,
                 'priority': 0,
                 'use_user_color': False,
                 'user_application': None,
                 'user_color': None}},
                             elt_value={  2: [(0, "'x'")], 3: [], 4: [(0, '1')], '__in__': [], '__out__': []},
                             elt_ad_hoc={  2: {  'position': [-749.0, -508.0], 'useUserColor': False, 'userColor': None},
   3: {  'position': [-700.0, -430.0], 'useUserColor': False, 'userColor': None},
   4: {  'position': [-642.0, -506.0], 'useUserColor': False, 'userColor': None},
   '__in__': {  'position': [0, 0], 'useUserColor': True, 'userColor': None},
   '__out__': {  'position': [-695.5, -370.0],
                 'useUserColor': False,
                 'userColor': None}},
                             lazy=True,
                             eval_algo='LambdaEvaluation',
                             )



