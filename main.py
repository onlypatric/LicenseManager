from dataclasses import dataclass
import re
from typing import List, Literal, Union
from uuid import uuid4
from typing import Union
from flask import Flask, request, jsonify, Response
import datetime


def validateExpiry(date: Union[str, Literal["lifetime"], None]):
    # check date to match dd/mm/yyyy
    if date == "lifetime":
        return True
    elif date == None:
        return True
    isValideDate = re.match(r"^\d{2}/\d{2}/\d{4}$", date)
    if isValideDate:
        return True
    return False

def genUUID():
    return uuid4().__str__().upper()
@dataclass
class License:
    devices: List[str] = None
    bannedDevices: List[str] = None
    until: Union[str, Literal["lifetime"], None] = None
    uuid: str = ""
    def addDevice(self, deviceIP):
        if deviceIP in self.devices:
            return
        self.devices.append(deviceIP)

    def banDevice(self, deviceIP):
        self.bannedDevices.append(deviceIP)

    def checkDevice(self, deviceIP):
        if deviceIP not in self.devices:
            self.devices.append(deviceIP)
        return not (deviceIP in self.bannedDevices)

    def setExpiry(self, date: Union[str, Literal["lifetime"], None]):
        self.until = date


class Licenses:
    licenses: List[License] = []

    def addLicense(self, license: License):
        self.licenses.append(license)
        for license in self.licenses:
            if license.bannedDevices==None:
                license.bannedDevices=[]
            if license.devices==None:
                license.devices=[]

    def checkLicense(self, uuid: str):
        for license in self.licenses:
            if license.uuid == uuid:
                return license
        return None

    def findLicense(self, uuid, ip: str = None):
        for license in self.licenses:
            if license.bannedDevices==None:
                license.bannedDevices=[]
            if license.devices==None:
                license.devices=[]
            if license.uuid == uuid:
                if ip is not None:
                    if license.checkDevice(ip):
                        return license
                return license

    def removeLicense(self, uuid):
        for license in self.licenses:
            if license.uuid == uuid:
                self.licenses.remove(license)

    def updateLicense(self, uuid, license: License):
        for license in self.licenses:
            if license.uuid == uuid:
                license.devices = license.devices
                license.bannedDevices = license.bannedDevices
                license.until = license.until
                return license

    def updateLicenseExpiry(self, uuid, date: Union[str, Literal["lifetime"], None]):
        for license in self.licenses:
            if license.bannedDevices==None:
                license.bannedDevices=[]
            if license.devices==None:
                license.devices=[]
            if license.uuid == uuid:
                license.until = date
                return license


license_manager = Licenses()
app = Flask("QTik License Manager")


@app.route("/admin/licenses", methods=["POST"])
def create_license():
    # Create a new license and add it to the manager
    
    license = License(uuid=genUUID())
    license_manager.addLicense(license)
    return jsonify({"message": "License created", "uuid": license.uuid})

@app.route("/admin/licenses/<uuid>/ban_device", methods=["POST"])
def ban_device(uuid):
    data = request.json
    device_to_ban = data.get("expiryDate")

    # Find the license with the given UUID
    license = license_manager.findLicense(uuid)

    if license:
        # Check if the device is in the list of devices associated with the license
        if device_to_ban in license.devices:
            # Add the device to the list of banned devices
            license.banDevice(device_to_ban)
            return jsonify({"message": f"Device {device_to_ban} banned from the license", "uuid": license.uuid})

    return jsonify({"message": "Device not found or license not found"}), 400

@app.route("/admin/licenses/<uuid>", methods=["PUT"])
def update_license(uuid):
    # Update the license details, including devices and expiry date
    license = license_manager.findLicense(uuid)
    if license:
        # Implement logic to update license details here
        return jsonify({"message": "License updated", "uuid": license.uuid})
    else:
        return jsonify({"message": "License not found"})


@app.route("/admin/licenses/<uuid>", methods=["DELETE"])
def delete_license(uuid):
    # Delete a license
    license_manager.removeLicense(uuid)
    return jsonify({"message": "License deleted"})


@app.route("/admin/licenses", methods=["GET"])
def get_all_licenses():
    # Retrieve a list of all licenses
    licenses = []
    for license in license_manager.licenses:
        # Include relevant license information in the response
        licenses.append({
            "uuid": license.uuid,
            "devices": license.devices,
            "bannedDevices": license.bannedDevices,
            "expiryDate": license.until
        })
    return jsonify({"licenses": licenses})
@app.route("/admin/licenseinfo/<uuid>", methods=["GET"])
def get_license_info(uuid):
    return jsonify({"license": None if license_manager.findLicense(uuid) is None else license_manager.findLicense(uuid).__dict__})


@app.route("/admin/licenses/<uuid>/set_expiry", methods=["POST"])
def set_expiry_date(uuid):
    # Set the expiry date for a license
    data = request.form
    expiry_date = data.get("expiryDate")
    
    # Check if the UUID is valid
    license = license_manager.findLicense(uuid,ip=request.remote_addr)
    print(uuid)
    if not license:
        return jsonify({"message": "License not found"}), 404

    # Validate the expiry date
    if validateExpiry(expiry_date):
        license.setExpiry(expiry_date)
        return jsonify({"message": "Expiry date set", "uuid": license.uuid})
    else:
        return jsonify({"message": "Invalid expiry date"}), 400
# User route


@app.route("/activate/<uuid>", methods=["POST"])
def activate_license(uuid):
    # User only needs to activate the license by providing the UUID
    license = license_manager.findLicense(uuid)
    if license:
        # Implement activation logic here if needed
        return jsonify({"message": f"License activated until: {license.until}"})
    else:
        return jsonify({"message": "License not found or not avaiable for this device"}), 404


if __name__ == "__main__":
    app.run(port=8000)
