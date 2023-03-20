#!/bin/bash

# Download and extract the Gurobi Optimizer
wget https://packages.gurobi.com/10.0/gurobi10.0.1_armlinux64.tar.gz
tar -xf gurobi10.0.1_armlinux64.tar.gz -C /opt
rm gurobi10.0.1_armlinux64.tar.gz

# Add environmental variables to the .profile file.
cat << EOF >> /home/ubuntu/.profile
export GUROBI_HOME="/opt/gurobi1001/armlinux64"
export PATH="\$PATH:\$GUROBI_HOME/bin"
export LD_LIBRARY_PATH="\$GUROBI_HOME/lib"
EOF

# Move the license file to the Gurobi folder.
mv gurobi.lic /opt/gurobi1001
