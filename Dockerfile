# QuantEcon.applications Docker Image (for tmpnb orchestrate.py server & mybinder service)
# User: econ

FROM andrewosh/binder-base

MAINTAINER Matthew McKay <mamckay@gmail.com>

USER root

RUN apt-get update

# Julia dependencies
RUN apt-get install -y julia libnettle4 && apt-get clean

ENV CONDA_DIR /opt/conda

# Install conda
RUN echo 'export PATH=$CONDA_DIR/bin:$PATH' > /etc/profile.d/conda.sh && \ 
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    /bin/bash Miniconda3-latest-Linux-x86_64.sh -b -p $CONDA_DIR && \
    rm Miniconda3-latest-Linux-x86_64.sh && \
    $CONDA_DIR/bin/conda update --yes conda

# We run our docker images with a non-root user as a security precaution.
# econ is our user
RUN useradd -m -s /bin/bash econ
RUN chown -R econ:econ $CONDA_DIR

EXPOSE 8888

USER econ
ENV HOME /home/econ
ENV SHELL /bin/bash
ENV USER econ
ENV PATH $CONDA_DIR/bin:$PATH
WORKDIR $HOME

RUN ipython profile create

# Workaround for issue with ADD permissions
USER root
# ADD notebooks/ /home/econ/
RUN chown econ:econ /home/econ -R
USER econ

# Python packages
RUN conda install --yes pip numpy pandas scikit-learn scikit-image matplotlib scipy seaborn sympy cython patsy statsmodels cloudpickle dill numba bokeh && conda clean -yt

#Install QuantEcon
RUN pip install quantecon
#RUN source activate python2 && pip install quantecon && source deactivate python2

# IJulia and Julia packages
RUN julia -e 'Pkg.add("IJulia")'
# RUN julia -e 'Pkg.add("PyPlot")' && julia -e 'Pkg.add("Distributions")' && julia -e 'Pkg.add("KernelEstimator")' 
# julia -e 'Pkg.add("Gadfly")' && julia -e 'Pkg.add("RDatasets")' &&
# RUN julia -e 'Pkg.add("QuantEcon")'