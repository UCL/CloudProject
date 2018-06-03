{ pkgs ? import <nixpkgs> {} }:

pkgs.dockerTools.buildImage {
  name = "mpi4py";
  tag = "latest";

  contents = with pkgs; [ 
    openmpi
    (python35.withPackages(ps: with ps; [numpy scipy ipython mpi4py]))
  ];

  config = {
    Cmd = [ "python3 -m IPython" ];
    WorkingDir = "/build";
    Volumes = {
      "/build" = {};
    };
  };
}
