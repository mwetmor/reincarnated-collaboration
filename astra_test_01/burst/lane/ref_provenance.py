"""First-party reference path containment; canonical resolution blocks escapes.

Allowed roots: burst/runs/<run>/artifacts, run_0*, design/experiments, and
burst/fixtures. This is a provenance LOCATION check, not authorship inference
or a cryptographic content-hash check; reference bytes are hashed at staging.
"""
from pathlib import Path
ASTRA_ROOT=Path(__file__).resolve().parents[2]


def check(path):
    try:
        resolved=Path(path).expanduser().resolve(strict=True)
        root=ASTRA_ROOT.resolve(strict=True)
        if not resolved.is_file():return False,'Reference must be an existing file'
        try:parts=resolved.relative_to(root).parts
        except ValueError:return False,'Reference resolves outside first-party roots'
        allowed=(len(parts)>=2 and parts[0].startswith('run_0')) or (
            len(parts)>=3 and parts[:2]==('design','experiments')) or (
            len(parts)>=3 and parts[:2]==('burst','fixtures')) or (
            len(parts)>=5 and parts[:2]==('burst','runs') and parts[3]=='artifacts')
        if allowed:return True,'Resolved first-party reference path'
        return False,'Reference is not under a registered first-party content root'
    except (OSError,RuntimeError,ValueError,TypeError) as exc:
        return False,'Unresolvable reference: '+str(exc)
