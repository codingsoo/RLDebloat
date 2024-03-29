FROM debian:buster

RUN apt-get update && apt-get install -y software-properties-common wget gnupg
RUN wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add -
RUN apt-add-repository "deb http://apt.llvm.org/buster/ llvm-toolchain-buster-8 main" && apt-get update
RUN apt-get install -y clang-8 libclang-8-dev llvm-8-dev cmake git wget
RUN apt-get install -y libspdlog-dev nlohmann-json-dev
RUN apt-get install -y libmlpack-dev libpcre3-dev
RUN ln -s /usr/bin/clang-8 /usr/bin/clang && ln -s /usr/bin/llvm-config-8 /usr/bin/llvm-config

COPY chisel /tmp/chisel
COPY benchmark /bench
RUN mkdir -p /tmp/chisel/build && cd /tmp/chisel/build && CXX=clang cmake .. && make

ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/tmp/chisel/build/bin
ENV CC clang
ENV CHISEL_BENCHMARK_HOME /bench
