import requests


def download(package_name):
    """
    Return download link for package_name
    """
    app_info_url = 'https://api.cafebazaar.ir/rest-v1/process/AppDownloadInfoRequest'
    request_headers = {
        'Accept': 'application/json',
        'Content-type': 'application/json',
    }
    request_data = {
        "properties": {
            "androidClientInfo": {
                "sdkVersion": 22,
                "cpu": "x86,armeabi-v7a,armeabi"
            }
        },
        "singleRequest": {
            "appDownloadInfoRequest": {
                "downloadStatus": 1,
                "packageName": package_name,
            }
        }
    }

    response = requests.post(app_info_url, headers=request_headers, json=request_data)
    if response.status_code == 200:
        response_data = response.json()
        token = response_data['singleReply']['appDownloadInfoReply']['token']
        cdnPrefix = response_data['singleReply']['appDownloadInfoReply']['cdnPrefix'][0]
        download_link = f'{cdnPrefix}apks/{token}.apk'
        package_size = response_data['singleReply']['appDownloadInfoReply']['packageSize']
        installation_size = response_data['singleReply']['appDownloadInfoReply']['installationSize']
        return {
            'status': 'success',
            'status_code': response.status_code,
            'data': {
                'download_link': download_link,
                'package_size': package_size,
                'installation_size': installation_size,
            }
        }
    return {
        'status': 'error',
        'status_code': response.status_code,
        'message': response.text,
    }