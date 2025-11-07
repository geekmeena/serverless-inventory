#!/usr/bin/env python3
#!/usr/bin/env python3
import aws_cdk as cdk
from serverless_inventory.serverless_inventory_stack import ServerlessInventoryStack

app = cdk.App()
ServerlessInventoryStack(app, "ServerlessInventoryStack")

app.synth()


