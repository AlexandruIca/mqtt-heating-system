# MQTT Heating System
This project exposes an MQTT API that should manage/observe a heating system.

# Setting up a development environment
- Clone this repo including the `vcpkg` submodule:
  ```
  git clone --recurse-submodules https://github.com/AlexandruIca/mqtt-heating-system.git
  ```
- Build `vcpkg`:
  ```sh
  cd vcpkg/
  ./bootstrap-vcpkg.sh
  ```
- Make sure you have [CMake](https://cmake.org/) installed
- Run:
  ```sh
  # Might take some time when you first running, it will install all the dependencies
  cmake -B build/ \
    -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
    -DCMAKE_TOOLCHAIN_FILE=./vcpkg/scripts/buildsystems/vcpkg.cmake . \

  cd build/
  cmake --build .
  # You can also copy the `compile_commands.json` file to your root dir(to be used by C++ tools)
  #
  # After everything succeeds you have you executable in `build/src/`
  ```
Alternatively, if you have [nix](https://github.com/NixOS/nix) installed there's already a `shell.nix` in the repo, you can use that and you're all set(with this you can also use `scripts/linux-build.sh`).

# Contributing
- Start a new branch when you want to work on something, and give that branch a descriptive name
- Just make sure you format your code correctly(you can use `clang-format` and `cmake-format` to verify that you code is formatted correctly)
- Always have an issue to link your commits to
- The first line of every commit should be concise and descriptive, with a reference to the issue it's linked to, after that you can optionally have a blank line followed by as much text as you need. Try not to exceed more than 80-100 columns in your commits, example:
  ```
  Updated some info in the README (#42)

  Whatever...
  ```
- Make a PR and link your PR to the appropiate issue