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

$(curl -s -X POST "${BASE_URL}/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser2",
    "email": "testuser2@example.com",
    "password": "testpassword",
    "profile": "contractor"
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

login_response2=$(curl -s -X POST "${BASE_URL}/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser2",
    "password": "testpassword"
  }')

echo "Login response:"
echo $login_response | jq .


access_token=$(echo $login_response | jq -r .access_token)
access_token2=$(echo $login_response2 | jq -r .access_token)

echo "Getting user profile..."
profile_response=$(curl -s -X GET "${BASE_URL}/users/me" \
  -H "Authorization: Bearer $access_token")

profile_response2=$(curl -s -X GET "${BASE_URL}/users/me" \
  -H "Authorization: Bearer $access_token2")

echo "User profile response:"
echo $profile_response | jq .


echo "Creating a contract"

client_id=$(echo $profile_response | jq -r .id)
contractor_id=$(echo $profile_response2 | jq -r .id)

echo "Client ID: $client_id"
echo "Contractor ID: $contractor_id"

contract_response=$(curl -s -X POST "${BASE_URL}/contracts/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $access_token" \
  -d '{
    "title": "Test Contract",
    "description": "This is a test contract",
    "price": 1000,
    "client_id": "'$client_id'",
    "contractor_id": "'$contractor_id'"
  }')

echo "Contract Response:"
echo $contract_response | jq .
