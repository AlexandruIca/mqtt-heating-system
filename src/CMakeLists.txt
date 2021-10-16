set(Boost_USE_STATIC_LIBS ON)

find_package(fmt REQUIRED)
find_package(Boost REQUIRED COMPONENTS log)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

add_executable(${CMAKE_PROJECT_NAME} ${CMAKE_CURRENT_SOURCE_DIR}/main.cpp)
target_include_directories(${CMAKE_PROJECT_NAME} PRIVATE ${Boost_INCLUDE_DIR})
target_link_libraries(${CMAKE_PROJECT_NAME} PRIVATE fmt::fmt Boost::log)
