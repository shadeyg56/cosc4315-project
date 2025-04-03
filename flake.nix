{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "x86_64-darwin" "aarch64-linux" "aarch64-darwin" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
      pkgs = forAllSystems (system: nixpkgs.legacyPackages.${system});
    in
    {
      devShells = forAllSystems (system: {
        default = pkgs.${system}.mkShellNoCC {

          packages = with pkgs.${system}.python312Packages; with pkgs.${system}; [
            python312
            beautifulsoup4
            types-beautifulsoup4
            requests
            lxml
            numpy
            scikit-learn
            transformers
            torch
            tf-keras
            datasets
            accelerate
            chromadb
            docker
            docker-compose
            rootlesskit
            ollama
          ];

          shellHook = ''
          '';

        };
      });
    };
}
