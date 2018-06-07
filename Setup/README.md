# Google Compute Login
This README will show you how to gain access to our Google Compute systems. If you have already done the CloudML README then you can skip the SDK installation.

## Installing the SDK

### Download the SDK
You will need to first download the Google Cloud SDK.

**Ubuntu**
  
  [64 bit](https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-201.0.0-linux-x86_64.tar.gz) - 19.7MB
  
  [32 bit](https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-201.0.0-linux-x86.tar.gz) - 19.3MB

**Windows**	
  
  [64 bit](https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-204.0.0-darwin-x86_64.tar.gz) 103.4MB
  
  [32 bit](https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-204.0.0-windows-x86.zip) - 103.6 MB

**Mac**
	
  [64 bit](https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-204.0.0-darwin-x86_64.tar.gz) - 16MB
	
  [32 bit](https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-204.0.0-darwin-x86.tar.gz) - 16MB
	
### Installing

Extract the archive into your preferred file location.

Once you have extracted the file you will need to run the install script. Open up a terminal in the folder you extracted the file to by either right-clicking inside the folder and selecting "Open in Terminal"or using the cd command to navigate to it. The run the following command.

**Linux or Mac**
```
./google-cloud-sdk/install.sh
```

**Windows**
```
.\google-cloud-sdk\install.bat
```

### Initialize

Now that you have installed the SDK, you will need to use the gcloud command to perform a few SDK setup tasks.

To start setup, run the following.
```
cd google-cloud-sdk
gcloud init
```

It should then ask you to login. Select 'Y'
```
To continue, you must log in. Would you like to log in (Y/n)? Y
```

Login to the @ucdavis.edu emails you provided to the team and click **Allow**.
**Note:** I have set your accounts to have full owner permissions. Please do not make any changes to the project settings without consulting the team first.

You will then see something like the following.
```
Pick cloud project to use: 
 [1] ecs170-swarmai-id
 [2] other-project-1
 [3] other-project-2
 [4] Create a new project
Please enter numeric choice or text value (must exactly match list
```

Select whichever number corresponds to "ecs170-swarmai-id"

It will then ask you
```
Do you want to configure a default Compute Region and Zone? (Y/n)?
```
Just enter 'n'. Our regions are already set up.

## Connecting to the cloud instances
This part will show you how to connect to the instance group. An instance group is a collection of VMs that will allow multiple people to access their own VMs simultaneously without take resources from each other. We can have up to 10 instances at a time.

### Logging in through glcoud (ssh)
All you have to do from now on is enter this command into terminal/CMD. If you would like to run multiple instances simultaneously log into any of the single instances by changing the instance name at the end of the command.
```
gcloud compute --project "ecs170-swarmai-id" ssh --zone "us-east1-b" "api-instance-group-5v7p"
```
All of the files for the API, Cloud, and located in /home/seana/. The VM will automatic create an empty home folder for you when you login so you will need to navigate to mine.

### Viewing the Google Compute Console
If you need to view any information about the cloud computing services, you can do that at the Compute portion of the [Google Cloud Console](https://cloud.google.com/compute/docs/console).
Here you will be able to view the names, statuses, and resource usage of all of the VMs. You should also be able to do basic operations like stopping, starting, and restart them.
If you are denied permission for any of these things or would like more specific permissions, reach out to me (Sean) and I'll get them upgraded.
