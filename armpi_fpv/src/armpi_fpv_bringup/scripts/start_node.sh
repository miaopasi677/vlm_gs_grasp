#!/bin/bash
WS_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
exec "$WS_ROOT/run_robot.sh"
