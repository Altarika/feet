FROM ubuntu:14.04
MAINTAINER Romary Dupuis <romary.dupuis@altarika.com>
# update what we need
RUN apt-get update && apt-get install -y \
      curl \
      python-dev \
      python-setuptools \
      python-pip \
      libmecab-dev \
      mecab \
      mecab-ipadic-utf8 \
      git \
      vim
# install neologd dictionary for MeCab
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git && cd mecab-ipadic-neologd && ./bin/install-mecab-ipadic-neologd -y 
# set up volume we will share our codebase with
ENV INSTALL_PATH /usr/local/feet
WORKDIR $INSTALL_PATH
COPY . .
# add feet package to our python path
RUN echo $(pwd) > /usr/local/lib/python2.7/dist-packages/feet.pth
# install requirements
RUN pip install -r requirements/project.txt && python -m nltk.downloader averaged_perceptron_tagger maxent_ne_chunker maxent_treebank_pos_tagger punkt words
EXPOSE 5000
# launch feet server
CMD /bin/true
