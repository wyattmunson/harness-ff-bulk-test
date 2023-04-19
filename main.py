from featureflags.client import CfClient
from featureflags.config import *
from featureflags.evaluations.auth_target import Target
from featureflags.util import log
import os
import time
import random

# API Key
apiKey = os.getenv('HARNESS_SDK_KEY', "export HARNESS_SDK_KEY varible")

# Flag Name
flagName = os.getenv('FF_FLAG_NAME', "rolloutFlag")

def main():    
    # Create a Feature Flag Client
    client = CfClient(apiKey)

    # Create a target (different targets can get different results based on rules.  This include a custom attribute 'location')
    # target = Target(identifier='pythonSDK', name="PythonSDK", attributes={"location": "emea"})

    # Loop forever reporting the state of the flag
    while True:
        print("\n\nEVALUATING TARGET...")
        generated_id = generate_identifier()
        target = Target(identifier=generated_id, name=generated_id, attributes={"location": "us"})
        result = client.bool_variation(flagName, target, False)
        log.info("Flag variation %s", result)
        write_to_file(flagName, generated_id, result)
        time.sleep(2)

    close()


def generate_identifier():
    identifier = random.randint(10000, 99999)
    identifier = "generated-" + str(identifier)
    return identifier


def write_to_file(flagName, generatedId, result):
    f = open("output.txt", "a")
    f.write(f"{flagName},{generatedId},{result}\n")

if __name__ == "__main__":
    main()