# Use an official Python runtime as the base image
FROM python:3.9-slim

FROM ubuntu:latest

# Install curl and tar for installing pixi binary
RUN apt-get update && \
    apt-get install -y curl tar

# Environment variables
ENV PIXI_VERSION=latest
ENV INSTALL_DIR=/usr/local/bin
ENV REPO=prefix-dev/pixi
ENV PLATFORM=unknown-linux-musl
ENV PROJECT_NAME=pixi-in-docker

# Download and install pixi
RUN if [ "$PIXI_VERSION" = "latest" ]; then \
    DOWNLOAD_URL="https://github.com/$REPO/releases/latest/download/pixi-$(uname -m)-$PLATFORM.tar.gz"; \
    else \
    DOWNLOAD_URL="https://github.com/$REPO/releases/download/$PIXI_VERSION/pixi-$(uname -m)-$PLATFORM.tar.gz"; \
    fi && \
    curl -SL "$DOWNLOAD_URL" | tar -xz -C "$INSTALL_DIR"

# Make a project dir and make it the workdir for the docker image.
RUN mkdir -p /root/$PROJECT_NAME
WORKDIR /root/$PROJECT_NAME

# Copy the project file and lockfile to only reinstall environment if those are changed.
COPY ../../pixi.lock ../../pixi.toml ./

# Install the environment
# The mount is a docker specific cache location so the firstime it will be slow but the second time the cache will be reused.
# More info in their docs: https://docs.docker.com/build/guide/mounts/
RUN --mount=type=cache,target=/root/.cache/rattler pixi install

COPY ../../. ./ 

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY pixi.lock .
COPY pixi.toml .

# Install the dependencies
RUN pixi install

# Copy the rest of the application code to the working directory
COPY . .

RUN pixi run pip_install_e

# Expose the port that Streamlit runs on
EXPOSE 8000

# Set the command to run the Streamlit app
CMD ["pixi", "run", "api"]
