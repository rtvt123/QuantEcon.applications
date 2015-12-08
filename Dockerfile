# quantecon.applications Docker Image (for mybinder.org service)
# User: main

FROM andrewosh/binder-base

MAINTAINER Matthew McKay <mamckay@gmail.com>

USER root

#-Update Debian Base-#
RUN apt-get update -y
RUN apt-get install -y --no-install-recommends curl ca-certificates

# Julia dependencies
RUN apt-get install -y julia libnettle4 && apt-get clean

USER main

#-Install Python3.5 Anaconda Distributions-#
RUN conda update --yes conda
RUN conda install --yes python=3.5 anaconda && conda clean -yt
RUN pip install quantecon
# RUN source activate python2 && pip install quantecon && source deactivate python2

#-Julia Packages-#
RUN echo "cacert=/etc/ssl/certs/ca-certificates.crt" > ~/.curlrc
RUN julia -e 'Pkg.add("PyCall"); Pkg.checkout("PyCall"); Pkg.build("PyCall"); using PyCall'
RUN julia -e 'Pkg.add("IJulia"); using IJulia'
RUN julia -e 'Pkg.add("PyPlot"); Pkg.checkout("PyPlot"); Pkg.build("PyPlot"); using PyPlot' 
RUN julia -e 'Pkg.add("Distributions"); using Distributions'
RUN julia -e 'Pkg.add("KernelEstimator"); using KernelEstimator'