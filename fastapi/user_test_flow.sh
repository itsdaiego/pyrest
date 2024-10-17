#!/bin/bash

BASE_URL="http://localhost:8000"

echo "Registering a new user..."

register_response=$(curl -s -X POST "${BASE_URL}/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "testpassword",
    "profile": "client"
  }')

echo "Registration response:"
echo $register_response | jq .

echo "Logging in..."

login_response=$(curl -s -X POST "${BASE_URL}/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpassword"
  }')

echo "Login response:"
echo $login_response | jq .


access_token=$(echo $login_response | jq -r .access_token)

echo "Getting user profile..."
profile_response=$(curl -s -X GET "${BASE_URL}/users/me" \
  -H "Authorization: Bearer $access_token")

echo "User profile response:"
echo $profile_response | jq .
