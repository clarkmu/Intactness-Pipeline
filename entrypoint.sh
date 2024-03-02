#!/bin/sh
uvicorn server:app --reload --host 0.0.0.0 --port $PORT