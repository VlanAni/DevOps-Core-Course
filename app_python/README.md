## Overview

Simple REST-API server on FastAPI framework

## Prerequisites

Python version >= 3.14

OS: any UNIX system

## Installation

uv sync

## Running 

`python app.py`

## API Endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | `/` | Get full information about this app |
| GET | `/health` | Get some information about runtime |

## Configuration

| ENV | Default | Purpose |
| --- | --- | --- |
| PORT | `5000` | A port which the server listening on |
| HOST | `0.0.0.0` | An address of interfaces whose the server is listening on |
| DEBUG | `False` | Debug mode for the server |