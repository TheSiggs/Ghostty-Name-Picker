{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python312;
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            python
            pkgs.poetry
            pkgs.cmake
            pkgs.google-cloud-sdk

            pkgs.gcc
            pkgs.libffi
          ];
          shellHook = ''
            export LD_LIBRARY_PATH=${pkgs.gcc.cc.lib}/lib:$LD_LIBRARY_PATH
            export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.config/gcloud/application_default_credentials.json"
            export GOOGLE_CLOUD_PROJECT="ghostty-picker"
            export FLASK_SETTINGS_FILENAME="settings.py"

            echo "Activating Poetry environment..."
            if [ ! -d ".venv" ]; then
              poetry install
            fi
            source .venv/bin/activate
          '';
        };
      });
}

