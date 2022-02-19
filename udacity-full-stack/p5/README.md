# Linux Server Configuration

### Overview

This project takes a baseline installation of a Linux distribution on a virtual machine and prepares it to host a web application by installing updates, securing it from a number of attack vectors, and installing/configuring web and database servers.

### HTTP

The web application, [The MOOC Catalog](https://github.com/allanbreyes/mooc-catalog), is hosted via HTTP at the server's IP address: [52.10.171.172](http://52.10.171.172/).

### SSH

To gain entry into the server, one can SSH into the server by executing the command:

```
ssh -p 2200 -i [RSA_FILE] grader@52.10.171.172
```

Ensure the RSA file is included and enter the password provided.
