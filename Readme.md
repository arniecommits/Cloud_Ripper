# Cloud Ripper

---

This is an effort to highlight risks from cloud misconfigurations or having seemingly unused artefacts such as IAM policies/Roles in your cloud environment. This is an initial framework approach so that you can take and build upon the various service discovery and enumeration techniques that have been used in script. This particular version is aimed at AWS similar techniques can utilised with other CSP's.



**Please Note: The purpose of the code is purely educational and should not be used with malicious intent or within infrastructure where you do not have permissions to run such tests.**



## Sample Application Architecture

![Image](https://user-images.githubusercontent.com/60926235/123081035-6cd17480-d415-11eb-8e02-957101f75500.png)

In the above example, we have a simple web app that uses a vulnerable version of PHP-ImageMagic Library, we trigger the initial C2 Connection based on an RCE vulnerability within this to establish a shell within the docker container. Once on the container we are able to query the instance metadata service to obtain the credentials for the role from this point the attack flows as follows:

![Ima](https://user-images.githubusercontent.com/60926235/123082295-c5edd800-d416-11eb-9950-cc41d18ab2c1.png)












