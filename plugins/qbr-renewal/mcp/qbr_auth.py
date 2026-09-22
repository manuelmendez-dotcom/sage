"""Per-user, route-scoped sign-in through the automatically provisioned CLI."""
import json
import shutil
import subprocess

QBR_URL = "https://qbr-express.internal.zenai-apps.com"


def pomerium_token() -> str:
    executable = shutil.which("pomerium-cli")
    if not executable:
        raise RuntimeError("The QBR sign-in component is missing. Rerun the one-command installer.")
    try:
        result = subprocess.run([executable, "k8s", "exec-credential", QBR_URL],
                                check=True, capture_output=True, text=True, timeout=90)
        token = json.loads(result.stdout)["status"]["token"]
        if not isinstance(token, str) or not token.removeprefix("Pomerium-"):
            raise ValueError("empty credential")
        return token.removeprefix("Pomerium-")
    except (subprocess.SubprocessError, ValueError, KeyError, TypeError):
        raise RuntimeError("QBR sign-in is needed. Complete company sign-in in your browser and reconnect.") from None
