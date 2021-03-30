# import uuid
import json
import yaml
import os


configFileName=os.path.dirname(os.path.abspath(__file__)) + '/configuration.json'
configFile=open(configFileName,'r')
config=json.load(configFile)
configFile.close()

imagePullSecrets = config.get('imagePullSecrets', [])


def createFile(name,machineType,image,
        jobid,tmpFolder,workingDir,
        imountPoint,isystemMount,
        omountPoint,osystemMount,
        iomountPoint,iosystemMount,
        maxMem,maxCores,nfsIp):
    
    if os.path.exists('/data/containerized'):
        inContainer=True
    else:
        inContainer=False

    jobName=name.lower().replace(' ','-').replace('\t','-') + '-' + jobid

    yamlName=tmpFolder + '/' + jobName + '.yaml'
    commandFile=tmpFolder + '/' + 'commands.txt'

    commands=[]
    f=open(commandFile,'r')
    for line in f:
        command=line.strip()
        if command!='':
            commands.append(command)
    f.close()

    if len(commands)==1:
        command=commands[0].split()
    

    volumes=[]
    mounts=[]
    if not inContainer:
        if iomountPoint!='':
            volume={'name': jobName + '-nfs-storage'}
            volume['nfs']={'server': nfsIp, 'path': iosystemMount}
            mount={'name': volume['name'], 'mountPath': iomountPoint}

            volumes.append(volume)
            mounts.append(mount)
            
        else:
            if imountPoint!='':
                volume={'name': jobName + '-nfs-input-storage'}
                volume['nfs']={'server': nfsIp, 'path': isystemMount}
                mount={'name': volume['name'], 'mountPath': imountPoint}

                volumes.append(volume)
                mounts.append(mount)
            
            if omountPoint!='':
                volume={'name': jobName + '-nfs-output-storage'}
                volume['nfs']={'server': nfsIp, 'path': osystemMount}
                mount={'name': volume['name'], 'mountPath': omountPoint}

                volumes.append(volume)
                mounts.append(mount)
    else:
        volume={'name': jobName + '-volume', 'persistentVolumeClaim':{'claimName':'schema-data-volume'}}
        volumes.append(volume)

        if iomountPoint!='':
            mount={'name': volume['name'], 'mountPath': iomountPoint, 'subPath': iosystemMount.replace('/data/','')}
            mounts.append(mount)
            
        else:
            if imountPoint!='':
                mount={'name': volume['name'], 'mountPath': imountPoint, 'subPath': isystemMount.replace('/data/','')}
                mounts.append(mount)
            
            if omountPoint!='':
                mount={'name': volume['name'], 'mountPath': omountPoint, 'subPath': osystemMount.replace('/data/','')}
                mounts.append(mount)
    # print(volumes)
    # exit(0)
    containers=[]
    container={'name':jobName, 'resources':{}, 'image':image}
    container['resources']={'limits': {'memory': maxMem + 'Gi', 'cpu':maxCores + 'm'}}
    container['workingDir']=workingDir
    container['command']=command
    containers.append(container)

    if len(mounts)!=0:
        container['volumeMounts']=mounts

    
    manifest_data={}
    manifest_data['apiVersion']='batch/v1'
    manifest_data['kind']='Job'
    manifest_data['metadata']={'name': jobName}
    if inContainer:
        manifest_data['metadata']['namespace']='schema'

    manifest_data['spec']={'template':{'spec':{}}, 'backoffLimit':0}
    if len(volumes)!=0:
        manifest_data['spec']['template']['spec']['volumes']=volumes
    if imagePullSecrets:
        manifest_data['spec']['template']['spec']['imagePullSecrets'] = imagePullSecrets
    manifest_data['spec']['template']['spec']['containers']=containers
    manifest_data['spec']['template']['spec']['restartPolicy']='Never'

    #if memory is large, add tolerations:
    if int(maxMem) > 64:
        tolerations=[]
        tolerations.append({'key':'fat-node','operator':'Exists','effect':'NoExecute'})
        manifest_data['spec']['template']['spec']['tolerations']=tolerations
    if machineType!='converged-node':
        manifest_data['spec']['template']['spec']['nodeSelector']={'node-type':machineType}
    
    g=open(yamlName,'w')
    yaml.dump(manifest_data, g, default_flow_style=False)
    g.close()

    exit(0)
    
    return yamlName