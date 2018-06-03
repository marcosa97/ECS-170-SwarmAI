<<<<<<< HEAD
# Google Compute Login
This README will show you how to gain access to our Google Compute systems. If you have already done the CloudML README then you can skip the SDK installation.

## Installing the SDK

### Download the SDK
You will need to first download the Google Cloud SDK.
**Ubuntu**
	[Google Cloud SDK - 64 bit](https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-201.0.0-linux-x86_64.tar.gz) - 19.7MB
	[Google Cloud SDK - 32 bit](https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-201.0.0-linux-x86.tar.gz) - 19.3MB

**Windows**	
	[Google Cloud SDK - 64 bit](https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-204.0.0-darwin-x86_64.tar.gz) 103.4MB
	[Google Cloud SDK - 32 bit](https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-204.0.0-windows-x86.zip) - 103.6 MB
**Mac**
	[Google Cloud SDK - 64 bit](https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-204.0.0-darwin-x86_64.tar.gz) - 16MB
	[Google Cloud SDK - 32 bit](https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-204.0.0-darwin-x86.tar.gz) - 16MB
	
### Installing

Extract the archive into your preferred file location.

**Linux or Mac**
Once you have extracted the file you will need to run the install script. Open up a terminal in the folder you extracted the file to by either right-clicking inside the folder and selecting "Open in Terminal"or using the cd command to navigate to it. The run the following command.

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

**Warning:** This stage may give errors as the additional user access is untested. If you have any issues, contact Sean. It probably isn't your fault.

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

### Viewing the Google Compute Console
If you need to view any information about the cloud computing services, you can do that at the Compute portion of the [Google Cloud Console](https://cloud.google.com/compute/docs/console).
Here you will be able to view the names, statuses, and resource usage of all of the VMs. You should also be able to do basic operations like stopping, starting, and restart them.
If you are denied permission for any of these things or would like more permissions to create custom instances, reach out to me (Sean) and I'll get you upgraded.
=======
# ECS 170 Project: SwarmAI

## Conceptual Outline
For this project, our idea is to create a new type of AI called the swarm AI. Inspiration for this AI comes from the lore for the Zergs in SCII. Zergs can sense each other's presence within a range, and thus execute coordinated attacks without actual instructions on strategy. Instead, their "will" are overidden by an Overlord, which points them to a target, but does not specify method. In this context, the Overlord can be some type of "Master AI" that focuses on major decisions during a battle, while the "Swarm AI" are swarms of units assigned to certain tasks. Each member in a swarm can coordinate with each other and carry out the task efficiently. In this project, we will attempt to create such a Swarm AI.

## Neural network Architecture

To create such a Swarm AI, we decided to experiment with using a deep recurrent neural network with residual layers. We assume a swarm of 5 units, each with its own copy of this neural network. The same weights are shared for the entire swarm. Each neural network will take in previous action of the swarm (attack or retreat for all members), and this network's corresponding unit's status data (health, attack range, damage, etc), as well as data of target (health, attack damage, attack range, etc). This AI is only meant to test out this idea, so extended features such as unique skills are not taken into account. The output of the neural network consists of an attack head and a retreat head. Both heads are tanh-activated. The greater out of the two gets chosen. The physical meaning of the output values are prediction of evaluation score. The score is evaluated as follows:
- Died: -1
- Did not do damage, took damage: -0.5
- Did damage, took damage: 0
- Did not do damage, did not take damage: 0.5
- Did damage, did not take damage: 1

Number of layers, regularization constant, and other tuning parameters will be decided later on after prototyping.

## Training Pipeline

To train this neural network, we will be using an A3C, implemented to run on Google Cloud. Each action of each member of the swarm is saved as training data, with real ouputs acquired from training. The training data is stored in a database, from which the neural network will randomly sample to train continuously. 

In terms of the actual game, training is done using hydralisks and (some other ranged) as swarm units, with a melee unit as enemy. The melee unit is invincible, and will continuously pursue the swarm until it kills all of them, and then data from the session is collected and saved to databsae. Ranged units are used because it is easier to verify if the neural network is working, since behavior such as kiting and spreading out should occur as the neural network figures out how to maximize damage done and minimize damage taken.


>>>>>>> c7d1163bfc299ce14513ca4dd9a64ef3a9f000a2
