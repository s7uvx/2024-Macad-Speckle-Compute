import rhino3dm as r3d
import specklepy

from specklepy.api.wrapper import StreamWrapper
from specklepy.api.client import SpeckleClient

import rhinoinside
rhinoinside.load()



# Our MaCAD server!
server_url = "https://macad.speckle.xyz"
# The token for your account. Get it from the Speckle Dashboard > Profile > Acess Tokens
token = "d92d6c2cc1011cbe561f6e3e5eaf80cf0c307142f9"
# This is the stream you want to federate the branches of. Change it to your studio stream! 
stream_url = "https://macad.speckle.xyz/streams/4975f9f0a8"
# The name of the branch you want to push to. The data inside it will be ignored on further pushes.
combine_branch = "shared/g12"

filePath = r'C:\Users\cawn069856\Documents\IAAC\Studio\rhino-revit\revitLinks_method\01_bakedGeo_clusters.3dm'

model = r3d.File3dm().Read(filePath)

for instance in model.InstanceDefinitions:
    if instance.Name == 'R00':
        print(instance.Name)
        print(instance.Id)
        instanceId = instance.Id

transforms = []
for o in model.Objects:
    if o.Geometry.ObjectType==r3d.ObjectType.InstanceReference:
        if o.Geometry.ParentIdefId == instanceId:
            transforms.append(r3d.Transform.ToFloatArray(o.Geometry.Xform, False))

print(transforms)

# Authenticate the account with the token (for servers or remote scripts that don´t have access to your local speckle account)
client = SpeckleClient(host=server_url)
client.authenticate_with_token(token)

# Get the stream object and a transport object
wrapper = StreamWrapper(stream_url)
stream_id = wrapper.stream_id
transport = wrapper.get_transport()

g12branch = client.branch.get(stream_id, "wip/g12/r00",commits_limit=1)

print(g12branch.commits.items)

# for obj in model.Objects:
#     if obj.Attributes.Name:
#         print("{} / {} ".format(obj.Geometry.ObjectType, obj.Attributes.Name))
#     print(obj.Attributes())
# for o in model.Objects:
#     if o.Geometry.ObjectType==r3d.ObjectType.InstanceReference:
#         print(o.Geometry.GetObjectIds())
        # print("{} / {} / {}".format(o.Geometry.ObjectType, r3d.Transform.ToFloatArray(o.Geometry.Xform, False), o.Geometry.ParentIdefId))
        # uuid=o.Geometry.ParentIdefId

#get geometry from stream
