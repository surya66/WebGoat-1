#!/usr/bin/env python

"""
Script: deploy_dast.py
Required Modules:
"""

__author__ = 'ratnesh'

import itertools
import os
import time
import datetime
import json
import requests
import socket
import time
from concurrent.futures import ThreadPoolExecutor
from defectdojo_api import defectdojo
from dd_config import DEFECT_DOJO_HOST, DEFECT_DOJO_API_KEY, DEFECT_DOJO_USERNAME, SCANNER, PROJECT_NAME, ARTIFACT_NAME


class DeployDast(object):
    """
        Class for Defect Dojo.
    """

    def __init__(self):
        """
            Init method
        """

        self.defect_dojo = defectdojo.DefectDojoAPI(DEFECT_DOJO_HOST, DEFECT_DOJO_API_KEY, DEFECT_DOJO_USERNAME,
                                                    debug=False)

    def create_project(self, project_name):
        """
        Create the project in defect dojo
        :param project_name:
        :return:
        """

        # Create a product
        prod_type = 1  # 2 - IT, product type
        return self.defect_dojo.create_product(project_name, project_name, prod_type)

    def get_project_list(self):
        """
        Get the list of project tabulated in defect dojo
        :return:
        """
        # List Products
        return self.defect_dojo.list_products()

    def get_artifact_list(self):
        """
        Get the list of artifact tabulated in defect dojo
        :return:
        """
        return self.defect_dojo.list_engagements()

    def create_artifact(self, artifact_name, project_id):
        """
        Create the artifact specific to project id provided in defect dojo
        :param artifact_name:
        :param project_id:
        :return:
        """
        print 'Artifact does not exist, creating.....'
        artifact_created = self.defect_dojo.create_engagement(name=artifact_name, product_id=project_id, lead_id=1,
                                                              status='In Progress',
                                                              target_start=str(datetime.date.today()),
                                                              target_end=str(datetime.date.today()))
        print artifact_created.data_json(pretty=True)  # Decoded JSON object
        return artifact_created


def fetch_project_id(project_list, project_name):
    """
    Get the project id of the specific project name from the project list in defect dojo
    :param project_list:
    :param project_name:
    :return:
    """
    project_id = ''
    if project_list.success:
        print project_list.data_json(pretty=True)  # Decoded JSON object
        for project in project_list.data["objects"]:
            if project['name'] == project_name:
                print project['name']  # Print project name
                project_id = project['id']  # Print project id
    else:
        print project_list.message
    print project_id
    return project_id


def check_if_artifact_exists(artifact_name, project_id, artifact_list):
    """
    Check if the specific artifact exists w.r.t project id provided in defect dojo
    :param artifact_name
    :param project_id
    :param artifact_list:
    :return:
    """
    artifact_exists = ''
    if artifact_list.success:
        # print(list_artifacts.data_json(pretty=True))  # Decoded JSON object
        for artifact in artifact_list.data["objects"]:
            if (artifact['name'] == artifact_name) and (artifact['product_id'] == project_id):
                artifact_exists = artifact['id']

    else:
        print artifact_list.message
    return artifact_exists


def upload_results(scanner, result_file, engagement_id):

    API_URL = DEFECT_DOJO_HOST +"/api/v1"
    IMPORT_SCAN_URL = API_URL + "/importscan/"
    AUTH_TOKEN = "ApiKey " + DEFECT_DOJO_USERNAME + ":" + DEFECT_DOJO_API_KEY

    headers = dict()
    json = dict()
    files = dict()
    headers['Authorization'] = AUTH_TOKEN

    json['minimum_severity'] = "Info"
    json['scan_date'] = datetime.date.today()
    json['verified'] = False
    json['tags'] = ""
    json['active'] = False
    json['engagement'] = "/api/v1/engagements/"+ str(engagement_id) + "/"
    json['lead'] ="/api/v1/users/"+ "1" + "/"
    json['scan_type'] = scanner

    # Prepare file data to send to API
    files['file'] = open(result_file)

    # Make a request to API

    response = requests.post(IMPORT_SCAN_URL, headers=headers, files=files, data=json, verify=False)

    return response.status_code


def upload_executor(project_name, artifact_name, scanner, result_file):
    """
    Execute the burp scan on provided port number
    :param scan_data:
    :param port_number:
    :param build_id:
    :return:
    """

    try:

        dd_obj = DeployDast()

        # Get project list in defect dojo
        project_list = dd_obj.get_project_list()

        # Get project id specific to project name
        project_id = fetch_project_id(project_list, project_name)

        # If project does not exists then create new project and fetch project id
        if not project_id:
            print('Project ID does not exists in defect dojo, Creating new one...')
            dd_obj.create_project(project_name)
            print('Getting latest project list from defect dojo...')
            project_list = dd_obj.get_project_list()
            print('Getting project ID after creating the project "{}" in defect dojo...'.format(project_name))
            project_id = fetch_project_id(project_list, project_name)
            print('Fetched project ID: {}'.format(project_id))

        # Get the list of artifacts
        print('Getting artifact list from defect dojo...')
        artifact_list = dd_obj.get_artifact_list()

        # Check if artifact exists
        print('Checking if artifact: {} exists in defect dojo...'.format(artifact_name))
        artifact_exists = check_if_artifact_exists(artifact_name, project_id, artifact_list)
        print('Fetched artifact[Engagement ID]: {}'.format(artifact_exists))
        if not artifact_exists:
            print('Artifact does not exists in defect dojo, Creating new one...')
            dd_obj.create_artifact(artifact_name, project_id)
            print('Getting latest artifact list from defect dojo...')
            artifact_list = dd_obj.get_artifact_list()
            print('Checking if artifact: {} exists in defect dojo...'.format(artifact_name))
            artifact_exists = check_if_artifact_exists(artifact_name, project_id, artifact_list)
            print('Fetched artifact[Engagement ID]: {}'.format(artifact_exists))


        result = upload_results(scanner=scanner, result_file=result_file, engagement_id=artifact_exists)
        if result == 201 :
            print "Successfully uploaded the results to Defect Dojo"
        else:
            print "Something went wrong, please debug " + str(result)


    except Exception as err_msg:
        output = "Error occurred, {}".format(err_msg)
        print(output)
    


if __name__ == '__main__':

    print "Defect Dojo module"
    
    for scanner in SCANNER:
        # print(scanner.replace(" ","-"))
        if scanner == 'Dependency Check Scan':
            upload_executor(project_name=PROJECT_NAME, artifact_name=ARTIFACT_NAME, scanner=scanner, result_file='/tmp' + scanner.replace(" ","-")+".xml")
        elif scanner == 'Snyk Scan':
            upload_executor(project_name=PROJECT_NAME, artifact_name=ARTIFACT_NAME, scanner=scanner, result_file='/tmp' + scanner.replace(" ","-")+".json")
        elif scanner == 'ZAP Scan':
            time.sleep(300)
            upload_executor(project_name=PROJECT_NAME, artifact_name=ARTIFACT_NAME, scanner=scanner, result_file='/tmp' + scanner.replace(" ","-")+".xml")