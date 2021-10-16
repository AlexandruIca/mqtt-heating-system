cmake_minimum_required(VERSION 3.15)

project(mqtt-heating-system LANGUAGES CXX)

include(cmake/Sanitizers.cmake)
include(cmake/StaticAnalyzers.cmake)
include(cmake/PreventInSourceBuilds.cmake)
include(cmake/Cache.cmake)
include(cmake/Doxygen.cmake)
include(cmake/CompilerWarnings.cmake)
include(cmake/StandardProjectSettings.cmake)

add_library(project_options INTERFACE)
target_compile_features(project_options INTERFACE cxx_std_20)
enable_sanitizers(project_options)
enable_doxygen()

add_library(project_warnings INTERFACE)
set_project_warnings(project_warnings)

option(ENABLE_TESTING "Build the tests of this project!" OFF)

add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/src/)
