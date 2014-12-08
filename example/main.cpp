// Copyright (c) 2014, Jing Fan. All Rights Reserved.
//

#include "util.h"

#include <vector>

#include <iostream>
int main() {
  std::cout << h3::getVertexId() << "\n";
  
  std::vector<h3::Vertex<double> > neighbours;
  // h3::getNeighbours<double>(neighbours);
  h3::getNeighbours(neighbours);
  h3::updateValue("v2", 34294);
  return 0;
}
