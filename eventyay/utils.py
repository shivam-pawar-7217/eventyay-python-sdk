from typing import Dict, Any, Optional
from urllib.parse import urlparse, parse_qs

def parse_pagination_params(url: str) -> Dict[str, Any]:
    """
    Extract pagination parameters (page, page_size) from a URL.
    Useful for handling 'next' links from API responses.
    
    Args:
        url: The full URL to parse.
        
    Returns:
        Dict containing 'page' and 'page_size' if found.
    """
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    
    pagination = {}
    if 'page[number]' in params:
        pagination['page[number]'] = params['page[number]'][0]
    elif 'page' in params:
        pagination['page'] = params['page'][0]
        
    if 'page[size]' in params:
        pagination['page[size]'] = params['page[size]'][0]
    elif 'page_size' in params:
        pagination['page_size'] = params['page_size'][0]
        
    return pagination

def clean_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove keys with None values from a dictionary.
    Useful for cleaning up query parameters.
    """
    return {k: v for k, v in data.items() if v is not None}
