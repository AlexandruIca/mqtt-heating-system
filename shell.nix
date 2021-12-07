let
    pkgs = import (fetchTarball("https://github.com/NixOS/nixpkgs/archive/ee90403e147b181300dffca5b0afa405e14f1945.tar.gz")) {};
in pkgs.mkShell {
    name = "cpp-environment";
    buildInputs = [
        pkgs.gcc11
        pkgs.ninja
        pkgs.gnumake
        pkgs.cmake
        pkgs.cmake-format
        pkgs.clang-tools
        pkgs.ccache
        pkgs.doxygen
        pkgs.python39
        pkgs.poetry
    ];
    shellHook = ''source ~/.bashrc'';
}
