#!/bin/bash
export FLASK_DEBUG=1

gunicorn app:app

