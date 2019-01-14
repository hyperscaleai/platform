# Follow HDP insturctions 
Need to sign up first:
https://docs.hortonworks.com/HDPDocuments/Ambari-2.7.3.0/bk_ambari-installation/content/download_the_ambari_repo_ubuntu16.html

1. Perpare
    Make sure you can ssh as root to the host id_rsa >> authorized_hosts 
    hostname -f / FQDN setup (I put localhost for simplicity)
    
2. Add Ambari Server repo & update packages 

3. Install Ambari Server:
    apt-get install ambari-server

4. Setup Ambari Server
    ambari-server setup

5. Start Ambari Server

    ISSUE: could not install agent. I manually run agent ssh root@localhost & service ambari-agent start 
    SOLUTION: https://docs.hortonworks.com/HDPDocuments/Ambari-2.6.2.0/bk_ambari-administration/content/install_the_ambari_agents_manually.html



Ubuntu 16
On a server host that has Internet access, use a command line editor to perform the following:

Steps

Log in to your host as root.

Download the Ambari repository file to a directory on your installation host.

wget -O /etc/apt/sources.list.d/ambari.list http://public-repo-1.hortonworks.com/ambari/ubuntu16/2.x/updates/2.7.3.0/ambari.list
apt-key adv --recv-keys --keyserver keyserver.ubuntu.com B9733A7A07513CAD
apt-get update
[Important]	Important
Do not modify the ambari.list file name. This file is expected to be available on the Ambari Server host during Agent registration.

Confirm that Ambari packages downloaded successfully by checking the package name list.

apt-cache showpkg ambari-server
apt-cache showpkg ambari-agent
apt-cache showpkg ambari-metrics-assembly
You should see the Ambari packages in the list.

[Note]	Note
When deploying a cluster having limited or no Internet access, you should provide access to the bits using an alternative method.

Ambari Server by default uses an embedded PostgreSQL database. When you install the Ambari Server, the PostgreSQL packages and dependencies must be available for install. These packages are typically available as part of your Operating System repositories. Please confirm you have the appropriate repositories available for the postgresql-server packages.