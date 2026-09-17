from pathlib import Path
import shutil

build_py = Path("build.py")
workflow = Path(".github/workflows/flutter-build.yml")
staged_workflow = Path(".github/scripts/staged_flutter_build_phase3.yml")

build_text = build_py.read_text(encoding="utf-8")
old_build = "certleap-academy-{version}-install.exe"
new_build = "certleap-academy-{version}-portable.exe"
if old_build in build_text:
    if build_text.count(old_build) != 1:
        raise RuntimeError("expected one build.py install artifact name")
    build_text = build_text.replace(old_build, new_build, 1)
    build_py.write_text(build_text, encoding="utf-8")
elif new_build not in build_text:
    raise RuntimeError("could not find CertLeap portable artifact naming in build.py")

workflow_text = workflow.read_text(encoding="utf-8")
old_workflow = "./SignOutput/certleap-academy-${{ env.VERSION }}-${{ matrix.job.arch }}.exe"
new_workflow = "./SignOutput/certleap-academy-${{ env.VERSION }}-${{ matrix.job.arch }}-portable.exe"
workflow_changed = False
if old_workflow in workflow_text:
    if workflow_text.count(old_workflow) != 1:
        raise RuntimeError("expected one Flutter Windows portable artifact name")
    workflow_text = workflow_text.replace(old_workflow, new_workflow, 1)
    workflow.write_text(workflow_text, encoding="utf-8")
    workflow_changed = True
elif new_workflow not in workflow_text:
    raise RuntimeError("could not find CertLeap portable artifact naming in flutter-build.yml")

if workflow_changed:
    shutil.copyfile(workflow, staged_workflow)
    print(f"Staged modified release workflow at {staged_workflow}")
else:
    if staged_workflow.exists():
        staged_workflow.unlink()
    print("Release workflow already uses Portable artifact naming")

print("CertLeap Windows package naming is ready")
