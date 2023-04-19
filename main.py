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
flagName = os.getenv('HARNESS_FLAG_NAME', "rolloutFlag")
idMin = os.getenv('HARNESS_ID_MIN', 10000)
idMax = os.getenv('HARNESS_ID_MAX', 99999)


def main():    
    # Create a Feature Flag Client
    client = CfClient(apiKey)

    # Loop forever reporting the state of the flag
    while True:
        print("\n\nEVALUATING TARGET...")

        generated_id = generate_identifier()
        target = Target(identifier=generated_id, name=generated_id, attributes={"location": "us"})
        result = client.bool_variation(flagName, target, False)
        
        log.info("\nFLAG VARIATION: %s", result)
        write_to_file(flagName, generated_id, result)
        
        time.sleep(1)

    close()


def generate_identifier():
    identifier = random.randint(idMin, idMax)
    identifier = "generated-" + str(identifier)
    return identifier


def write_to_file(flagName, generatedId, result):
    f = open("output.txt", "a")
    f.write(f"{flagName},{generatedId},{result}\n")

if __name__ == "__main__":
    main()