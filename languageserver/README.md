# Language Server

This directory contains some examples about coc.nvim + Language Server in Docker.
Note that do not just copy and paste, I can't guarantee it to work.


### Mount Volume Path

LSP assumes that local process.
So, if you want to build language server not in local and communicate it,
you have to pretend to be in the server and communicate locally.
Your volume mount destination in docker-compose.yml is the same as `pwd`,
then you can be pretender.
