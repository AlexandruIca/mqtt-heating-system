#!/usr/bin/env sh

CC=gcc CXX=g++ cmake -B build/ -G"Ninja" \
  -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
  -DENABLE_SANITIZER_ADDRESS=ON \
  -DENABLE_SANITIZER_UNDEFINED_BEHAVIOR=ON \
  -DCMAKE_TOOLCHAIN_FILE=./vcpkg/scripts/buildsystems/vcpkg.cmake \
  .

cd build/
cp compile_commands.json ..
cmake --build .
