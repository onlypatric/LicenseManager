import requests

class AdminLicenseAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_license(self):
        response = requests.post(f"{self.base_url}/admin/licenses")
        return response.json()

    def update_license(self, uuid, data):
        response = requests.put(f"{self.base_url}/admin/licenses/{uuid}", json=data)
        return response.json()

    def delete_license(self, uuid):
        response = requests.delete(f"{self.base_url}/admin/licenses/{uuid}")
        return response.json()

    def get_all_licenses(self):
        response = requests.get(f"{self.base_url}/admin/licenses")
        return response.json()

    def set_expiry_date(self, uuid, expiry_date):
        data = {"expiryDate": expiry_date}
        response = requests.post(f"{self.base_url}/admin/licenses/{uuid}/set_expiry", data=data)
        return response.json()
    
    def get_license_info(self, uuid):
        response = requests.get(f"{self.base_url}/admin/licenseinfo/{uuid}")
        return response.json()

    def ban_device(self, uuid, device):
        data = {"device": device}
        response = requests.post(f"{self.base_url}/admin/licenses/{uuid}/ban_device", json=data)
        return response.json()

# Example usage of the AdminLicenseAPI class
if __name__ == "__main__":
    admin_api = AdminLicenseAPI("http://localhost:8000")

    # Create a new license
    new_license = admin_api.create_license()
    print("New License:", new_license)

    # Update a license
    license_uuid = new_license.get("uuid")
    # Set expiry date for a license
    expiry_date = "30/09/2023"
    expiry_result = admin_api.set_expiry_date(license_uuid, expiry_date)
    print("Expiry Result:", expiry_result)
    # Get all licenses
    all_licenses = admin_api.get_all_licenses()
    print("All Licenses:", all_licenses)

    # Delete a license
    delete_result = admin_api.delete_license(license_uuid)
    print("Delete Result:", delete_result)

    # Get all licenses
    all_licenses = admin_api.get_all_licenses()
    print("All Licenses:", all_licenses)

