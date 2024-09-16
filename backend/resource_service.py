import requests

class ResourceService:
    # This is the class to get the service-specific credentials for a resource service.
    # We use this for the case of NLU, TTS and STT services.
    def get_service_credentials(self, iam_token, service_name):
        resource_service_url = "https://resource-controller.cloud.ibm.com/v2/resource_instances"
        headers = {
            'Authorization': f'Bearer {iam_token}',
            'Accept': 'application/json',
        }
        response = requests.get(resource_service_url, headers=headers)
        if response.status_code == 200:
            resources = response.json()['resources']
            for resource in resources:
                if service_name.lower() in resource['name'].lower():
                    instance_id = resource['guid']
                    resource_key_url = f"https://resource-controller.cloud.ibm.com/v2/resource_instances/{instance_id}/resource_keys"
                    key_response = requests.get(resource_key_url, headers=headers)
                    if key_response.status_code == 200:
                        keys = key_response.json()['resources']
                        if keys:
                            return keys[0]['credentials']
                        else:
                            data = {
                                'name': f'{service_name}-Credentials',
                                'source': instance_id,
                                'role': 'Writer'
                            }
                            create_key_response = requests.post(resource_key_url, headers=headers, json=data)
                            if create_key_response.status_code == 201:
                                return create_key_response.json()['credentials']
                            else:
                                raise Exception(f"Failed to create resource key: {create_key_response.text}")
            raise Exception("No matching instance found for the specified service name.")
        else:
            raise Exception(f"Failed to get service credentials: {response.text}")