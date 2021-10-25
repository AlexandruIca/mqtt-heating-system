# MQTT Heating System
This project exposes an MQTT API that should manage/observe a heating system.

# Document de analiză a cerințelor clientului

## Scopul aplicației
Aplicația are rolul de a ajuta oamenii să fie mai aproape de centralele lor. Pe timp de iarna, functia de ”control remote” este foarte importanța deoarece faciliteaza stabilirea temperaturii optime pana la sosirea oamenilor în casa, astfel nemaifiind nevoie sa aștepte incalzirea acesteia. De asemenea, alertele vin în sustinerea utilizatorului întrucât îl atentioneaza când apare o defecțiune neprevăzută a centralei, acesta putand apela imediat la un serviciu autorizat.

### Obiectivele aplicației:
- Schimbare temperatura caldura
- Schimbare temperatura apa
- Programare interval
- Alerte
- Control de la distanta

### Grupul țintă
Utilizatori casnici.

### Colectarea cerințelor
Datorită problemelor de termoficare din capitala, estimam ca numărul de centrale vândute în perioada urmatoare o să crească, așa ca ne-am gandit sa venim in ajutorul oamenilor creandu-le posibilitatea de a controla mai usor centrala, acesta fiind un moment oportun pentru crearea unei astfel de aplicatii.

### Interpretarea și prioritizarea cerințelor
- Utilizatorul poate opri/porni centrala.
- Utilizatorul poate modifica temperatura.
- Utilizatorul poate vedea statistici de utilizare a apei si gazului.
- Utilizatorul poate fi alertat daca se depaseste o anumita limita lunara sau daca centrala are o defectiune.
- Utilizatorul poate crea rutine pentru centrala.
 
## Gruparea cerințelor
In primul rand vom implementa functionalitatea de baza (pornirea si oprirea centralei). Acestea sunt destul de ușor de implementat, și acest feature e de folos tuturor utilizatorilor.
Dupa aceea vom implementa alertele, statisticile si in final rutinele.

## Prioritati
Se pot vedea si la issues.

- Pornire / Oprire 10/10
- Schimbare temperatura caldura 10/10
- Schimbare temperatura apa 10/10
- Programare interval 8/10
- Alerte 8/10
- Control de la distanta 10/10

## Plot the issues
![Axa prioritati](./media/axa-prioritati.png)

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
