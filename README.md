# ny-cab-analytics
### Introduction
The main aim of the project was to analyse and create a pipeline for the NYC Yellow taxi trip data.
[Data source](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

### Project Stucture
- `./main/expt.ipynb` : jupyter notebook where all the experimentation resides
- `./ny-data-pipeline/` : directory where all the code in the mage(orchestrator) resides.

### Installation and setup

**configuring remote machine**
- create a VM instance in Google Compute Engine.
- Generate the private and public SSH keys using [this](https://cloud.google.com/compute/docs/connect/create-ssh-keys ).
- go to the SSH folder `cd .ssh`, you will find a private key and a public key(`.pub` extension). Copy the contents of the public key -> open `metadata` in the current project -> SSH keys -> paste it there. 
- to connect to the already created instance from your local machine via terminal : `ssh -i ~/.ssh/<private key folder name> <username>@<copied IP address>`
- to ssh into the VM, open the config file in the `.ssh` folder(create one if you don't have any) and make the following changes
```
host <name can be anything preferrably short>
	HostName <external IP of the instance created>
	User <user name used to create the ssh key>
	IdentityFile ~/.ssh/config
```
- Now we can simply connect to the instance using `ssh <host name used above>`
- setup VSCode(or an editor of your choice) by installing remote extension and connect to the remote instance

****


Click [here](https://lookerstudio.google.com/reporting/24cca208-4879-493e-8c4e-c28c17b4f7ff) to view the dashboard on looker.
