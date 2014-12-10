// Copyright (c) 2014, Jing Fan. All Rights Reserved.
//

#include "util.h"

#include <vector>

#include <iostream>
#include <string>

int main() {
  // std::cout << h3::getVertexId() << "\n";
  
  // std::vector<h3::Vertex<double> > neighbours;
  // h3::getNeighbours<double>(neighbours);
  // h3::getNeighbours(neighbours);
  // double sum = 0;
  // for (Vertex v : neighbours) {
  //  sum += v.data;
  //}

  //h3::updateValue(h3::getVertexId(). 0.85*sum + 0.15);
  // h3::updateValue("v2", 34294);
 
  std::string vData = h3::getData();
  
  // TODO: Deserialize
  Image *img = deserialize(vData);
  
  std::vector<h3::vector<std::string> > neighbours;
  h3::getNeighbours(neighbours);

  if (neighbours.size() == 0) {
    std::cout << "ERROR: The image has no neighbour\n";
    return -1;
  }
  
  // TODO: Deserialize
  Network *nw = deserialize(neighbours[0].data);
  NodeId nwId = neighbours[0].nodeId;

  Layer *layer1 = nw->layers[0];
  Layer *layer6 = nw->layers[5];
  layer6->operations[0]->groundtruth = img->label;
  for (int i = 0; i < 4; ++i) {
    layer1->operations[i]->inputs[0] = img->pixels; 
  }

  nw->forward();
  nw->backward();

  // TODO : Serialize
  std::string output = serialize(nw);
  h3::updateValue(nwId, output);

  return 0;
}
