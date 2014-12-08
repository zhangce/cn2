// Copyright (c) 2014, Jing Fan and Ce Zhang. All Rights Reserved.
// This file gives the definition of the APIs exposed to the users.

#ifndef _H3_UTIL_H_
#define _H3_UTIL_H_


#include <string.h>
#include <unistd.h>

#include "dirent.h"

#include <fstream>
#include <iostream>
#include <string>
#include <utility>
#include <vector>
namespace h3 {

  #define PATH_NUM 256
  
  /**
   * @brief Define Vertex type.
   */
  // typedef std::pair<int, VertexData> Vertex;
  
  typedef std::string NodeIdType;
  
  template <typename VertexData>
  struct Vertex {
    public:
      NodeIdType nodeId;
      VertexData data;
      std::vector<Vertex<VertexData> > neighbours;
      Vertex(NodeIdType nId,
             VertexData& vdata,
             bool isOrigin)
        : nodeId(nId), data(vdata) {
          if (isOrigin) {
            getNeighbours(neighbours);
          }
        }
  };

  /**
   * @brief Get the id of this vertex.
   */
   NodeIdType getVertexId() {
    char path[PATH_NUM];
    getcwd(path, sizeof(path));
    // std::cout << path << std::endl;
    std::vector<char*> splitArray;
    char* pch = strtok(path, "/");
    while (pch != NULL) {
      splitArray.push_back(pch);
      pch = strtok(NULL, "/");
    }
    // std::cout << splitArray.back() << std::endl;
    // char nodeIdStr[PATH_NUM];
    // memcpy(nodeIdStr, splitArray.back() + 1, strlen(splitArray.back()));
    return std::string(splitArray.back());
  } 

  /**
   * @brief Get the data of this vertex
   */
  template <typename VertexData>
  VertexData getData() {
    std::ifstream fin("./state");
    VertexData data;
    fin >> data;
    fin.close();
  }

  /**
   * @brief Get the id and values of neighbours.
   * @param neighbours The id and values of neighbours.
   */
  template <typename VertexData>
  void getNeighbours(std::vector<Vertex<VertexData> >& neighbours) {
    struct dirent *entry;
    DIR* startDir;
    startDir = opendir("./neighbors");
    if (startDir  == NULL) {
      perror("opendir");
      std::cout <<  "haha";
    }

    while ((entry = readdir(startDir))) {
      // return;
      if (entry->d_name[0] == '.') {
        continue;
      }

      std::string neighbourDir("../");
      neighbourDir.append(std::string(entry->d_name));
      neighbourDir.append("/state");
      std::ifstream fin(neighbourDir);
      // std::cout << startDir << " " << neighbourDir << std::endl;
      VertexData data;
      fin >> data;
      std::cout << neighbourDir << " : " << data << std::endl;
      neighbours.push_back(Vertex<VertexData>(std::string(entry->d_name),
                                              data,
                                              false));
      fin.close();
    }

    closedir(startDir);
  }  
  

  /**
   * @brief Update the value of the node with nodeId. The node should either be
   * current node or neighbour node.
   * @param nodeId The id of the node to be updated.
   * @param newVal The new value.
   */
  template <typename VertexData>
  void updateValue(NodeIdType nodeId, VertexData newVal) {
    std::ofstream fout("../" + nodeId + "/state" );
    fout << newVal;
    fout.close();
  }
} // namespace h3
#endif // _H3_UTIL_H_
