# Cloud Ripper

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
---

This is an effort to highlight risks from cloud misconfigurations; we also look at how seemingly unused artefacts such as IAM policies/Roles in your cloud environment can be easily misused to move laterally or exfiltrate data. This is an initial framework approach so that you can take and build upon the various service discovery and enumeration techniques that have been used in script. This particular version is aimed at AWS similar techniques can utilised with other CSP's.

**Please Note: The purpose of the code is purely educational and should not be used with malicious intent or within infrastructure where you do not have permissions to run such tests.**

## Sample Application Architecture

![Image](https://user-images.githubusercontent.com/60926235/123081035-6cd17480-d415-11eb-8e02-957101f75500.png)

In the above example, we have a simple web app that uses a vulnerable version of PHP-ImageMagic Library to convert files to pdf, we trigger the initial C2 Connection based on an RCE vulnerability within this to establish a shell within the docker container. Once on the container we are able to query the instance metadata service to obtain the credentials for the role from this point the attack flows as follows:

![Ima](https://user-images.githubusercontent.com/60926235/123082295-c5edd800-d416-11eb-9950-cc41d18ab2c1.png)

MITRE TTP's

**![MITRE Tactics Used:](https://user-images.githubusercontent.com/60926235/123084778-7230be00-d419-11eb-9ead-a1198c8fba54.png)**

### Install Pre-Reqs:

The attacker machine from which the RunAttack.py script is executed must have awscli installed and have the correct path set as well as python dependencies json,time,sys,os,subprocess. 

The script has only been tested on Debian based Linux release.

Minimum Permissions the initial Role attached to the work must have: IAM List, eg. policy bellow

```
{
 "Version": "2012-10-17",
 "Statement": [
 {
 "Sid": "VisualEditor0",
 "Effect": "Allow",
 "Action": [
 "sts:AssumeRole",
 "iam:List*",
 "iam:Get*"
 ],
 "Resource": "*"
 }
 ]
}
```

### Usage Information:

Their are two parts two the script , the attack execution script and service enumeration dictionary file.

The attack execution script reads the awscli commands present in the enum.txt file to attempt to enumerate services and try to work out how deep the permissions are in terms of privileges for the exisiting role, it than moves to find other roles that can exploited and once assumed other roles successfully will loop through and discover additional vulnerable roles that can be potentially exploited.

The script can be run as python3 RunAttack.py [the enum.txt file needs to be in the same dir as the script]

```
python3 RunAttack.py
```

## Defensive Advise:

1. Ensure applications are scanned for vulnerabilities and code dependencies and libraries used are regularly updated.

2. Ensure application traffic is inspected by a Cloud IPS solution such McAfee vNSP so you can look for malicious traffic such as shellcode or injection attempts.

3. Use Cloud Security Posture Management tool such as [MVISION Cloud]([McAfee MVISION Cloud for Container Security | McAfee](https://www.mcafee.com/enterprise/en-gb/products/mvision-cloud/container-security.html)) which can look for building your resource inventory and run effective checks against privilege creep or unused resources.

4. Remove unused Cloud config objects, and ensure any roles that have **assume** capabilities have strict conditions attached so they cannot be taken over and exploited.
