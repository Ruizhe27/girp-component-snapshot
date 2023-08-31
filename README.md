# girp-component-snapshot

## Introduction

This project aims to extract components from model based on its object tree structure. From a GIRP metadata file, this algorithm will output components and computing relavant camera specs.
<br>
<br>

## Usage

Start gRPC server locally<br>
`docker-compose up --build`
<br>
<br>

To start computing camera angles, first setup the local environment:<br>
`conda create --name component-snapshot python=3.10`

`cd girp-component-snapshot`

`pip install -r requirements.txt`
<br>
<br>

And run with example place file:<br>
`python -m service.client $path_to_metadata`
<br>
