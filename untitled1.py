# -*- coding: utf-8 -*-
"""
Created on Tue May 18 17:10:49 2021

@author: scout
"""
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist,
                  best_path):
    path[0].append(str(start))
    print(path)
    # if start and end are not valid nodes:
    #     raise an error
    if not (digraph.has_node(start) and digraph.has_node(end)):
        raise ValueError('invalid start/end nodes') 
    # elif start and end are the same node:
    #     update the global variables appropriately
    elif start == end:
        return(path)
    # else:
    else:
        #     for all the child nodes of start
        for edge in digraph.get_edges_for_node(start):
            if edge not in path:
                edge_source = edge.src
                edge_destination = edge.dest
                if (best_dist == None or path[1] < best_dist) and path[2] <= max_dist_outdoors:
                    #     construct a path including that node
                    # path[0] += str(edge_source), str(edge_destination)
                    path[1] += edge.get_total_distance()
                    path[2] += edge.get_outdoor_distance()
                    #     recursively solve the rest of the path, from the child node to the end node
                    newpath = get_best_path(digraph, edge_destination, end, path, max_dist_outdoors, best_dist, best_path)
                    # best_dist = newpath[1]
                    if newpath != None:
                        best_path = newpath
                    
    # return the shortest path
    return(best_path)