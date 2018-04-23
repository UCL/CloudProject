{ pkgs ? import <nixpkgs> {} }:

pkgs.dockerTools.buildImage {
  name = "mpi4py";
  tag = "latest";

  contents = [ python3, openmpi ];
  runAsRoot = ''
      #!${stdenv.shell}
      mkdir -p /build
  '';

  config = {
    Cmd = [ "python3" ];
    WorkingDir = "/build";
    Volumes = {
      "/build" = {};
    };
  };
}
