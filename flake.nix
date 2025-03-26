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

          packages = with pkgs.${system}; [
            python312
            python312Packages.beautifulsoup4
            python312Packages.types-beautifulsoup4
            python312Packages.requests
            python312Packages.lxml
            python312Packages.numpy
            python312Packages.scikit-learn
            python312Packages.transformers
            python312Packages.tensorflow
            python312Packages.tf-keras
          ];

          shellHook = ''
          '';

        };
      });
    };
}
