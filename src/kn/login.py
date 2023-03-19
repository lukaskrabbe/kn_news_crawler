import requests
import logging
from datetime import datetime

logger = logging.getLogger('kn-login')

def login(session, secret):
    """

    Args:
        session:
        secret:

    Returns:
        boolean: True if successful
    """
    logger.info("Start login process with user: %s", secret['user'])

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Cookie': 'madsack-rnd-sso-hub=madsack-rnd-sso-hub6415906cd6c12; madsack-rnd-sso-hub-present=true'
    }
    payload= f"client_id=madsack-kn-epaper-web&code_challenge=_HiJPr_WQe8sKR0uTpPylHJAVp9tAJoAnpnQvNLfdW8&code_challenge_method=S256&origin=%2Fv4%2Fhub%2Fsso%2Flogin&password={requests.utils.quote(secret['password'])}&redirect_uri=https%3A%2F%2Fepaper.kieler-nachrichten.de%2Fsso-redirect&response_type=code&username={requests.utils.quote(secret['user'])}"

    # RND-login
    url = "https://account.rnd.de/v4/hub/sso/login"
    response = session.request("POST", url, headers=headers, data=payload)
    logger.info("account.rnd.de/sso/login - status code: %s" % response.status_code)
    assert response.status_code == 200


    url = "https://account.rnd.de/v4/hub/oauth?client_id=madsack-kn-epaper-web&redirect_uri=https%3A%2F%2Fepaper.kieler-nachrichten.de%2Fsso-redirect&response_type=code&code_challenge=_HiJPr_WQe8sKR0uTpPylHJAVp9tAJoAnpnQvNLfdW8&code_challenge_method=S256&origin=%2Fv4%2Fhub%2Fsso%2Flogin"
    response = session.request("GET", url, headers=headers)
    logger.info("account.rnd.de/hub/oauth - status code: %s" % response.status_code)
    assert response.status_code == 200

    # KN-Login
    del headers['Cookie']
    url = "https://epaper.kieler-nachrichten.de/sso-redirect?code=def50200c019da0f96208b2278d953389d87e6166e7b03fd2dafa5545193347a208709498242e39eb41fd7c2d2e459d3fb16b7e529140d4a43bd4869130c4102c75306e0d7114938df9306f3e7ac435e704d0c42850e6cedc628b52bf1063b0bc09d511c3f480eeda0b8d2eddc649f8127ab658237967ba832c703bb0f40a8ae51014c78827e0fa3ac8124b5b07e77f04cad2d916b4b1ae0cb3b6ad98e1de3be9f77c4453fb3283018051fba1c7db2b309438e23c862cc6acbb6388dc84ab6e750e7c20ada89f4398c6e86371c0e842f34b2c5d7945ceb56f974aad62a248c170d01a7e811eb17f985f6f9786af1324453b37fa39b3da7e1e96a68eac30d71fcf88f8838ad0a434e9f5ee8aff815ef149a5046e0846e7d4fe1cd3ad57ba03970defd6ff0deece565b3cea70fd57fa044419b77baea75471943b4e6ce96ddb7c16f8fcc9fd851eeb785d74310f30386d6ebe9092745d6f93793513b9b48c904beccd301897bdbb0311d84da8c763c1a57ea4c08f92b47196d5078f89920b10b31119d67842801884a192caf09b1aad0f7ac8a74cb3d52c468b84306134c7e3c71cd939df0187d8ce8a0e59400cb5c0bc2ea53eacb28632cb0"
    response = session.request("GET", url, headers=headers)
    logger.info("epaper.kieler-nachrichten.de/sso-redirect - status code: %s" % response.status_code)
    assert response.status_code == 200

    url = "https://epaper.kieler-nachrichten.de/kieler-nachrichten/" + datetime.today().strftime('%d.%m.%Y')
    response = session.request("GET", url, headers=headers)
    logger.info("epaper.kieler-nachrichten.de/kieler-nachrichten - status code: %s" % response.status_code)
    assert response.status_code == 200

    logger.info("Successful login with user: %s", secret['user'])
    return True


