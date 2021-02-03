#!/bin/bash -ex
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install --yes zip python3-venv

mkdir ~/archives
cd ~/archives

# Convert the sleep comments to print statement so there's a way to
# gauge progress and so that Circle doesn't shut things down due to
# lack of output (the latter is a theoretical concern).
sed -r 's/# sleep(.*)/print("sleep\1")/' \
  /github/workspace/controllers/example_controller/example_controller.py > robot.py

# Have the robot code print success at the end, along with a unique identifier.
echo "print('Success: $GITHUB_SHA')" >> robot.py

zip ABC.zip robot.py

cd /github/workspace
python3 -m venv venv
venv/bin/pip install -U pip
venv/bin/pip install -r libraries.txt

source ./venv/bin/activate
xvfb-run script/run-comp-match ~/archives 42 - ABC --duration 5 --no-record

LAST_LINE=$(tail --lines=1 ~/archives/ABC/log-zone-1-match-42.txt)
set -x
test "$LAST_LINE" == "1| Success: $GITHUB_SHA"
