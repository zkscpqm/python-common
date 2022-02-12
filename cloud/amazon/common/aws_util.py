from types_extensions import dict_type


def extract_aws_response_status_code(resp: dict_type) -> int:
    if meta_ := resp.get('ResponseMetadata'):
        return meta_.get('HTTPStatusCode')
    return 404
